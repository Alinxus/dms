# backend/src/models/message.py

from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    id: str
    user_id: str
    platform: str
    recipient: str
    content: str
    status: str  # 'queued', 'sent', 'failed'
    created_at: str
    updated_at: str

class MessageCreate(BaseModel):
    user_id: str
    platform: str
    recipient: str
    content: str

class MessageResponse(BaseModel):
    id: str
    platform: str
    recipient: str
    content: str
    status: str
    created_at: str