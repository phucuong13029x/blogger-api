from app import *
from app._config import authen
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def _access_tokken(cer_path, token_path):
    SCOPES = ["https://www.googleapis.com/auth/blogger"]
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cer_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return creds.token

class blogger_sdk:
    def __init__(self, id, key=authen['key']):
        self.id           = id
        self.url          = f"https://blogger.googleapis.com/v3/blogs/{self.id}/posts"
        self.access_token = _access_tokken(authen['cer'], authen['token'])
        self.key          = key
        self.headers      = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        print(self.headers)

    def _req(self, url, data):
        try:
            response = requests.post(url, headers=self.headers, json=data)
            return response.text
        except requests.HTTPError as e:
            error = json.loads(e.args[1])['error']['message']
            return error
        
    def _create_post(self, title:str, content:str):
        print(title)
        try:
            data = {
                "kind": "blogger#post",
                "blog": {
                    "id": self.id
                },
                "title": title,
                "content": content
            }
            result = self._req(url=self.url, data=data)
            return result
        except Exception as e:
            print(e)
            return False