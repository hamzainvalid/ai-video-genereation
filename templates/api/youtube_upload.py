import os
import json
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from local_pipeline import local_pipeline
from dotenv import load_dotenv


load_dotenv()

token_data = os.getenv("TOKEN_SECRET")
client_secret_data = os.getenv("CLIENT_SECRET_KEY")

video_path, video_title = local_pipeline()
# Now pass video_path to your youtube_upload script


# Define the required scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Step 1: Authenticate and build service
def get_authenticated_service():
    creds = None

    # Try to load token from env or fallback to file
    token_data = os.getenv("GOOGLE_TOKEN_JSON")
    if token_data:
        creds = Credentials.from_authorized_user_info(json.loads(token_data), SCOPES)
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Refresh or create new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            # Load client_secret.json from env or file
            client_secret_data = os.getenv("GOOGLE_CLIENT_SECRET_JSON")
            if client_secret_data:
                with open("temp_client_secret.json", "w") as f:
                    f.write(client_secret_data)
                secret_path = "temp_client_secret.json"
            else:
                secret_path = "client_secret.json"

            flow = InstalledAppFlow.from_client_secrets_file(secret_path, SCOPES)
            creds = flow.run_local_server(port=0)

            # Save token locally
            with open("token.json", "w") as token_file:
                token_file.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

# Step 2: Upload video
def upload_video(file_path, title, description, category_id="22", privacy="public"):
    youtube = get_authenticated_service()

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy,
        },
    }

    media_file = MediaFileUpload(file_path, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    response = request.execute()
    print(f"✅ Video uploaded! ID: {response['id']}")

# Step 3: Run it
if __name__ == "__main__":
    upload_video(
        file_path=video_path,  # put a sample 5-10 sec MP4 in your folder
        title=video_title,
        description=""
    )
