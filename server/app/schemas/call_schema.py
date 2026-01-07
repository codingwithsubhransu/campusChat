from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class CallLog(Base):
    __tablename__ = "call_logs"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    caller_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)

    call_type = Column(String(20), default="audio")  # e.g., audio, video
    status = Column(String(20), default="missed", nullable=False)  # e.g., missed, answered, declined
    start_time = Column(DateTime, server_default=func.now())
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)  # duration in seconds

    caller = relationship("User", foreign_keys=[caller_id])