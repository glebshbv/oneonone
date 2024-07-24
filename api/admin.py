import os
from dotenv import load_dotenv
import fastapi
from fastapi import Header, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from typing import Optional, List

from db.database import get_db
from schemas.user import User, UserCreate
from api.utils.users import get_user, get_users, create_user, get_user_by_chat_id

router = fastapi.APIRouter()
load_dotenv()


def verify_token(x_token: str = Header(...)):
    if x_token != os.getenv('API_TOKEN'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


@router.get("/users", response_model=List[User], dependencies=[Depends(verify_token)])
async def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("/users", dependencies=[Depends(verify_token)])
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_chat_id(db=db, chat_id=user.chat_id):
        raise HTTPException(status_code=400, detail="User is already registered")
    user = create_user(db=db, user=user)
    if user is None:
        raise HTTPException(status_code=401, detail="Failed to create user")
    return user
