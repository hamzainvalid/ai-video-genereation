import os
import requests
from dotenv import load_dotenv
import random

load_dotenv()

TEST_EL_API = os.getenv('TEST_EL_API')
NN_EL_API = os.getenv('NN_EL_API')
PERSONAL_EL_API = os.getenv('PERSONAL_EL_API')
EXTRA_EL_API_1 = os.getenv('EXTRA_EL_API_1')
HED_EL_API = os.getenv('HED_EL_API')

voices_list = [
        'tQ4MEZFJOzsahSEEZtHK',
        'D5TZi5xGzBoJjBT4GONI',
        'pjcYQlDFKMbcOUp6F5GD'
    ]


def testing_api(voice):
    api_key = HED_EL_API
    voice_id =  voice
    print(f'voice selected {voice_id}')

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

testing_api('aCChyB4P5WEomwRsOKRh')