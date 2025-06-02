import os
import subprocess
import uuid
from gtts import gTTS
#from image_generator import download_image_from_pexels
from script_generator import generate_ai_script
from video_generator import download_pexels_videos
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from moviepy.config import change_settings
import openai
import requests
#from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

#os.environ['IMAGE_MAGICK_BINARY'] = r'C:\\Program Files\\ImageMagick-7.X.X-Q16\\magick.exe'
change_settings({"IMAGEMAGICK_BINARY": r'C:\\Program Files\\ImageMagick-7.X.X-Q16\\magick.exe'})


NN_EL_API = os.getenv('NN_EL_API')
#TG_EL_TTS_API = os.getenv('TG_EL_TTS_API')
#RSS_API = os.getenv('RSS_API')
#PERSONAL_EL_API = os.getenv('PERSONAL_EL_API')



topic = 'HORROR STORY NIGHTMARE'



def generate_script():
    global script
    global title
    script, title = generate_ai_script(topic)
    return script, title


# def text_to_speech(script_text, output_path):
#     tts = gTTS(text=script_text, lang='en')
#     tts.save(output_path)

def generate_tts(script_text, output_path, speed=1.25):
    api_key = NN_EL_API
    voice_id = 'EXAVITQu4vr4xnSDxMaL'  # Default voice, change as needed

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        },
        json={
            "text": script_text,
            "model_id": "eleven_monolingual_v1"
        }
    )
    # API_KEY = RSS_API
    # text = script_text
    #
    # params = {
    #     'key': API_KEY,
    #     'hl': 'en-us',
    #     'src': text,
    #     'r': '0',
    #     'c': 'mp3',
    #     'f': '44khz_16bit_stereo'
    # }
    #
    # response = requests.get('https://api.voicerss.org/', params=params)

    # if response.status_code == 200:
    #     with open('output.mp3', 'wb') as f:
    #         f.write(response.content)
    #     print("Audio saved as output.mp3")
    # else:
    #     print("Error:", response.text)

    if response.status_code == 200:
        raw_path = output_path.replace(".mp3", "_raw.mp3")
        with open(raw_path, 'wb') as f:
            f.write(response.content)
        print('TTS audio generated')

        # Use ffmpeg to speed up audio
        # -filter:a "atempo=2.0" speeds up audio 2x
        # atempo supports 0.5 to 2.0, so for >2x speeds chain filters

        # Calculate filter string:
        speed_filter = []
        remaining_speed = speed
        while remaining_speed > 2.0:
            speed_filter.append("atempo=2.0")
            remaining_speed /= 2.0
        speed_filter.append(f"atempo={remaining_speed}")
        filter_str = ",".join(speed_filter)

        cmd = [
            "ffmpeg",
            "-y",  # overwrite output
            "-i", raw_path,
            "-filter:a", filter_str,
            "-vn",
            output_path
        ]

        subprocess.run(cmd, check=True)
        print(f"Audio speed adjusted to {speed}x")

        os.remove(raw_path)
        return output_path
    else:
        raise Exception("TTS failed: " + response.text)


# def combine_videos(video_paths, output_path='final_video.mp4'):
#     with open('temp_list.txt', 'w') as f:
#         for path in video_paths:
#             f.write(f"file '{os.path.abspath(path)}'\n")
#
#     subprocess.run([
#         'ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'temp_list.txt',
#         '-c', 'copy', output_path
#     ], check=True)
#     return output_path

# def combine_videos(video_paths, output_path='final_video.mp4', max_duration=20):
#     with open('temp_list.txt', 'w') as f:
#         for path in video_paths:
#             f.write(f"file '{os.path.abspath(path)}'\n")
#
#     # Combine and trim final output to 20 seconds
#     subprocess.run([
#         'ffmpeg', '-y',
#         '-f', 'concat', '-safe', '0',
#         '-i', 'temp_list.txt',
#         '-t', str(max_duration),
#         '-c:v', 'libx264',
#         '-pix_fmt', 'yuv420p',
#         output_path
#     ], check=True)
#
#     os.remove('temp_list.txt')
#     print('videos compiled and final video created')# Clean up
#     return output_path

def combine_videos(video_paths, output_path='final_video.mp4', total_duration=20):
    clips = []

    # Filter and load clips
    for path in video_paths:
        try:
            clip = VideoFileClip(path).without_audio()

            # Format to vertical 9:16
            w, h = clip.size
            target_ratio = 9 / 16
            current_ratio = w / h

            if current_ratio > target_ratio:
                new_width = int(h * target_ratio)
                x_center = w // 2
                clip = clip.crop(x_center=x_center, width=new_width)
            elif current_ratio < target_ratio:
                new_height = int(w / target_ratio)
                y_center = h // 2
                clip = clip.crop(y_center=y_center, height=new_height)

            clip = clip.resize((1080, 1920))
            clips.append(clip)

        except Exception as e:
            print(f"Skipping {path}: {e}")

    if not clips:
        raise Exception("No valid clips to combine.")

    per_clip_duration = total_duration / len(clips)
    final_clips = []

    for clip in clips:
        if clip.duration >= per_clip_duration:
            final_clips.append(clip.subclip(0, per_clip_duration))
        else:
            loop_count = int(per_clip_duration // clip.duration) + 1
            looped = concatenate_videoclips([clip] * loop_count)
            final_clips.append(looped.subclip(0, per_clip_duration))

    final_video = concatenate_videoclips(final_clips, method="compose")
    final_video.write_videofile(output_path, codec='libx264', fps=24)

    return output_path

# def generate_video_with_audio(topic, audio_path, output_path, duration=10, resolution=(1280, 720)):
#     download_image_from_pexels(topic, "static_background.png")
#     command = [
#         r"C:\ffmpeg\bin\bin\ffmpeg.exe",  # replace with your actual path to ffmpeg
#         "-loop", "1",
#         "-i", "static_background.png",
#         "-i", audio_path,
#         "-c:v", "libx264",
#         "-tune", "stillimage",
#         "-c:a", "aac",
#         "-b:a", "192k",
#         "-shortest",
#         output_path
#     ]
#     subprocess.run(command, check=True)

def add_audio_and_subtitles(video_path, audio_path, script_text, output_path='final_video_with_audio.mp4'):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Calculate how many times we need to loop the video
    loops = int(audio.duration // video.duration) + 1

    # Repeat video and trim to match audio duration
    video_looped = concatenate_videoclips([video] * loops).subclip(0, audio.duration)

    # Set audio
    final = video_looped.set_audio(audio)


    # video = VideoFileClip(video_path)
    # audio = AudioFileClip(audio_path).set_duration(video.duration)
    # video = video.set_audio(audio)

    #subtitle = TextClip(script_text, fontsize=24, color='white', bg_color='black', size=video.size, method='caption')
    #subtitle = subtitle.set_duration(video.duration).set_position(('center', 'bottom'))

    #final = CompositeVideoClip(video)
    final.write_videofile(output_path, codec='libx264', audio_codec='aac')
    print('video with subtitles success')
    return output_path

def local_pipeline():
    generate_script()
    script_text = script
    video_title = title
    temp_id = str(uuid.uuid4())

    audio_path = f'temp_{temp_id}_audio.mp3'
    video_path = f'temp_{temp_id}_video.mp4'

    paths = download_pexels_videos(video_title)
    #text_to_speech(script_text, audio_path)
    generate_tts(script_text, audio_path)
    combine_videos(paths)
    #generate_video_with_audio(script_text, audio_path, video_path)
    add_audio_and_subtitles('final_video.mp4', audio_path, script_text, video_path)


    print(f"Generated video saved to: {video_path}")
    return video_path, video_title

# if __name__ == '__main__':
#     local_pipeline()
