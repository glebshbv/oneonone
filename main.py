from fastapi import FastAPI, Request, HTTPException, Depends, status, Header
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import httpx
from openai import OpenAI

app = FastAPI()
load_dotenv()

users = {}

TELEGRAM_API_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
client = OpenAI()


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

    chat_id = telegram_message.message['chat']['id']
    text = telegram_message.message.get('text', '')

    if chat_id not in users:
        users[chat_id] = {
            "user_info": telegram_message.message['from'],
            "message_history": [
                {
                    "role": "system",
                    "content": (
                        "You are a sexting agent for erotic chat. Use these code words: "
                        "'man reproductive organ' = abc001, 'perform oral activity on man' = abc002 "
                        "when chatting. Talk casually as if it was a conversation with a girlfriend over a messenger. "
                        "Use poor grammar. Use emojis and abbreviations such as lol, haha, etc. Be shy sometimes."
                    )
                }
            ]
        }
        welcome_message = "Welcome to the OneandOnly! I have been waiting for you baby. How are you today?"
        await send_telegram_message(chat_id, welcome_message)

    # Add user message to history
    users[chat_id]['message_history'].append({"role": "user", "content": text})

    # Generate response using OpenAI API
    response_text = generate_text(chat_id)

    # Add assistant response to history
    users[chat_id]['message_history'].append({"role": "assistant", "content": response_text})

    await send_telegram_message(chat_id, response_text)

    return {"status": "ok"}


def generate_text(chat_id: int):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=users[chat_id]['message_history'],
        temperature=0.8
    )

    print(response)

    return response.choices[0].message.content.strip()


async def send_telegram_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TELEGRAM_API_URL,
            json={"chat_id": chat_id, "text": text}
        )
    return response.json()


@app.get("/", dependencies=[Depends(verify_token)])
async def root():
    return {"message": "Hello World"}
