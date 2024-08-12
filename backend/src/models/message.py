# backend/src/models/message.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..database import Base

class MessageModel(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    platform = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    content = Column(String, nullable=False)
    status = Column(String, default='queued')  # 'queued', 'sent', 'failed'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserModel", back_populates="messages")

class MessageCreate(BaseModel):
    user_id: int
    platform: str
    recipient: str
    content: str

class MessageResponse(BaseModel):
    id: int
    platform: str
    recipient: str
    content: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class Message(BaseModel):
    id: int
    user_id: int
    platform: str
    recipient: str
    content: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True