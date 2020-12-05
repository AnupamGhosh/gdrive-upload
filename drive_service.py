import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleDriveService():
  def __init__(self):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    secrets_path = os.path.join(os.path.dirname(__file__), 'secrets')
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    token_path = os.path.join(secrets_path, 'token.pickle')
    if os.path.exists(token_path):
      with open(token_path, 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        secret = os.path.join(secrets_path, 'client_secret.json')
        flow = InstalledAppFlow.from_client_secrets_file(secret, SCOPES)
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open(token_path, 'wb') as token:
        pickle.dump(creds, token)

    self.drive_service = build('drive', 'v3', credentials=creds)

  def get(self):
    return self.drive_service
