# backend/src/models/account.py

from pydantic import BaseModel
from typing import Optional

class Account(BaseModel):
    id: str
    user_id: str
    platform: str
    username: str
    created_at: str
    updated_at: str

class AccountCreate(BaseModel):
    user_id: str
    platform: str
    username: str
    password: str  # Note: This should be handled securely, preferably encrypted

class AccountResponse(BaseModel):
    id: str
    platform: str
    username: str