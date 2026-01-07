from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user
from app.core.security import get_current_user_ws
from app.db.database import get_db
from sqlalchemy import select, or_, and_, func, desc
from app.schemas.user_schema import User
from app.schemas.message_schema import Message
from app.schemas.group_schema import Group, GroupMembers
from app.core.chat_manager import manager
import json


router = APIRouter()
@router.get("/recent-chats")
async def get_recent_chats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user['user_id']

    query = (
        select(
            User.id,
            User.username,
            User.name,
            User.profile_pic,
            func.max(Message.created_at).label("last_message_time")
        )
        .join(
            Message, or_(
                and_(Message.sender_id == user_id, Message.receiver_id == User.id),
                and_(Message.sender_id == User.id, Message.receiver_id == user_id)
            )
        )
        .group_by(User.id)
        .order_by(desc("last_message_time"))
    )

    result = await db.execute(query)
    chats = result.all()

    return [
        {
            "id": c.id,
            "username": c.username,
            "name": c.name,
            "profile_pic": c.profile_pic,
            "last_message_time": c.last_message_time
        } for c in chats
    ]


@router.get("/history/{other_user_id}")
async def get_chat_history(
    other_user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user["user_id"]
    query = (
        select(Message)
        .where(
            or_(
                and_(Message.sender_id == user_id, Message.receiver_id == other_user_id),
                and_(Message.sender_id == other_user_id, Message.receiver_id == user_id)
            )
        ).order_by(Message.created_at.asc())
    )

    result = await db.execute(query)
    messages = result.scalars().all()

    return messages

@router.get("/history/group/{group_id}")
async def get_group_chat_history(
    group_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = (
        select(Message)
        .where(Message.group_id == group_id)
        .order_by(Message.created_at.asc())
    )

    result = await db.execute(query)
    messages = result.scalars().all()

    return messages

@router.websocket("/ws/chat")
async def chat_socket(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    token = websocket.query_params.get("token")
    user = await get_current_user_ws(websocket, db, token)
    if not user:
        await websocket.send_json({"error": "Authentication failed"})
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    user_id = user.id
    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
            except json.JSONDecodeError:
                continue # Skip malformed messages

            # Database logic is correct
            new_msg = Message(
                sender_id=user_id,
                receiver_id=message_data.get("receiver_id"),
                group_id=message_data.get("group_id"),
                content=message_data["content"]
            )
            db.add(new_msg)
            await db.commit()
            await db.refresh(new_msg)

            payload = {
                "id": new_msg.id,
                "sender_id": user_id,
                "content": new_msg.content,
                "created_at": str(new_msg.created_at),
                "group_id": new_msg.group_id,
            }

            if new_msg.group_id:
                res = await db.execute(
                    select(GroupMembers.user_id).where(GroupMembers.group_id == new_msg.group_id)
                )
                member_ids = res.scalars().all()
                await manager.broadcast_to_group(payload, member_ids)
            else:
                # Send to receiver AND sender (so sender sees their message on all devices)
                await manager.send_personal_message(payload, new_msg.receiver_id)
                await manager.send_personal_message(payload, user_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)