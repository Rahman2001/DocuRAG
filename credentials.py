import os

# DOCURAG CREDENTIALS
DOCURAG_DOMAIN = 'https://cb5b-88-240-183-220.ngrok-free.app'  # YOUR NGROK DOMAIN
DOCURAG_CHAT_ENDPOINT = '/api/docurag/chat'
DOCURAG_CHAT_UI_ENDPOINT = '/api/docurag'

# GRADIO APP CREDENTIALS
GRADIO_APP_ENDPOINT = 'http://localhost:1243'

# GOOGLE CLOUD PROJECT CREDENTIALS
APP_CREDENTIALS_PATH = r'C:\Users\...\AppData\Roaming\gcloud\application_default_credentials.json'  # YOUR GCLOUD CREDENTIALS JSON FILE
PROJECT_ID = '...'  # YOUR GCLOUD PROJECT ID
LOCATION = "us-central1"  # YOUR GCLOUD PROJECT LOCATION
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = APP_CREDENTIALS_PATH
os.environ['GOOGLE_CLOUD_PROJECT'] = PROJECT_ID
OAUTH_CLIENT_CREDENTIALS_PATH = r'client_secret_{CLIENT_SECRET}.apps.googleusercontent.com.json'
OAUTH_SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile']
MODEL_NAME = "gemini-1.5-pro-001"

# GOOGLE CLOUD OAUTH CREDENTIALS
AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'

# GOOGLE DRIVE LINKS TO YOUR DOCUMENTS
PATHS = ["https://drive.google.com/file/d/1EFe1SY_JdyHPQUjEvyfcxqmqHeaDSJIk/view?usp=sharing"]

# GOOGLE GMAIL CREDENTIALS
SENDER_ACCOUNT_ID = '...'  # YOUR TESTING GMAIL ACCOUNT
SENDER_ACCOUNT_APP_PASSWORD = '...'  # YOUR APP PASSWORD FOR TESTING GMAIL ACCOUNT
RECEIVER_ACCOUNT_ID = '...'  # RECEIVER GMAIL ACCOUNT
