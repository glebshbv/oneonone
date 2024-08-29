import asyncio
import os
import uuid
import io
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, save
import boto3
from pydub import AudioSegment
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
        self.default_audio_name = 'default1.ogg'
        self.audio_name = None
        self.uuid = str(uuid.uuid4().hex)

    async def default_audio_downloader(self) -> str:
        return await self._set_default_audio_link()

    async def convert_text_to_ogg_and_set_link(self, text: str):
        self.text = text
        try:
            file_path = await self._convert_text_to_speech()
            return await self._upload_file_to_s3(file_path)
        except Exception as e:
            print(f"An error occurred in convert_text_to_ogg_and_set_link: {e}")
            return await self.default_audio_downloader()

    async def _set_default_audio_link(self):
        return f"{os.getenv('CLOUDFLARE_R2_PUBLIC_ENDPOINT_URL')}/{self.default_audio_name}"

    async def _convert_text_to_speech(self) -> str:
        try:
            # Generate audio with ElevenLabs
            audio_generator = self.client.generate(
                text=self.text,
                voice=Voice(
                    voice_id=os.getenv('ELEVEN_VOICE_ID'),
                    settings=VoiceSettings(stability=0.9,
                                           similarity_boost=0.55,
                                           style=0.25,
                                           use_speaker_boost=True)
                ),
                stream=True
            )
            # Collect audio data
            audio_data = b''.join(chunk for chunk in audio_generator)

            # Save as MP3 first
            mp3_file_path = f"./tmp/{self.uuid}.mp3"
            with open(mp3_file_path, "wb") as f:
                f.write(audio_data)

            # Convert to OGG using ffmpeg directly
            ogg_file_path = f"./tmp/{self.uuid}.ogg"
            await asyncio.to_thread(os.system, f"ffmpeg -i {mp3_file_path} -c:a libopus -b:a 24k {ogg_file_path}")

            # Check file size and reduce bitrate if necessary
            file_size = os.path.getsize(ogg_file_path)
            if file_size > 1_000_000:  # 1MB in bytes
                await asyncio.to_thread(os.system, f"ffmpeg -i {mp3_file_path} -c:a libopus -b:a 16k {ogg_file_path}")

            self.audio_name = f"{self.uuid}.ogg"
            # Remove the temporary MP3 file
            os.remove(mp3_file_path)
            print(f"Converted {self.audio_name} with path {ogg_file_path}")
            return ogg_file_path

        except Exception as e:
            print(f"An error occurred: {e}")
            return await self.default_audio_downloader()

    async def _upload_file_to_s3(self, file_path: str):
        try:
            with open(file_path, 'rb') as file:
                await asyncio.to_thread(self.s3_client.upload_fileobj, file, self.bucket_name, f"{self.uuid}.ogg")
            os.remove(file_path)
            return f"{os.getenv('CLOUDFLARE_R2_PUBLIC_ENDPOINT_URL')}/{self.audio_name}"

        except Exception as e:
            print(f"An error occurred while uploading to S3: {e}")
            return self._set_default_audio_link()