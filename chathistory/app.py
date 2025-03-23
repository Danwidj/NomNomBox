from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            customer_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create chat_messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            role TEXT CHECK(role IN ('user', 'model')),
            prompt TEXT,
            response TEXT,
            recommended_meal_kits TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES users (customer_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('chat_history.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
init_db()

@app.route('/chat/<customer_id>', methods=['GET'])
def get_chat_history(customer_id):
    try:
        conn = get_db()
        c = conn.cursor()
        
        # Check if user exists, if not create new user
        c.execute('SELECT * FROM users WHERE customer_id = ?', (customer_id,))
        if not c.fetchone():
            c.execute('INSERT INTO users (customer_id) VALUES (?)', (customer_id,))
            conn.commit()
        
        # Get chat history
        c.execute('''
            SELECT role, prompt, response, recommended_meal_kits, created_at
            FROM chat_messages
            WHERE customer_id = ?
            ORDER BY created_at ASC
        ''', (customer_id,))
        
        messages = []
        for row in c.fetchall():
            message = {
                'type': row['role'],
                'prompt': row['prompt'],
                'response': row['response'],
                'recommended_meal_kits': json.loads(row['recommended_meal_kits']) if row['recommended_meal_kits'] else [],
                'timestamp': row['created_at']
            }
            messages.append(message)
        
        return jsonify({'messages': messages})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/chat/<customer_id>', methods=['POST'])
def add_chat_message(customer_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        conn = get_db()
        c = conn.cursor()
        
        # Check if user exists, if not create new user
        c.execute('SELECT * FROM users WHERE customer_id = ?', (customer_id,))
        if not c.fetchone():
            c.execute('INSERT INTO users (customer_id) VALUES (?)', (customer_id,))
        
        # Insert user message
        c.execute('''
            INSERT INTO chat_messages (customer_id, role, prompt)
            VALUES (?, 'user', ?)
        ''', (customer_id, data.get('prompt')))
        
        # Insert model response if provided
        if 'model_response' in data:
            c.execute('''
                INSERT INTO chat_messages (customer_id, role, prompt, response, recommended_meal_kits)
                VALUES (?, 'model', ?, ?, ?)
            ''', (
                customer_id,
                data.get('model_prompt', ''),
                data['model_response'].get('response', ''),
                json.dumps(data['model_response'].get('recommended_meal-kit', []))
            ))
        
        conn.commit()
        return jsonify({'message': 'Chat message added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/chat/<customer_id>', methods=['DELETE'])
def delete_chat_history(customer_id):
    try:
        conn = get_db()
        c = conn.cursor()
        
        # Delete all messages for the user
        c.execute('DELETE FROM chat_messages WHERE customer_id = ?', (customer_id,))
        # Delete the user
        c.execute('DELETE FROM users WHERE customer_id = ?', (customer_id,))
        
        conn.commit()
        return jsonify({'message': 'Chat history deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True) 