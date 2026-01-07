from sqlalchemy import ForeignKey, UniqueConstraint
from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(String(20), default="active")
    created_at = Column(DateTime, server_default=func.now())

    contact_info = relationship("User", foreign_keys=[contact_id])

    __table_args__ = (UniqueConstraint("user_id", "contact_id", name="_user_contact_uc"),)
