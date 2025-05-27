import requests
import os

PEXELS_API_KEY = 'lsMpm0KixlEtDB5n8TB587kWgFjxUZ9xmcc9LM0W8PjU6p8JPTRfb8VX'  # Replace with your actual API key


from PIL import Image
import requests
from io import BytesIO


def download_image_from_pexels(prompt, output_path='ai_bg.jpg'):
    headers = {
        'Authorization': PEXELS_API_KEY
    }
    params = {
        'query': prompt,
        'per_page': 1
    }
    response = requests.get('https://api.pexels.com/v1/search', headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['photos']:
            image_url = data['photos'][0]['src']['original']
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Open image from memory
                img = Image.open(BytesIO(image_response.content)).convert('RGB')

                # Resize to fit 1080x1920 (shorts) while maintaining aspect ratio
                target_size = (1080, 1920)
                img.thumbnail(target_size, Image.LANCZOS)

                # Create black background canvas
                background = Image.new('RGB', target_size, (0, 0, 0))

                # Paste resized image centered on black background
                x = (target_size[0] - img.size[0]) // 2
                y = (target_size[1] - img.size[1]) // 2
                background.paste(img, (x, y))

                # Save result
                background.save(output_path)
                print(f"Shorts-compatible image saved as {output_path}")
                return output_path
            else:
                print("Failed to download the image.")
        else:
            print("No images found for the given prompt.")
    else:
        print(f"Failed to fetch images. Status code: {response.status_code}")

    return None

