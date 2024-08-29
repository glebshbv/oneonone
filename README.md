
# **Custom Voice Telegram Bot**

This bot leverages the power of OpenAI for natural language understanding and ElevenLabs for generating custom voices. The bot allows users to create and manage conversational agents with personalized voices, maintaining context throughout the conversation.

## **Table of Contents**
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Features](#features)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## **Installation**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/custom-voice-telegram-bot.git
   cd custom-voice-telegram-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables** (see [Environment Variables](#environment-variables) below).

4. **Run the bot:**
   ```bash
   python main.py
   ```

5. **The bot comes with Docker and Docker Compose configured.**
 ***Just run this command inside folder:***
```bash
docker-compose up --build
```

## **Environment Variables**

You need to create a `.env` file in the root directory of your project to store the following environment variables:

- **`API_TOKEN`**: API token to access /admin APIs.
- **`TELEGRAM_BOT_TOKEN`**: Your Telegram bot token obtained from BotFather.
- **`TELEGRAM_WEBHOOK_TOKEN`**: Telegram Webhook token (configure webhooks in advance)
- **`CHATS`**: A comma-separated list of Telegram chat IDs where the bot will send messages. Example: `CHATS="123456789,987654321"`
- **`OPENAI_API_KEY`**: Your API key for OpenAI.
- **`ELEVEN_API_KEY`**: Your API key for ElevenLabs.
- **`ELEVEN_VOICE_ID`**: Your ElevenLabs Voice ID.
- **`CLOUDFLARE_R2_ACCESS_KEY_ID`**: Cloudflare R2 Config
- **`CLOUDFLARE_R2_SECRET_ACCESS_KEY`**: Cloudflare R2 Config
- **`CLOUDFLARE_R2_BUCKET_NAME`**: Cloudflare R2 Config
- **`CLOUDFLARE_R2_ENDPOINT_URL`**: Cloudflare R2 Config
- **`CLOUDFLARE_R2_PUBLIC_ENDPOINT_URL`**: Cloudflare R2 Config
- **`CLOUDFLARE_R2_REGION`**: Cloudflare R2 Config
- **`DATABASE_URL`**: Postgres DB String
- **`DEFAULT_PROMPT`**: Your starting prompt for conversation



Example `.env` file:
```dotenv
API_TOKEN=super-token

TELEGRAM_BOT_TOKEN=super-token
TELEGRAM_WEBHOOK_TOKEN=super-token
OPENAI_API_KEY=super-token
HOST=host
ELEVEN_API_KEY=super-token
ELEVEN_VOICE_ID=super-id

CLOUDFLARE_R2_ACCESS_KEY_ID=super-token
CLOUDFLARE_R2_SECRET_ACCESS_KEY=super-token
CLOUDFLARE_R2_BUCKET_NAME=super-name
CLOUDFLARE_R2_REGION=apac
CLOUDFLARE_R2_ENDPOINT_URL=your-url
CLOUDFLARE_R2_PUBLIC_ENDPOINT_URL=public-endpoint

DATABASE_URL=postgresql+psycopg2://username:password@host/db

DEFAULT_PROMPT=default-prompt

```

## **Usage**

- Start a conversation with the bot in Telegram.
- The bot will respond to your messages, maintaining the context of the conversation.
- Voice responses are generated using ElevenLabs, providing a custom voice for the bot.
- You can customize the bot's behavior and voice through the OpenAI and ElevenLabs integrations.

## **Features**

- **Conversational AI**: Uses OpenAI to generate context-aware responses.
- **Custom Voices**: Uses ElevenLabs to create personalized voices for the bot.
- **Contextual Memory**: The bot maintains the context of the conversation.
- **Multi-Chat Support**: Can be configured to send messages to multiple Telegram chats.

## **How It Works**

1. **Message Handling**: The bot receives messages via the Telegram API.
2. **Natural Language Processing**: OpenAI processes the text to generate an appropriate response.
3. **Voice Generation**: ElevenLabs converts the text response into audio using a custom voice.
4. **Message Delivery**: The bot sends the response back to the user in both text and voice formats, maintaining conversation continuity.

## **Contributing**

Contributions are welcome! Please fork this repository and submit a pull request.

## **License**

This project is licensed under the MIT License.
