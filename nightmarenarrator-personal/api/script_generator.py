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


NN_GEM_API = os.getenv('NN_GEM_API')

def generate_ai_script(prompt):
    topic = prompt
    # client = OpenAI(api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    #
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You generate short engaging scripts for AI videos that go viral on social media."},
    #         {"role": "user", "content": f"Give me a viral short-form video script about how to anything trending related to {topic}."}
    #     ]
    # )
    #
    # script = response.choices[0].message.content

    genai.configure(api_key=NN_GEM_API)

    # Initialize the model
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

    title_prompt = f'Generate a new catchy topic name of no more than 4 words for {topic}. Provide only one and make sure its not been used and provide only the text'
    response_title = model.generate_content(title_prompt)
    title = response_title.text
    print(f'title created: {title}')

    # Create the prompt
    prompt = f"You generate short engaging scripts for AI videos that go viral on social media of around 20 seconds or so, make sure its not too formal. Give me a viral short-form horror story video script about anything related to {title}. Provide only the script and nothing else. Do not add the emojis, do not add asterisks or anything else like script and scene, don't mention music fades in and upbeat music and all that. In the end say subscribe and like if you wanna hear more horror stories instead of link in bio and all"

    # Generate the content
    response = model.generate_content(prompt)
    script = response.text

    script_id = str(uuid.uuid4())[:8]
    script_filename = f"script_{script_id}.txt"

    with open(script_filename, "w", encoding="utf-8") as f:
        f.write(script)

    print(f"✅ Script saved to: {script_filename}")
    return script, title






