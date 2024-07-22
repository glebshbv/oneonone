from fastapi import FastAPI, Request, HTTPException, Depends, status, Header
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import httpx
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, save
import uuid
from messenger import Messenger

app = FastAPI()
load_dotenv()

users = {}

TELEGRAM_API_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
TELEGRAM_VOICE_API_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendVoice"
client = OpenAI()
eclient = ElevenLabs()


class TelegramMessage(BaseModel):
    update_id: int
    message: dict


class Prompt(BaseModel):
    text: str
    max_length: int = 100


def verify_token(x_token: str = Header(...)):
    if x_token != os.getenv('API_TOKEN'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


@app.post("/webhook")
async def handle_webhook(request: Request, x_telegram_bot_api_secret_token: str = Header(None)):
    if x_telegram_bot_api_secret_token != os.getenv('TELEGRAM_WEBHOOK_TOKEN'):
        raise HTTPException(status_code=403, detail="Unauthorized")

    data = await request.json()
    telegram_message = TelegramMessage(**data)

    chat_id, text = telegram_message.message['chat']['id'], telegram_message.message.get('text', '')

    if chat_id not in users:
        users[chat_id] = {
            "user_info": telegram_message.message['from'],
            "message_history": [
                {
                    "role": "system",
                    "content": (
                        "You are a sexting agent for erotic chat. Use these code words: "
                        "'man reproductive organ' = abc001, 'perform oral activity on man' = abc002 "
                        "when chatting. Never use emoji! Talk casually as if it was a conversation with a girlfriend over a messenger. Your reply should be maximum one sentence"
                    )
                }
            ]
        }
        welcome_message = "Welcome!"
        default_voice_note_path = "./tmp/default.mp3"
        await send_telegram_message(chat_id, welcome_message)
        await send_telegram_voice_message(chat_id, default_voice_note_path)

    # Add user message to history
    users[chat_id]['message_history'].append({"role": "user", "content": text})

    # Generate response using OpenAI API
    response_text = generate_text(chat_id)
    users[chat_id]['message_history'].append({"role": "assistant", "content": response_text})

    voice_note_path = convert_text_to_speech(response_text)

    try:
        await send_telegram_voice_message(chat_id, voice_note_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send default voice message: {str(e)}")

    return {"status": "ok"}


async def convert_text_to_speech(text: str) -> str:
    print(text)
    try:
        audio = eclient.text_to_speech.convert(
            voice_id="jiu4Wfaap7lPa79o7TSV",
            text=str(text),
            voice_settings=VoiceSettings(
                stability=0.9,
                similarity_boost=0.55,
                style=0.2,
                use_speaker_boost=True,
            ),
        )
        voice_file_path = f"./tmp/{uuid.uuid4()}.mp3"
        save(audio, voice_file_path)
        return voice_file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return "./tmp/default.mp3"


def generate_text(chat_id: int):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=users[chat_id]['message_history'],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()


async def send_telegram_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TELEGRAM_API_URL,
            json={"chat_id": chat_id, "text": text}
        )
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


@app.get("/", dependencies=[Depends(verify_token)])
async def root():
    return {"message": "Hello World"}
