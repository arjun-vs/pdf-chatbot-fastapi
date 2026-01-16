from pydantic import BaseModel, EmailStr
from enum import Enum

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class ChatResponse(BaseModel):
    user: EmailStr
    question: str
    answer: str