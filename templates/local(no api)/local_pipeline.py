import os
import subprocess
import uuid
from gtts import gTTS
from image_generator import download_image_from_pexels
from script_generator import generate_ai_script



def generate_script():
    global script
    script = generate_ai_script('write a catchy script for a video of no more than 20 seconds about finance')
    return script


def text_to_speech(script_text, output_path):
    tts = gTTS(text=script_text, lang='en')
    tts.save(output_path)

def generate_video_with_audio(topic, audio_path, output_path, duration=10, resolution=(1280, 720)):
    download_image_from_pexels(topic, "static_background.png")
    command = [
        r"C:\ffmpeg\bin\bin\ffmpeg.exe",  # replace with your actual path to ffmpeg
        "-loop", "1",
        "-i", "static_background.png",
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]
    subprocess.run(command, check=True)

def local_pipeline():
    script_text = generate_script()
    temp_id = str(uuid.uuid4())

    audio_path = f'temp_{temp_id}_audio.mp3'
    video_path = f'temp_{temp_id}_video.mp4'

    text_to_speech(script_text, audio_path)
    generate_video_with_audio(script_text, audio_path, video_path)

    print(f"Generated video saved to: {video_path}")
    return video_path

if __name__ == '__main__':
    local_pipeline()
