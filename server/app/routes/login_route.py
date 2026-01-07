from fastapi import APIRouter, HTTPException, Depends, Response
from app.models.user_model import UserModel, LoginModelIn
from app.schemas.user_schema import User
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password, create_access_token
from app.core.otp_config import send_otp_via_email
from sqlalchemy.future import select
from sqlalchemy import or_
import random
from app.core.security import get_current_user

router = APIRouter()
@router.post("/login")
async def login_users(response: Response, user: LoginModelIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(or_(User.username == user.username_or_email, User.email_id == user.username_or_email)))
    db_user = result.scalars().first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username/email or password")
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    
    # Set HttpOnly Cookie
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,   # Prevents JavaScript theft (XSS protection)
        max_age=86400,   # Expires in 24 hours
        samesite="lax",  # Standard for most web apps
        secure=False     # Set to True only when you have HTTPS (SSL)
    )

    # Return JSON for Local Storage
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "username": db_user.username,
        "is_verified": db_user.is_verified # Helpful for React to know where to redirect
    }


@router.get("/current-user", response_model=UserModel)
async def get_current_logged_in_user(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"username": current_user["username"]}


@router.get("/current_user_is_verified")
async def check_user_verified(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"is_verified": current_user["is_verified"]}

@router.post("/logout")
async def logout_user(response: Response):
    try:
        response.delete_cookie(key="access_token")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error during logout")
    return {"message": "Logged out successfully"}