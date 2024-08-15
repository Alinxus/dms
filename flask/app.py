from flask import Flask, render_template, request, jsonify
from send import send_messages
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_messages', methods=['POST'])
def send_dm():
    data = request.json
    usernames = data.get('usernames', [])
    messages = data.get('messages', [])
    instagram_username = data.get('instagram_username')
    instagram_password = data.get('instagram_password')
    
    if not usernames or not messages:
        return jsonify({"error": "Usernames and messages are required"}), 400

    if not instagram_username or not instagram_password:
        return jsonify({"error": "Instagram username and password are required"}), 400

    results = send_messages(messages, usernames, 'session.json', instagram_username, instagram_password)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)