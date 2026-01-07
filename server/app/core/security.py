from passlib.context import CryptContext
from fastapi import Request, WebSocket, status, HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from fastapi import Depends
from app.db.database import get_db
from app.schemas.user_schema import User

load_dotenv()
    

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60*24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

from fastapi import HTTPException, status

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    # 1. Look for token in Cookies
    token = request.cookies.get("access_token")
    
    # Define the exception to reuse
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception
        
    try:
        # 2. Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        
        if user_id_str is None:
            raise credentials_exception
            
        user_id = int(user_id_str)
        
    except (JWTError, ValueError):
        raise credentials_exception

    # 3. Database Query
    query = select(User).where(User.id == user_id)
    user_exec = await db.execute(query)
    user = user_exec.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    # Return a dictionary (or the user object itself)
    return {
        "username": user.username, 
        "user_id": user.id, 
        "email": user.email_id, 
        "is_verified": user.is_verified
    }

from fastapi import WebSocket, status, Query
from jose import jwt, JWTError

async def get_current_user_ws(
    websocket: WebSocket, 
    db: AsyncSession, 
    token: str = None  # We will extract this manually or via Query
):
    # 1. If token wasn't passed in params, try to get it from query_params manually
    if not token:
        token = websocket.query_params.get("token")

    if not token:
        return None
        
    try:
        # 2. Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get("sub")
        
        if not user_id_str:
            return None
            
        user_id = int(user_id_str)
        
        # 3. Database Query
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        
        return user  # Returns the actual User object
        
    except (JWTError, ValueError):
        return None