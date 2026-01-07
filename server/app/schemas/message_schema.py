from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index= True, unique= True, autoincrement= True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable= False)

    # if receiver_id is set then it is a DM
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable= True)

    # if group_id is set then it is a group message
    group_id = Column(Integer, ForeignKey("groups.id"), nullable= True)

    content = Column(Text, nullable= False)
    message_type = Column(String(20), default= "text")  # e.g., text, image, video, etc.
    file_url = Column(String(500), nullable= True)

    is_read = Column(Boolean, default= False)
    created_at = Column(DateTime, server_default= func.now())

    sender = relationship("User", foreign_keys=[sender_id])
    group = relationship("Group", back_populates="messages")

