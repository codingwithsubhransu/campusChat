from fastapi import APIRouter, HTTPException, Depends, Response
from app.models.user_model import UserModel
from app.schemas.user_schema import User
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password, create_access_token
from app.core.otp_config import send_otp_via_email
from app.models.user_model import RegisterModelIn
from sqlalchemy.future import select
from sqlalchemy import or_
import random

 
router = APIRouter()

@router.post("/register")
async def register_user(response: Response, user: RegisterModelIn, db: AsyncSession = Depends(get_db)):
    # Check for existing user
    result = await db.execute(select(User).where(or_(User.username == user.username, User.email_id == user.email_id)))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    hashed_pwd = hash_password(user.password)

    # Create User with is_verified=False
    new_user = User(
        username=user.username.lower(),
        email_id=user.email_id,
        password=hashed_pwd,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Create Token using the new ID (converted to string)
    access_token = create_access_token(data={"sub": str(new_user.id)})
    
    # Set HttpOnly Cookie
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True, 
        max_age=86400, 
        samesite="lax", 
        secure=False # Set to True in production
    )

    return {
        "message": "User registered. Verify your email to continue.",
        "access_token": access_token,
        "token_type": "bearer",
        "username": new_user.username,
        "is_verified": False
    }