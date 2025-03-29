from pydantic import BaseModel,Field,constr
from typing import Annotated, List,Tuple



class Base64(BaseModel):
    photo_name: str
    base64_str: bytes

class ImageRequest(BaseModel):
    images: List[str]  # 接收 base64 字串的陣列    

class image_base(BaseModel):
    index:int
    bs64: str

class ImageRequestwithID(BaseModel):
    images: List[image_base]  # 接收 base64 字串的陣列    