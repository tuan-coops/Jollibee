from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.membership import Membership
from schemas import MembershipBase, MembershipResponse
from datetime import datetime

router = APIRouter()

@router.post("/membership/join", response_model=MembershipResponse)
def join_forum(request: MembershipBase, db: Session = Depends(get_db)):
    existing = db.query(Membership).filter(
        Membership.user_id == request.user_id,
        Membership.forum_id == request.forum_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Người dùng đã tham gia forum này")

    new_member = Membership(
        user_id=request.user_id,
        forum_id=request.forum_id,
        role=request.role,
        joined_at=datetime.utcnow()
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

@router.get("/membership/{forum_id}")
def get_members(forum_id: int, db: Session = Depends(get_db)):
    members = db.query(Membership).filter(Membership.forum_id == forum_id).all()
    return members
