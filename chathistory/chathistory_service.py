from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone, timedelta
import json
import logging

# ===== App Configuration =====
app = Flask(__name__)
CORS(app)

# ===== Firebase Setup =====
# Initialize Firebase Admin
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# ===== Helper Functions =====
def get_sgt_time():
    """Get current time in SGT (UTC+8)"""
    utc_now = datetime.now(timezone.utc)
    sgt_offset = timedelta(hours=8)
    return utc_now + sgt_offset

def log_error(error, function_name):
    """Log error details with traceback"""
    logging.error(f"Error in {function_name}: {str(error)}")
    import traceback
    traceback.print_exc()

def ensure_user_exists(user_ref, customer_id):
    """Ensure user document exists, create if not"""
    user_doc = user_ref.get()
    
    if not user_doc.exists:
        user_ref.set({
            'created_at': get_sgt_time()
        })
        logging.info(f"Created new user document for customer: {customer_id}")
    
    return user_doc.exists

def parse_timestamp(timestamp_str):
    """Parse timestamp string or return current SGT time"""
    try:
        if not timestamp_str:
            return get_sgt_time()
            
        created_at = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S UTC+8")
        # Ensure the datetime is timezone-aware
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone(timedelta(hours=8)))
        return created_at
    except (ValueError, TypeError):
        logging.warning(f"Invalid timestamp format: {timestamp_str}, using current time")
        return get_sgt_time()

# ===== Request Logging =====
@app.before_request
def log_request_info():
    """Log request details for debugging"""
    logging.info(f"Request: {request.method} {request.path}")
    logging.info(f"Headers: {dict(request.headers)}")
    logging.info(f"Body: {request.get_data().decode()}")

# ===== API Endpoints =====
@app.route('/chat/<customer_id>', methods=['GET'])
def get_chat_history(customer_id):
    """Get chat history for a customer"""
    try:
        logging.info(f"Getting chat history for customer: {customer_id}")
        
        # Get user document
        user_ref = db.collection('chat_messages').document(customer_id)
        ensure_user_exists(user_ref, customer_id)
        
        # Get chat messages
        messages_ref = user_ref.collection('messages')
        messages = messages_ref.order_by('created_at').get()
        
        # Process messages
        chat_messages = []
        for message in messages:
            message_data = message.to_dict()
            chat_messages.append({
                'role': message_data.get('role', 'model'),
                'prompt': message_data.get('prompt', ''),
                'response': message_data.get('response', ''),
                'recommended_meal_kits': message_data.get('recommended_meal_kits', []),
                'created_at': message_data.get('created_at').isoformat() if message_data.get('created_at') else None
            })
        
        logging.info(f"Returning {len(chat_messages)} messages for customer: {customer_id}")
        return jsonify({'messages': chat_messages})
    except Exception as e:
        log_error(e, 'get_chat_history')
        return jsonify({'error': str(e)}), 500

@app.route('/chat/<customer_id>', methods=['POST'])
def add_chat_message(customer_id):
    """Add a new chat message for a customer"""
    try:
        logging.info(f"Adding chat message for customer: {customer_id}")
        
        # Validate request data
        data = request.get_json()
        if not data:
            logging.warning("No data provided in request")
            return jsonify({'error': 'No data provided'}), 400
            
        # Get user document reference
        user_ref = db.collection('chat_messages').document(customer_id)
        ensure_user_exists(user_ref, customer_id)
        
        # Parse timestamp
        created_at = parse_timestamp(data.get('created_at'))
        
        # Prepare message data
        message_data = {
            'role': data.get('role', 'model'),
            'prompt': data.get('prompt', ''),
            'response': data.get('response', ''),
            'recommended_meal_kits': data.get('recommended_meal_kits', []),
            'created_at': created_at
        }
        
        # Add message to Firestore
        messages_ref = user_ref.collection('messages')
        doc_ref = messages_ref.add(message_data)
        logging.info(f"Message saved with ID: {doc_ref[1].id}")
        
        return jsonify({'message': 'Chat message added successfully', 'document_id': doc_ref[1].id})
    except Exception as e:
        log_error(e, 'add_chat_message')
        return jsonify({'error': str(e)}), 500

@app.route('/chat/<customer_id>', methods=['DELETE'])
def delete_chat_history(customer_id):
    """Delete all chat history for a customer"""
    try:
        logging.info(f"Deleting chat history for customer: {customer_id}")
        
        # Get references
        user_ref = db.collection('chat_messages').document(customer_id)
        messages_ref = user_ref.collection('messages')
        
        # Delete all messages in the subcollection
        docs = messages_ref.get()
        for doc in docs:
            doc.reference.delete()
        
        # Delete the user document
        user_ref.delete()
        
        logging.info(f"Chat history deleted for customer: {customer_id}")
        return jsonify({'message': 'Chat history deleted successfully'})
    except Exception as e:
        log_error(e, 'delete_chat_history')
        return jsonify({'error': str(e)}), 500

# ===== Main Entry Point =====
if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Start the server
    app.run(host='0.0.0.0', port=5012, debug=True) 