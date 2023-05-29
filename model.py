from pydantic import BaseModel
from typing import List, Optional

# class QueryImageResult(BaseModel):
#     path: str
#     distance: str
#
# class QueryImageResponse(BaseModel):
#     results: List[QueryImageResult]
#
# class Query(BaseModel):
#     query: str
#     top_k: Optional[int] = 3
#
# class QueryRequest(BaseModel):
#     query: Query
#
# class UpsertImageResult(BaseModel):
#     keys:List[str]
#
# class UpsertImageResponse(BaseModel):
#     upsertImageResult:UpsertImageResult
#
# class UpsertTextResult(BaseModel):
#     keys:List[str]
#
# class UpsertTextResponse(BaseModel):
#     upsertTextResult:UpsertTextResult
#
# class UpsertText(BaseModel):
#     text:str
#
# class UpsertTextRequest(BaseModel):
#     upsertTexts:List[UpsertText]
#
# class QueryTextResult(BaseModel):
#     text: str
#     distance: str
#
# class QueryTextResponse(BaseModel):
#     results: List[QueryTextResult]

class ChatResponse(BaseModel):
    text:str

class ChatRequest(BaseModel):
    text:str

class InsertTextsResponse(BaseModel):
    filenames:List[str]

class InsertTextsFromTairRequest(BaseModel):
    keys:List[str]

class InsertTextsFromTairResponse(BaseModel):
    keys:List[str]

class KeyValue(BaseModel):
    key:str
    value:str

class TairSetRequest(BaseModel):
    kv:List[KeyValue]

class TairSetResponse(BaseModel):
    keys:List[str]