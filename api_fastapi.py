# -*- coding: utf-8 -*-
import os

import uvicorn
from fastapi import FastAPI, File, HTTPException, Depends, Body, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from model import (
    ChatResponse,
    ChatRequest,
    InsertTextsResponse,
    InsertTextsFromTairRequest,
    InsertTextsFromTairResponse,
    TairSetRequest,
    TairSetResponse
)
from chatbot import get_chatbot
from typing import List

app = FastAPI()  # 创建API实例


@app.get("/")
def root():
    return {"message": "Hi,Tair Guys!"}


@app.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
        request: ChatRequest = Body(...),
):
    try:
        answer = chatbot.chat(request.text)
        return ChatResponse(text=answer)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")

@app.post(
    "/chat_by_prompt",
    response_model=ChatResponse,
)
async def chat(
        request: ChatRequest = Body(...),
):
    try:
        answer = chatbot.chat_by_prompt(request.text)
        return ChatResponse(text=answer)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.post(
    "/insertTextsFromTair",
    response_model=InsertTextsFromTairResponse,
)
async def insert_texts_from_tair(
        request : InsertTextsFromTairRequest=Body(...)
):
    try:
        chatbot.insert_texts_from_tair(request.keys)
        response = InsertTextsFromTairResponse(keys=request.keys)
        return response
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")

@app.post(
    "/setDataToTair",
    response_model=TairSetResponse,
)
async def set_data_to_tair(
        request : TairSetRequest=Body(...)
):
    try:
        chatbot.set_data_to_tair(request)
        response = TairSetResponse(keys=[item.key for item in request.kv])
        return response
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")

@app.post(
    "/insertTextFiles",
    response_model=InsertTextsResponse,
)
async def insert_texts(
        files: List[UploadFile] = File(...),
):
    response=InsertTextsResponse(filenames=[])
    for file in files:
        cont = await file.read()
        current_dir = os.getcwd()
        filename = os.path.join(current_dir,f'upload_text/{file.filename}')
        with open(filename,'wb') as f:
            f.write(cont)
        response.filenames.append(filename)

    try:
        for filename in response.filenames:
            chatbot.insert_text(filename)
        return response
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")


# @app.post(
#     "/upsert-texts",
#     response_model=UpsertTextResponse,
# )
# async def upsert_texts(
#     request: UpsertTextRequest= Body(...),
# ):
#     try:
#         filenames = UpsertTextResult(keys=[])
#         for upsertText in request.upsertTexts:
#             with open(f'upload_texts.txt', 'w') as f:
#                 f.write(upsertText.text)
#             filenames.keys.append(upsertText.text)
#             vector_clip.upsert_text(upsertText.text,upsertText.text)
#         return UpsertTextResponse(upsertTextResult=filenames)
#     except Exception as e:
#         print("Error:", e)
#         raise HTTPException(status_code=500, detail=f"str({e})")
#
# @app.post(
#     "/query_images_by_text",
#     response_model=QueryImageResponse,
# )
# def query_images_by_text(
#     request: QueryRequest = Body(...),
# ):
#     try:
#         results = vector_clip.query_images_by_text(
#             request.query.query,request.query.top_k
#         )
#         return QueryImageResponse(results=results)
#     except Exception as e:
#         print("Error:", e)
#         raise HTTPException(status_code=500, detail="Internal Service Error")
#
# @app.post(
#     "/query_images_by_image",
#     response_model=QueryImageResponse,
# )
# async def query_images_by_image(
#     files: UploadFile = File(...),
# ):
#     cont = await files.read()
#     with open(f'query_images/{files.filename}','wb') as f:
#         f.write(cont)
#     try:
#         results = vector_clip.query_images_by_image(f'query_images/{files.filename}')
#         return QueryImageResponse(results=results)
#     except Exception as e:
#         print("Error:", e)
#         raise HTTPException(status_code=500, detail=f"str({e})")
#
# @app.post(
#     "/query_texts_by_text",
#     response_model=QueryTextResponse,
# )
# def query_texts_by_text(
#     request: QueryRequest = Body(...),
# ):
#     try:
#         results = vector_clip.query_texts_by_text(
#             request.query.query,request.query.top_k
#         )
#         return QueryTextResponse(results=results)
#     except Exception as e:
#         print("Error:", e)
#         raise HTTPException(status_code=500, detail="Internal Service Error")
#
# @app.post(
#     "/query_texts_by_image",
#     response_model=QueryTextResponse,
# )
# async def query_texts_by_image(
#     files: UploadFile = File(...),
# ):
#     cont = await files.read()
#     with open(f'query_images/{files.filename}','wb') as f:
#         f.write(cont)
#     try:
#         results = vector_clip.query_texts_by_image(f'query_images/{files.filename}')
#         return QueryTextResponse(results=results)
#     except Exception as e:
#         print("Error:", e)
#         raise HTTPException(status_code=500, detail=f"str({e})")

@app.on_event("startup")
async def startup():
    global chatbot
    chatbot = get_chatbot()


if __name__ == "__main__":
    uvicorn.run("api_fastapi:app", host="0.0.0.0", port=9001, reload=True)
