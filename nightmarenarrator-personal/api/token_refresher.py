import os
import json
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv


load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = None

    # Try to load token from env or fallback to file
    token_data = os.getenv("TOKEN_SECRET_NN")
    if token_data:
        creds = Credentials.from_authorized_user_info(json.loads(token_data), SCOPES)
        print('Token found in env')
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        print('Token found in path')

    # Refresh or create new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            # Load client_secret.json from env or file
            client_secret_data = os.getenv("CLIENT_SECRET_NN")
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

            os.remove('temp_client_secret.json')


get_authenticated_service()