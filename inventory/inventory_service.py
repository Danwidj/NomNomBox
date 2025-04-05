import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

# Initialize Firebase Admin SDK
cred = credentials.Certificate('./inventory-serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Helper function to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Set the upload folder for file uploads
# Set the upload folder for file uploads
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.getcwd(), 'inventory', 'uploads'))
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create the uploads folder if it doesn't exist
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Mass upload endpoint for meal kits from CSV/Excel file
@app.route("/inventory/mass_upload", methods=["POST"])
def mass_upload():
    try:
        if 'file' not in request.files:
            return jsonify({"code": 400, "message": "No file part"}), 400
        
        file = request.files['file']
        
        # Log the filename
        print(f"Uploaded file: {file.filename}")
        
        if file.filename == '':
            return jsonify({"code": 400, "message": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
            print(f"File path: {filepath}")
            file.save(filepath)
            
            # Process the uploaded file (CSV or Excel)
            meal_kits_data = process_file(filepath)

            # Upload the meal kits to Firestore
            upload_data_batch(meal_kits_data)
            
            return jsonify({"code": 201, "message": f"Successfully uploaded {len(meal_kits_data)} meal kits"}), 201
        else:
            return jsonify({"code": 400, "message": "Invalid file format. Only CSV and Excel files are allowed."}), 400
    except Exception as e:
        return jsonify({"code": 500, "message": f"Error during file upload: {str(e)}"}), 500

# Helper function to process the uploaded file (CSV/Excel)
def process_file(file_path):
    # Read the file into a DataFrame (CSV or Excel)
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, engine='openpyxl')
    
    # Prepare data for Firestore upload
    meal_kits_data = []
    for _, row in df.iterrows():
        meal_kit = {
            "id": row['id'],
            "description": row['description'],
            "dietaryTags": eval(row['dietaryTags']),  # Convert string to list
            "imageURL": row['imageURL'],
            "ingredients": eval(row['ingredients']),  # Convert string to list
            "isAvailable": row['isAvailable'],
            "name": row['name'],
            "numAvailable": row['numAvailable'],
            "nutritionalInfo": eval(row['nutritionalInfo']),  # Convert string to dictionary
            "preparationTime": row['preparationTime'],
            "price": row['price'],
            "servings": row['servings']
        }
        meal_kits_data.append(meal_kit)
    
    return meal_kits_data

# Helper function to upload data in batches
def upload_data_batch(meal_kits_data):
    # Reference to Firestore collection 'inventory'
    inventory_ref = db.collection('inventory')

    # Start a batch operation
    batch = db.batch()

    for meal_kit in meal_kits_data:
        # Add each meal kit to the batch
        meal_ref = inventory_ref.document()  # Automatically generate document ID
        batch.set(meal_ref, meal_kit)

    # Commit the batch operation
    batch.commit()
    print(f"Successfully uploaded {len(meal_kits_data)} meal kits to Firestore.")

# Get all meal kits
@app.route("/inventory", methods=["GET"])
def get_inventory():
    try:
        kits_ref = db.collection("inventory").stream()
        kits = [kit.to_dict() for kit in kits_ref]

        if kits:
            return jsonify({"code": 200, "data": kits}), 200
        return jsonify({"code": 404, "message": "No meal kits available"}), 404
    except Exception as e:
        return jsonify({"code": 500, "message": f"Error fetching inventory: {str(e)}"}), 500


# Get meal kit by ID
@app.route("/inventory/<string:kit_id>", methods=["GET"])
def get_meal_kit(kit_id):
    try:
        # Query Firestore for a meal kit where "id" field matches kit_id
        kits_ref = db.collection("inventory").where("id", "==", kit_id).stream()
        
        meal_kits = [kit.to_dict() for kit in kits_ref]  # Convert query results to a list

        if meal_kits:
            return jsonify({"code": 200, "data": meal_kits[0]}), 200  # Return the first match
        else:
            return jsonify({"code": 404, "message": "Meal kit not found"}), 404
    except Exception as e:
        return jsonify({"code": 500, "message": f"Error retrieving meal kit: {str(e)}"}), 500





# Add a new meal kit
@app.route("/inventory", methods=["POST"])
def add_meal_kit():
    try:
        data = request.json
        required_fields = ["name", "ingredients", "stock", "price"]

        if not all(field in data for field in required_fields):
            return jsonify({"code": 400, "message": "Missing required fields"}), 400

        kit_id = f"kit_{data['name'].replace(' ', '_')}"  # Generate unique ID
        db.collection("inventory").document(kit_id).set({
            "kit_id": kit_id,
            "name": data["name"],
            "ingredients": data["ingredients"],
            "stock": data["stock"],
            "price": data["price"]
        })

        return jsonify({"code": 201, "message": "Meal kit added"}), 201
    except Exception as e:
        return jsonify({"code": 500, "message": f"Error adding meal kit: {str(e)}"}), 500


# Update stock safely using transactions
@app.route("/inventory/<string:kit_id>", methods=["PUT"])
def update_stock(kit_id):
    try:
        data = request.json
        if "stock" not in data:
            return jsonify({"code": 400, "message": "Missing 'stock' field"}), 400

        # Query Firestore for the document where "id" matches kit_id
        kits_ref = db.collection("inventory").where("id", "==", kit_id).stream()
        kit_docs = list(kits_ref)

        if not kit_docs:
            return jsonify({"code": 404, "message": "Meal kit not found"}), 404

        # Get the first matching document (Firestore generates random document IDs)
        doc_ref = db.collection("inventory").document(kit_docs[0].id)

        # Proper transaction function
        @firestore.transactional
        def stock_transaction(transaction, ref):
            doc = ref.get(transaction=transaction)
            if not doc.exists:
                raise ValueError("Meal kit not found")

            transaction.update(ref, {"numAvailable": data["stock"]})

        transaction = db.transaction()  #  Start transaction 
        stock_transaction(transaction, doc_ref)  #  Run the transaction

        return jsonify({"code": 200, "message": "Stock updated successfully"}), 200

    except ValueError as e:
        return jsonify({"code": 404, "message": str(e)}), 404
    except Exception as e:
        return jsonify({"code": 500, "message": f"Error updating stock: {str(e)}"}), 500


# Delete a meal kit
@app.route("/inventory/<string:kit_id>", methods=["DELETE"])
def delete_meal_kit(kit_id):
    try:
        kit_ref = db.collection("inventory").document(kit_id)
        if not kit_ref.get().exists:
            return jsonify({"code": 404, "message": "Meal kit not found"}), 404

        kit_ref.delete()
        return jsonify({"code": 200, "message": "Meal kit deleted successfully"}), 200
    except Exception as e:
        return jsonify({"code": 500, "message": f"Error deleting meal kit: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
        
