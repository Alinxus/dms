# backend/src/utils/auth.py

import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from ..config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_DELTA
from ..models.user import User
from ..utils.db_operations import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(user: User):
    expire = datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_DELTA)
    to_encode = {
        "sub": user.email,
        "exp": expire,
    }
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

async def get_current_user(token: str):
    email = decode_access_token(token)
    if email is None:
        return None
    user = get_user_by_email(email)
    if user is None:
        return None
    return user