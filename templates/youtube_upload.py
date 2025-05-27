import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from local_pipeline import local_pipeline

video_path = local_pipeline()
# Now pass video_path to your youtube_upload script


# Define the required scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Step 1: Authenticate and build service
def get_authenticated_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
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
        title="Test Upload AI with static bg",
        description="ignore"
    )
