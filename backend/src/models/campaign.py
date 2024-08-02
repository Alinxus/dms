# backend/src/models/campaign.py

from pydantic import BaseModel
from typing import List, Optional

class Campaign(BaseModel):
    id: str
    user_id: str
    name: str
    message_template: str
    status: str
    created_at: str
    updated_at: str

class CampaignCreate(BaseModel):
    user_id: str
    name: str
    message_template: str

class CampaignResponse(BaseModel):
    id: str
    name: str
    status: str