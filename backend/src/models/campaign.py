# backend/src/models/campaign.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..database import Base

class CampaignModel(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, index=True)
    message_template = Column(String)
    status = Column(String, default='created')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserModel", back_populates="campaigns")

class CampaignCreate(BaseModel):
    user_id: int
    name: str
    message_template: str

class CampaignResponse(BaseModel):
    id: int
    name: str
    status: str

    class Config:
        orm_mode = True

class Campaign(BaseModel):
    id: int
    user_id: int
    name: str
    message_template: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mo