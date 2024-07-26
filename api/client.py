import os
from dotenv import load_dotenv
import fastapi
from fastapi import FastAPI, Request, HTTPException, Header, Depends
from starlette import status
from sqlalchemy.orm import Session
from db.database import get_db

from services.eleven_labs_handler import ElevenLabsHandler

from services.telegram_handler import TelegramHandler
from services.message_handler import MessageHandler
from services.openai_handler import OpenAIHandler

router = fastapi.APIRouter()
load_dotenv()


def verify_token(x_token: str = Header(...)):
    if x_token != os.getenv('API_TOKEN'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def verify_telegram_token(x_telegram_bot_api_secret_token: str = Header(...)):
    if x_telegram_bot_api_secret_token != os.getenv('TELEGRAM_WEBHOOK_TOKEN'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized",
        )


@router.get("/", dependencies=[Depends(verify_token)])
async def root():
    return {"message": "Hello World"}


@router.post("/webhook", dependencies=[Depends(verify_telegram_token)])
async def handle_webhook(request: Request,
                         db: Session = Depends(get_db),
                         ):

    data = await request.json()
    user_id = await MessageHandler(telegram_message=data, db=db).receive_message()
    print(user_id)
    response_text = await OpenAIHandler(user_id=user_id, db=db).messages()
    print(response_text)
    file_path = await ElevenLabsHandler().convert_text_to_ogg_and_set_link(text=response_text)
    print(file_path)
    try:
        await TelegramHandler(db=db, user_id=user_id).send_voice_message(voice_file_url=file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send default voice message: {str(e)}")

    return {"status": "ok"}