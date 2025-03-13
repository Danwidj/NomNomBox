import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import stripe

# Load environment variables from .env file
load_dotenv()

# Get the path of serviceAccountKey.json from the environment variable
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "serviceAccountKey.json")
# Use environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
# Initialize Firebase
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()