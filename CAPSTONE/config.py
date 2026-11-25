import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file if it exists
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    # Flask Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart-parking-secret-key-2026-prod-sec')
    DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'parking.db')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'data', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json'}

    # Firebase Realtime Database - Server-Side Admin Config
    FIREBASE_DATABASE_URL = os.environ.get('FIREBASE_DATABASE_URL', '').strip()
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH', '').strip()
    if FIREBASE_CREDENTIALS_PATH and not os.path.isabs(FIREBASE_CREDENTIALS_PATH):
        FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, FIREBASE_CREDENTIALS_PATH)

    # Firebase Client-Side Web Config (Publicly safe client properties)
    FIREBASE_CLIENT_CONFIG = {
        'apiKey': os.environ.get('FIREBASE_API_KEY', '').strip(),
        'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN', '').strip(),
        'databaseURL': os.environ.get('FIREBASE_DATABASE_URL', '').strip(),
        'projectId': os.environ.get('FIREBASE_PROJECT_ID', '').strip(),
        'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET', '').strip(),
        'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID', '').strip(),
        'appId': os.environ.get('FIREBASE_APP_ID', '').strip()
    }

    # Admin seed credentials
    DEFAULT_ADMIN_NAME = os.environ.get('DEFAULT_ADMIN_NAME', 'System Administrator')
    DEFAULT_ADMIN_EMAIL = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@smartparking.com')
    DEFAULT_ADMIN_PASSWORD = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'Admin@12345')

    # Attendant seed credentials
    DEFAULT_ATTENDANT_NAME = os.environ.get('DEFAULT_ATTENDANT_NAME', 'Parking Attendant')
    DEFAULT_ATTENDANT_EMAIL = os.environ.get('DEFAULT_ATTENDANT_EMAIL', 'attendant@smartparking.com')
    DEFAULT_ATTENDANT_PASSWORD = os.environ.get('DEFAULT_ATTENDANT_PASSWORD', 'Attendant@123')
