from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user
from app.db.database import get_db
from app.schemas.user_schema import User
from app.schemas.contact_schema import Contact

from sqlalchemy import select, or_, and_


router = APIRouter()

@router.get("/search-contacts")
async def get_contacts(
    query: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not query or len(query) < 3:
        return []
    
    blocked_id_query = select(Contact.user_id).where(
        Contact.contact_id == current_user["user_id"],
        Contact.status == "blocked"
    )
    blocked_result = await db.execute(blocked_id_query)
    blocked_ids = blocked_result.scalars().all()
    
    sql_query = (
        select(User.id, User.username, User.name, User.profile_pic, User.bio)
        .where(
            and_(
                or_(
                    User.username.ilike(f"%{query}"),
                    User.name.ilike(f"%{query}")
                ),
                User.id != current_user["user_id"],
                User.id.notin_(blocked_ids) if blocked_ids else True
            )
        ).limit(10)
    )

    result = await db.execute(sql_query)
    students = result.all()

    return [
        {
            "id": s.id,
            "username": s.username,
            "name": s.name,
            "profile_pic": s.profile_pic,
            "bio": s.bio
        } for s in students
    ]

@router.post("/add-contact/{target_contact_id}")
async def add_contact(
    target_contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: AsyncSession = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    check_query = select(Contact).where(
        Contact.user_id == user_id,
        Contact.contact_id == target_contact_id
    )

    res = await db.execute(check_query)
    existing_contact = res.scalars().first()
    if not existing_contact:
        new_contact = Contact(
            user_id=user_id,
            contact_id=target_contact_id,
            status="active"
        )
        db.add(new_contact)
        await db.commit()
        return {"message": "Contact added successfully"}

    return {"message": "Contact already exists"}


@router.get("/my-contacts")
async def get_my_contacts(
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    
    # Get all users from the contacts table where status is 'active'
    query = (
        select(User)
        .join(Contact, User.id == Contact.contact_id)
        .where(Contact.user_id == user_id, Contact.status == "active")
    )
    
    result = await db.execute(query)
    contacts =  result.scalars().all()
    return [
        {
            "id": c.id,
            "username": c.username,
            "name": c.name,
            "profile_pic": c.profile_pic,
            "bio": c.bio
        } for c in contacts
    ]