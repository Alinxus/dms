from flask import Flask, request, jsonify, render_template
import asyncio
from send import main as send_dm_messages
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
        contacts = []
        
        # Handle contacts from input
        contacts_input = request.form.get('contactsInput')
        if contacts_input:
            contacts.extend([contact.strip() for contact in contacts_input.split(',')])
        
        # Handle contacts from CSV file
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
        
        # Handle cookies
        cookies_content = None
        if 'cookiesContent' in request.form:
            cookies_content = request.form['cookiesContent']
        elif 'cookiesFile' in request.files:
            cookies_file = request.files['cookiesFile']
            cookies_content = cookies_file.read().decode('utf-8')
        
        if not cookies_content:
            return jsonify({'error': 'No cookies provided'}), 400
        
        # Save cookies to a temporary file
        cookies_path = os.path.join(os.getcwd(), f'temp_session_{datetime.now().strftime("%Y%m%d%H%M%S")}.json')
        with open(cookies_path, 'w') as f:
            f.write(cookies_content)
        
        custom_message = request.form.get('customMessage', 'Hello {username}, this is a test message!')
        messages = [custom_message]
        
        result = asyncio.run(send_dm_messages(messages, contacts, cookies_path))
        
        # Remove the temporary cookies file
        os.remove(cookies_path)
        
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