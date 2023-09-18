from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors

# this was the test file for intitial flask connection please run app.py
import requests
import logging

app = Flask(__name__)
CORS(app)  # Initialize CORS with your Flask app

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)  # Log errors to a file

# Route to receive messages from the frontend
@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        user_message = data.get('message')

        # Forward the user's message to the Worqhat API
        worqhat_url = "https://api.worqhat.com/api/ai/content/v3"
        headers = {
            "Authorization": "Bearer sk-0988d888ee574422a01561e9bf5de02e",  # Replace with your actual API key
            "Content-Type": "application/json"
        }
        worqhat_data = {
            "question": user_message,
            "randomness": 0.4
        }
        response = requests.post(worqhat_url, headers=headers, json=worqhat_data)

        if response.status_code == 200:
            worqhat_response = response.json().get("content")
            return jsonify({"response": worqhat_response})

        # Log the error
        logging.error(f"Error in request to Worqhat API: {response.status_code} - {response.text}")

        return jsonify({"response": "Error communicating with Worqhat API"})

    except Exception as e:
        # Log the exception
        logging.error(f"Exception in send_message route: {str(e)}")
        return jsonify({"response": str(e)})

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode in production
