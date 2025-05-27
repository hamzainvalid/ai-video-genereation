import random
from transformers import pipeline
import uuid
import os

# Optional: You can replace these with your own themes
TOPIC_POOL = [
    "The future of artificial intelligence",
    "Why space travel matters",
    "5 mind-blowing science facts",
    "Life lessons from animals",
    "How the brain rewires itself",
    "Weirdest facts about the ocean",
    "Secrets behind the pyramids"
]


def generate_ai_script(prompt):
    topic = prompt
    print(f"🧠 Topic: {topic}")

    text_gen = pipeline("text-generation", model="distilgpt2")
    prompt = f"{topic}\n\n"

    script_output = text_gen(prompt, max_length=200, num_return_sequences=1)[0]['generated_text']

    #script_id = str(uuid.uuid4())[:8]
    #script_filename = f"script_{script_id}.txt"

    # with open(script_filename, "w", encoding="utf-8") as f:
    #     f.write(script_output)
    #
    # print(f"✅ Script saved to: {script_filename}")
    return script_output


if __name__ == "__main__":
    generate_ai_script()
