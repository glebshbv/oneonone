import os
from dotenv import load_dotenv
import fastapi
from fastapi import Header, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from typing import Optional, List

from db.database import get_db
from schemas.user import User, UserCreate
from schemas.message_history import MessageHistory, MessageHistoryCreate, MessageHistoryBase
from api.utils.users import get_user, get_users, create_user, get_user_by_chat_id
from api.utils.message_history import get_message_history, create_message_history, get_message_history_by_user_id

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

# @router.patch("/users", dependencies=[Depends(verify_token)])
# async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
#     if get_user_by_chat_id(db=db, chat_id=user.chat_id):
#         raise HTTPException(status_code=400, detail="User is already registered")
#     user = create_user(db=db, user=user)
#     if user is None:
#         raise HTTPException(status_code=401, detail="Failed to create user")
#     return user


@router.get("/message_history", response_model=List[MessageHistory], dependencies=[Depends(verify_token)])
async def read_message_history(db: Session = Depends(get_db)):
    message_history = get_message_history(db=db)
    return message_history


@router.get("/message_history/{user_id}", response_model=List[MessageHistoryBase], dependencies=[Depends(verify_token)])
async def read_message_history_by_user_id(user_id: int, db: Session = Depends(get_db)):
    message_history = get_message_history_by_user_id(db=db, user_id=user_id)
    if not message_history:
        raise HTTPException(status_code=404, detail="Message history not found")
    return message_history


@router.post("/message_history", dependencies=[Depends(verify_token)])
async def create_message(message_history: MessageHistoryCreate, db: Session = Depends(get_db)):
    message = create_message_history(db=db, message_history=message_history)
    if message is None:
        raise HTTPException(status_code=401, detail="Failed to create message")
    return message