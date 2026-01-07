from fastapi import APIRouter, HTTPException, Depends, Response
from app.models.user_model import UserModel, LoginModelIn, OtpModel, OtpRequestModel
from app.schemas.user_schema import User
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password, create_access_token, get_current_user
from app.core.otp_config import send_otp_via_email
from sqlalchemy.future import select
from sqlalchemy import or_
import random
from pydantic import EmailStr

router = APIRouter()


@router.get("/resend-otp")
async def resend_otp(
    current_user: dict = Depends(get_current_user), # Note: type hint is dict
    db: AsyncSession = Depends(get_db)
):
    # get_current_user already checked the token. If it returned None:
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid session. Please login again.")
    
    # Fetch the actual SQLAlchemy object so we can update the OTP column
    # Use the 'user_id' from the dictionary returned by get_current_user
    result = await db.execute(select(User).where(User.id == current_user["user_id"]))
    db_user = result.scalars().first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User account not found")

    # Generate and Save new OTP
    new_otp = str(random.randint(100000, 999999))
    db_user.otp = new_otp
    await db.commit()
    
    # Send the email
    try:
        await send_otp_via_email(db_user.email_id, new_otp)
    except Exception as e:
        # Log the error but don't stop the response
        print(f"Mail delivery failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email. Please try again later.")
    
    return {"message": f"A new OTP has been sent to {db_user.email_id}"}

@router.post("/verify-otp")
async def verify_otp(otp_data: OtpModel, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await db.execute(select(User).where(User.id == current_user["user_id"]))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.otp != otp_data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    user.is_verified = True
    user.otp = None  # Clear OTP after successful verification
    await db.commit()
    
    return {"message": "OTP verified successfully"}