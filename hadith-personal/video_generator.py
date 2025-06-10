import os
import requests
from dotenv import load_dotenv

load_dotenv()

HED_PEXELS_API = os.getenv('HED_PEXELS_API')

def download_pexels_videos(query, num_videos=3, output_dir='videos'):
    os.makedirs(output_dir, exist_ok=True)
    PEXELS_API_KEY = HED_PEXELS_API
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query+' '+'Islam', "per_page": num_videos}

    response = requests.get('https://api.pexels.com/videos/search', headers=headers, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch videos: " + response.text)

    videos = response.json()['videos']
    paths = []
    counter = 0
    for i, video in enumerate(videos):
        url = video['video_files'][0]['link']
        r = requests.get(url)
        fname = f"{output_dir}/clip_{i}.mp4"
        with open(fname, 'wb') as f:
            f.write(r.content)
        paths.append(fname)
        counter+=1
        print(f'video {i} completed')

    return paths

