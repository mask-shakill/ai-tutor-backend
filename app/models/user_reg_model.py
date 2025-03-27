# app/models.py
from pydantic import BaseModel, EmailStr # type: ignore

class UserCreate(BaseModel):
    email: EmailStr
    password: str
