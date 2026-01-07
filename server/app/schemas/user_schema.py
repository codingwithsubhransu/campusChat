from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, unique= True, primary_key= True, autoincrement= True)
    # login credentials
    username = Column(String(50), nullable= False, unique= True)
    email_id = Column(String(150), nullable= False, unique= True)
    password = Column(String(255), nullable= False)

    #verification properties
    is_verified = Column(Boolean, default= False)
    otp = Column(String(6), nullable= True)

    # user profile details
    name = Column(String(100), nullable= True)
    profile_pic = Column(String(255), nullable= True)
    bio = Column(String(150), nullable= True)

    # user activity tracking
    last_login = Column(DateTime, nullable= True)
    created_at = Column(DateTime, server_default= func.now())
    updated_at = Column(DateTime, server_default= func.now(), onupdate= func.now())