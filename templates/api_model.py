import openai

openai.api_key = "YOUR_API_KEY"  # store this securely!

def generate_text_api(prompt):
    print("Using API model")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()
