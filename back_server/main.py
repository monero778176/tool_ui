# from asyncio import threads

import time
from fastapi import FastAPI,Form,File, UploadFile,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, List,Tuple


# from test_model import *
from cropper_module import router as crop_router
app = FastAPI()

origins = [
    
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crop_router.router,prefix='/api/cropper',tags=['cropper'])



@app.get("/")
async def main():
    return {"message": "Hello World"}




        