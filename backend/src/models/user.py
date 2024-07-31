# backend/src/models/user.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(BaseModel):
    id: str
    email: EmailStr
    password_hash: str
    full_name: str
    connected_accounts: Optional[List[dict]] = []
    created_at: str
    updated_at: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    connected_accounts: List[dict]