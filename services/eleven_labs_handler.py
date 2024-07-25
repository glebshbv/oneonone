import os
import uuid

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, save
import boto3
load_dotenv()


class ElevenLabsHandler:
    def __init__(self):
        self.client = ElevenLabs(api_key=os.getenv('ELEVEN_API_KEY'))
        self.s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv('CLOUDFLARE_R2_ENDPOINT_URL'),
            aws_access_key_id=os.getenv('CLOUDFLARE_R2_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('CLOUDFLARE_R2_SECRET_ACCESS_KEY'),
            region_name=os.getenv('CLOUDFLARE_R2_REGION')
        )
        self.text = None
        self.bucket_name = os.getenv('CLOUDFLARE_R2_BUCKET_NAME')
        self.default_audio_name = 'default.mp3'
        self.audio_name = None
        # self.uuid = str(uuid.uuid4().hex)
        self.uuid = None


    def converter(self):
        ...

    def default_audio_downloader(self) -> str:
        return self._set_default_audio_link()

    def _convert_text_to_mp3(self):
        ...

    def _set_default_audio_link(self):
        return f"{os.getenv('CLOUDFLARE_R2_PUBLIC_ENDPOINT_URL')}/{self.default_audio_name}"

    # def convert_text_to_speech(text: str) -> str:
    #     try:
    #         audio = eclient.generate(
    #             text=str(text),
    #             voice=Voice(
    #                 voice_id='jiu4Wfaap7lPa79o7TSV',
    #                 settings=VoiceSettings(stability=0.9,
    #                                        similarity_boost=0.55,
    #                                        style=0.25,
    #                                        use_speaker_boost=True)
    #             ),
    #         )
    #
    #         voice_file_path = f"./tmp/{uuid.uuid4()}.mp3"
    #         save(audio, voice_file_path)
    #         return voice_file_path
    #
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         return "./tmp/default.mp3"