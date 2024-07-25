import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, save
load_dotenv()

class ElevenLabsHandler:
    def __init__(self):
        self.client = ElevenLabs(api_key=os.getenv('ELEVEN_API_KEY'))


    def main(self):
        ...
