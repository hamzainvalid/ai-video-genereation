import random


voices = [
        'tQ4MEZFJOzsahSEEZtHK',
        'EXAVITQu4vr4xnSDxMaL',
        'D5TZi5xGzBoJjBT4GONI',
        '1rnYMVDXZksVr6x7pZPX'
    ]

voice_id =  random.choice(voices)

print(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}")