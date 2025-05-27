import config
from local_model import generate_text_local
from api_model import generate_text_api

def generate_text(prompt):
    if config.USE_API:
        return generate_text_api(prompt)
    else:
        return generate_text_local(prompt)

if __name__ == "__main__":
    prompt = "Make an examplary random video of no more than 10 seconds"
    response = generate_text(prompt)
    print("Response:", response)
