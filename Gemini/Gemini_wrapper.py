from flask import Flask, jsonify, request
import json
import os
from flask_cors import CORS
from google import genai
from google.genai import types
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def generate(data):
    try:
        prompt = data['prompt']
        context_data = {
            'dietary_preferences': data.get('dietary_preferences', []),
            'order_history': data.get('order_history', []),
            'inventory': data.get('inventory', [])
        }

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "nomnombox-8bf47.json"
        client = genai.Client(
            vertexai=True,
            project="nomnombox-8bf47",
            location="us-central1",
        )

        si_text1 = """NomNomBox is a meal-kit plan that delivers customised meal-kit to customer. 
        You are meal-kit recommender that does recommends meal-kit based on customer dietary preferences, order history, and the warehouse inventory.
        
        Context Data: {}
        
        Please provide recommendations based on the provided context and respond to the user's prompt.
        """.format(json.dumps(context_data))

        model = "gemini-2.0-flash-lite-001"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt)
                ]
            )
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature = 0.2,
            top_p = 0.8,
            max_output_tokens = 1024,
            response_modalities = ["TEXT"],
            response_mime_type = "application/json",
            response_schema = {
                "type": "OBJECT",
                "properties": {
                    "recommended meal-kit": {
                        "type": "ARRAY",
                        "items": {
                            "type": "STRING",
                            "enum": ["MK001","MK002","MK004","MK005","MK006","MK008","MK009"]
                        },
                        "maxItems": 3,
                        "minItems": 0,
                        "description": "A list of up to 3 unique meal-kit IDs that are currently available."
                    },
                    "response": {
                        "type": "STRING",
                        "description": "A natural language explanation or response to the user's query regarding the meal-kits."
                    }
                },
                "required": ["recommended meal-kit","response"]
            },
            system_instruction=[types.Part.from_text(text=si_text1)],
        )

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config
        )

        return response.text

    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/generate-recommendation', methods=['POST'])
def generate_recommendation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing prompt in request'}), 400
        reply = json.loads(generate(data))
        print(reply)
        return jsonify({"prompt": data["prompt"], "response": reply['response'], "recommended meal-kit": reply['recommended meal-kit']}) 
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5009)