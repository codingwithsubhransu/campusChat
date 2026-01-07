from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db, engine, Base
from sqlalchemy import text
from app.routes.register_route import router as register_router
from app.routes.login_route import router as login_router
from app.routes.otp_route import router as otp_router
from app.core.security import get_current_user
from app.routes.user_route import router as user_router
from app.routes.chat_route import router as chat_router

from app.schemas.user_schema import User
from app.schemas.message_schema import Message
from app.schemas.contact_schema import Contact
from app.schemas.group_schema import Group, GroupMembers

app = FastAPI()

# main.py
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register_router, prefix="/api", tags=["Register"])
app.include_router(login_router, prefix="/api", tags=["Login"])
app.include_router(otp_router, prefix="/api", tags=["OTP"])
app.include_router(user_router, prefix="/api", tags=["User"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])


@app.on_event("startup")
async def startup_event():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Database connection failed {e}")

@app.get("/health")
def health_check():
    return {"message": "This backend is healthy!"}

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    return {"message": "Database session is active"}