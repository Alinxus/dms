# backend/src/utils/db_operations.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from ..models.user import UserModel, UserCreate
from ..config import DATABASE_URL
import bcrypt
from ..models.campaign import CampaignModel, CampaignCreate
from ..models.message import MessageModel, MessageCreate


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_message(db: Session, message: MessageCreate) -> MessageModel:
    db_message = MessageModel(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_user(db: Session, user_id: int, status: List[str] = None) -> List[MessageModel]:
    query = db.query(MessageModel).filter(MessageModel.user_id == user_id)
    if status:
        query = query.filter(MessageModel.status.in_(status))
    return query.all()

def update_message_status(db: Session, message_id: int, new_status: str) -> MessageModel:
    db_message = db.query(MessageModel).filter(MessageModel.id == message_id).first()
    if db_message:
        db_message.status = new_status
        db.commit()
        db.refresh(db_message)
    return db_message
def create_campaign(db: Session, campaign: CampaignCreate) -> CampaignModel:
    db_campaign = CampaignModel(**campaign.dict())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

def get_user_campaigns(db: Session, user_id: int) -> List[CampaignModel]:
    return db.query(CampaignModel).filter(CampaignModel.user_id == user_id).all()

def update_campaign(db: Session, campaign_id: int, updated_data: dict) -> CampaignModel:
    db_campaign = db.query(CampaignModel).filter(CampaignModel.id == campaign_id).first()
    if db_campaign:
        for key, value in updated_data.items():
            setattr(db_campaign, key, value)
        db.commit()
        db.refresh(db_campaign)
    return db_campaign

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(user: UserCreate) -> UserModel:
    db = next(get_db())
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = UserModel(
        email=user.email,
        password_hash=hashed_password.decode('utf-8'),
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(email: str) -> UserModel:
    db = next(get_db())
    return db.query(UserModel).filter(UserModel.email == email).first()

def update_user(user: UserModel) -> UserModel:
    db = next(get_db())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_accounts(user_id: int) -> list:
    db = next(get_db())
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    return user.connected_accounts if user else []

# You'll need to create similar functions for campaigns, messages, etc.