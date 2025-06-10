import os
import requests
from dotenv import load_dotenv

load_dotenv()

TEST_EL_API = os.getenv('TEST_EL_API')
NN_EL_API = os.getenv('NN_EL_API')
PERSONAL_EL_API = os.getenv('PERSONAL_EL_API')
EXTRA_EL_API_1 = os.getenv('EXTRA_EL_API_1')

def testing_api(voice):
    voice = voice
    api_key = EXTRA_EL_API_1
    voice_id =  voice

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        },
        json={
            "text": '',
            "model_id": "eleven_multilingual_v2"
        }
    )

    if response.status_code == 200:
        print('Audio works for api')
    else:
        print('no api for this voice')

testing_api('IRHApOXLvnW57QJPQH2P')