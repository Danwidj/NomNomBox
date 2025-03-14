import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Firebase credentials from .env
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_credentials_path:
    raise ValueError("Missing FIREBASE_CREDENTIALS in .env file")

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred)

# Export Firestore DB & Auth
db = firestore.client()
auth = auth
