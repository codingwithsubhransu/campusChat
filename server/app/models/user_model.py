from pydantic import BaseModel, Field, EmailStr


class RegisterModelIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email_id: EmailStr
    password: str = Field(..., min_length=6, max_length=128)

class UserModel(BaseModel):
    username: str

class LoginModelIn(BaseModel):
    username_or_email: str
    password: str


class OtpRequestModel(BaseModel):
    email_id: EmailStr

class OtpModel(BaseModel):
    otp: str