import os
from dotenv import load_dotenv
import httpx
from fastapi import HTTPException
load_dotenv()

TELEGRAM_API_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
TELEGRAM_VOICE_API_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendVoice"


async def send_telegram_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TELEGRAM_API_URL,
            json={"chat_id": chat_id, "text": text}
        )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to send voice message")
    return response.json()


async def send_telegram_voice_message(chat_id: int, voice_file_path: str):
    async with httpx.AsyncClient() as asyncclient:
        with open(voice_file_path, 'rb') as voice_file:
            files = {
                'voice': ('voice.mp3', voice_file, 'audio/mp3')
            }
            data = {
                'chat_id': chat_id
            }
            response = await asyncclient.post(TELEGRAM_VOICE_API_URL, data=data, files=files)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to send voice message")
    return response.json()