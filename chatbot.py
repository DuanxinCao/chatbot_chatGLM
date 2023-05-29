import os
import torch
from transformers import AutoTokenizer, AutoModel
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from utils import torch_gc,ChineseTextSplitter
from langchain.document_loaders import UnstructuredFileLoader, TextLoader
from langchain.vectorstores import Tair
from langchain.schema import Document
from typing import Iterator, List, Optional
from tair_wrapper import TairWrapper
from model import TairSetRequest

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"
EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
TAIR_URL = "redis://120.27.213.45:6380"
IP = "120.27.213.45"
PORT = 6380
INDEX_NAME = "langchain"
TOPK = 10
PROMPT_TEMPLATE = """已知信息：
{context} 

根据上述已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”，不允许在答案中添加编造成分，答案请使用中文。 问题是：{question}"""

class ChatBot():
    def __init__(self):
        self.text_embeddings_model= HuggingFaceEmbeddings(model_name='GanymedeNil/text2vec-large-chinese',
                                           model_kwargs={'device': EMBEDDING_DEVICE})
        torch_gc()
        self.vector_store = Tair(self.text_embeddings_model,TAIR_URL,INDEX_NAME)
        self.tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
        self.llm_model = AutoModel.from_pretrained("/root/ChatGLM-6B/THUDM/chatglm-6b-int4-qe",
                                          trust_remote_code=True).half().cuda()
        self.llm_model = self.llm_model.eval()
        torch_gc()

    def chat(self,question:str):
        response, history = self.llm_model.chat(self.tokenizer, question, history=[])
        return response

    def insert_text_to_tair(self,docs:List[Document]=None,filename:str=""):
        keys = []
        for doc_index in range(len(docs)):
            keys.append(f'{filename}_{doc_index}')
        Tair.from_documents(docs, self.text_embeddings_model, tair_url=TAIR_URL, keys=keys)

    def insert_text(self,filepath:str):
        loader = TextLoader(filepath, autodetect_encoding=True)
        textsplitter = ChineseTextSplitter(pdf=False, sentence_size=100)
        docs= loader.load_and_split(textsplitter)
        self.insert_text_to_tair(docs,filepath)

    def insert_texts(self,filedir:str):
        for root,dirs,files in os.walk(filedir):
            for file in files:
                filepath = os.path.join(root,file)
                self.insert_text(filepath)

    def chat_by_prompt(self,query:str,topk:int=TOPK):
        context = self.vector_store.similarity_search(query, k=topk)
        context = "\n".join([doc.page_content for doc in context])
        prompt = PROMPT_TEMPLATE.replace("{question}", query).replace("{context}", context)
        response = self.chat(prompt)
        return response

    def insert_texts_from_tair(self,keys:List[str]):
        client = TairWrapper(IP,PORT)
        tairvector_text = []
        tairvector_meta = []
        tairvector_key = []
        for key in keys:
            result = client.get(key)
            result = str(result, encoding="utf-8")
            tairvector_text.append(result)
            tairvector_meta.append({"source":f"{key}"})
            tairvector_key.append(key)
        Tair.from_texts(tairvector_text,self.text_embeddings_model,tairvector_meta,INDEX_NAME,"content","metadata",tair_url=TAIR_URL)

    def set_data_to_tair(self,request:TairSetRequest):
        client = TairWrapper(IP,PORT)
        for item in request.kv:
            client.set(item.key,item.value)

def get_chatbot():
    return ChatBot()





