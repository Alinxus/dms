from flask import Flask, request, jsonify, render_template
import asyncio
from send import main as send_instagram_dms
from send_linkedin import main as send_linkedin_dms
import os
import json
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-dms', methods=['POST'])
def send_dms():
    try:
        platform = request.form.get('platform')
        contacts = []
        
        contacts_input = request.form.get('contactsInput')
        if contacts_input:
            contacts.extend([contact.strip() for contact in contacts_input.split(',')])
        
        if 'contactsFile' in request.files:
            contacts_file = request.files['contactsFile']
            contacts_path = os.path.join(os.getcwd(), 'temp_contacts.csv')
            contacts_file.save(contacts_path)
            with open(contacts_path, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row:
                        contacts.append(row[0].strip())
            os.remove(contacts_path)
        
        if not contacts:
            return jsonify({'error': 'No contacts provided'}), 400
        
        custom_message = request.form.get('customMessage', 'Hello, this is a test message!')
        messages = [custom_message]
        
        if platform == 'instagram':
            cookies_content = request.form.get('cookiesContent') or request.files.get('cookiesFile').read().decode('utf-8')
            if not cookies_content:
                return jsonify({'error': 'No cookies provided for Instagram'}), 400

            cookies_path = os.path.join(os.getcwd(), f'temp_session_{datetime.now().strftime("%Y%m%d%H%M%S")}.json')
            with open(cookies_path, 'w') as f:
                f.write(cookies_content)

            result = asyncio.run(send_instagram_dms(messages, contacts, cookies_path))
            os.remove(cookies_path)

        elif platform == 'linkedin':
            email = request.form.get('email')
            password = request.form.get('password')
            if not email or not password:
                return jsonify({'error': 'Email and password required for LinkedIn'}), 400

            result = asyncio.run(send_linkedin_dms(email, password, messages, contacts))
        
        else:
            return jsonify({'error': 'Invalid platform specified'}), 400
        
        if result is None:
            return jsonify({'error': 'DM sending process failed'}), 500
        
        success, failed = result
        
        return jsonify({
            'success': success,
            'failed': failed
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)