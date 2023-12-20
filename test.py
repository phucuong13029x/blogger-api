from PIL import Image

def convert_to_webp(input_image_path, output_image_path):
    # Open the image file
    image = Image.open(input_image_path)

    # Convert the image to WebP format
    image.save(output_image_path, 'webp')

# Example usage
input_image_path = 'input_image.jpg'
output_image_path = 'output_image.webp'

convert_to_webp(input_image_path, output_image_path)







from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Constants
SCOPES = ['https://www.googleapis.com/auth/blogger']
CLIENT_SECRET_FILE = 'client_secret.json'  # Replace with your client secret file
API_NAME = 'blogger'
API_VERSION = 'v3'
# Function to get credentials
def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials

# Function to upload image URL to Blogger
def upload_image_url(credentials, blog_id, image_url, caption):
    blogger_service = build(API_NAME, API_VERSION, credentials=credentials)
    request = blogger_service.blogs().get(blogId=blog_id, view='ADMIN')
    blog = request.execute()
    body = {
        'kind': 'blogger#post',
        'blog': blog,
        'title': 'Image Post',
        'content': f'<img src="{image_url}"/> {caption}',  # Embedding the image URL in HTML
    }
    post = blogger_service.posts().insert(blogId=blog_id, body=body).execute()
    print(f'Image post created successfully. Post ID: {post["id"]}')

def main():
    credentials = get_credentials()
    # Replace 'YOUR_BLOG_ID' with your Blogger blog ID
    blog_id = 'YOUR_BLOG_ID'
    image_url = input('Enter the URL of the image: ')
    caption = input('Enter the caption for the image: ')
    upload_image_url(credentials, blog_id, image_url, caption)

if __name__ == '__main__':
    main()
