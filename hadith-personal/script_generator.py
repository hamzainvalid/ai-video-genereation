import random
from transformers import pipeline
import uuid
import os
import openai
from openai import OpenAI
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Optional: You can replace these with your own themes
# TOPIC_POOL = [
#     "The future of artificial intelligence",
#     "Why space travel matters",
#     "5 mind-blowing science facts",
#     "Life lessons from animals",
#     "How the brain rewires itself",
#     "Weirdest facts about the ocean",
#     "Secrets behind the pyramids"
# ]


HED_GEM_API = os.getenv('HED_GEM_API')

def generate_ai_script():

    genai.configure(api_key=HED_GEM_API)

    # Initialize the model
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

    title_prompt = 'Create a different topic name of no more than 4 words from a different Hadith, provide only the text'
    response_title = model.generate_content(title_prompt)
    title = response_title.text
    print(f'title created: {title}')

    # Create the prompt
    prompt = f"Give me a Hadith from Sahih Al Bukhari related to {title}, provide only the text. In the end, mention Subscribe and share for more Hadith Everyday"

    # Generate the content
    response = model.generate_content(prompt)
    script = response.text

    script_id = str(uuid.uuid4())[:8]
    script_filename = f"script_{script_id}.txt"

    with open(script_filename, "w", encoding="utf-8") as f:
        f.write(script)

    print(f"✅ Script saved to: {script_filename}")
    return script, title






