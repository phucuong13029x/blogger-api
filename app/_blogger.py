from app import *
from app._config import authen
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import webbrowser



def _access_tokken(cer_path, token_path):
    SCOPES = [
        "https://www.googleapis.com/auth/blogger",
        "https://www.googleapis.com/auth/drive.file"
    ]
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
    return creds

class blogger_sdk:
    def __init__(self, id, key=authen['key']):
        self.id           = id
        self.api_name     = 'drive'
        self.api_version  = 'v3'
        self.url          = f"https://blogger.googleapis.com/v3/blogs/{self.id}/posts"
        self.credentials  = _access_tokken(authen['cer'], authen['token'])
        self.access_token = self.credentials.token
        self.service      = build(self.api_name, self.api_version, credentials=self.credentials)
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

    def upload_image(self, file_path, title='', caption=''):
        try:
            media = MediaFileUpload(file_path, mimetype='image/*')
            request = self.service.blogs().get(blogId=self.id, view='ADMIN')
            blog = request.execute()
            body = {
                'kind': 'blogger#post',
                'blog': blog,
                'title': title,
                'content': caption,
                'images': [{
                    'url': file_path
                }]
            }
            post = blogger_service.posts().insert(blogId=self.id, body=body).execute()
            print(post)
            image_url = post['images'][0]['url']
            return image_url
        except Exception as e:
            print(e)
            return False