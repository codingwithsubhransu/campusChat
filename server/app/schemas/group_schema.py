from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from app.db.database import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    group_pic = Column(String(255), nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    members = relationship("GroupMembers", back_populates="group")
    messages = relationship("Message", back_populates="group")


class GroupMembers(Base):
    __tablename__ = "group_members"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_admin = Column(Boolean, default=False)
    joined_at = Column(DateTime, server_default=func.now())

    group = relationship("Group", back_populates="members")
    user = relationship("User")