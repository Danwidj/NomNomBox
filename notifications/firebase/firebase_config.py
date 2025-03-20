import firebase_admin
from firebase_admin import credentials, firestore
import os
import sys

# Load Firebase credentials from environment variables or file
firebase_cred_path = os.getenv("FIREBASE_CREDENTIALS", "notifications-serviceAccountKey.json")

# Check if the file exists
if not os.path.exists(firebase_cred_path):
    print(f"ERROR: Firebase credentials file not found at {firebase_cred_path}")
    print("Make sure the file exists and the path is correct.")
    sys.exit(1)

# Initialize Firebase app
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_cred_path)
        firebase_admin.initialize_app(cred)
        print(f"Firebase initialized successfully with credentials from {firebase_cred_path}")
    else:
        print("Firebase already initialized")
except Exception as e:
    print(f"ERROR initializing Firebase: {e}")
    sys.exit(1)
