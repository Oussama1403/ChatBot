from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from pymongo import MongoClient
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access the API key using os.getenv
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Set up Gemini API
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

CORS(app, resources={r'/*': {'origins': '*'}})
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string if needed
db = client['user_database']
users_collection = db['users']

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')
    print(username, password, confirm_password)
    if users_collection.find_one({'username': username}):
        return jsonify({'message': 'User already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = {
        'username': username,
        'password': hashed_password,
        'confirmPassword': confirm_password
    }
    users_collection.insert_one(new_user)
    print('User created successfully')

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({'username': username})
    if user and bcrypt.check_password_hash(user['password'], password):
        token = create_access_token(identity=str(user['_id']))
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.json
    print(data)
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': '"message" field is required and cannot be empty'}), 422

    try:
        # Use the Gemini API for generating chat responses
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(history=[])
        response = chat.send_message(message)

        return jsonify({'reply': response.text.strip()})
    except Exception as e:
        print(f"Error communicating with Gemini: {str(e)}")
        return jsonify({'error': f"Error communicating with Gemini: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
