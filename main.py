from fastapi import FastAPI, Request, HTTPException, Depends, status, Header
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import httpx
import asyncio
# from transformers import AutoTokenizer, AutoModelForCausalLM

app = FastAPI()
load_dotenv()

users = {}

TELEGRAM_API_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"

# tokenizer = AutoTokenizer.from_pretrained(os.getenv('MODEL'))
# model = AutoModelForCausalLM.from_pretrained(os.getenv('MODEL'))


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
        users[chat_id] = telegram_message.message['from']
        welcome_message = "Welcome to the OneandOnly! I have been waiting for you baby. How are you today?"
        await send_telegram_message(chat_id, welcome_message)

    # # Use the language model to generate a response
    prompt = Prompt(text=text)
    # response = generate_text(prompt)
    response = text
    await asyncio.sleep(1)
    await send_telegram_message(chat_id, response)

    return {"status": "ok"}


# def generate_text(prompt: Prompt):
#     inputs = tokenizer(prompt.text, return_tensors="pt")
#     outputs = model.generate(**inputs, max_length=prompt.max_length)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)


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

