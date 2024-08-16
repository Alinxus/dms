from flask import Flask, request, jsonify, render_template
import asyncio
from send import main as send_dm_messages
import os
import json
import csv
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='instagram_dm_sender.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    logging.info("Rendering index page")
    return render_template('index.html')

@app.route('/send-dms', methods=['POST'])
def send_dms():
    logging.info("Received request to send DMs")
    try:
        contacts = []
        
        # Handle contacts from input
        contacts_input = request.form.get('contactsInput')
        if contacts_input:
            contacts.extend([contact.strip() for contact in contacts_input.split(',')])
            logging.info(f"Received {len(contacts)} contacts from input")
        
        # Handle contacts from CSV file
        if 'contactsFile' in request.files:
            contacts_file = request.files['contactsFile']
            contacts_path = os.path.join(os.getcwd(), 'contacts.csv')
            contacts_file.save(contacts_path)
            logging.info(f"Saved contacts file to {contacts_path}")
            with open(contacts_path, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row:
                        contacts.append(row[0].strip())
            logging.info(f"Read {len(contacts)} contacts from CSV file")
            os.remove(contacts_path)
            logging.info(f"Removed temporary contacts file: {contacts_path}")
        
        if not contacts:
            logging.error("No contacts provided")
            return jsonify({'error': 'No contacts provided'}), 400
        
        # Handle cookies
        cookies_content = None
        if 'cookiesContent' in request.form:
            cookies_content = request.form['cookiesContent']
            logging.info("Received cookies content from form data")
        elif 'cookiesFile' in request.files:
            cookies_file = request.files['cookiesFile']
            cookies_content = cookies_file.read().decode('utf-8')
            logging.info("Read cookies content from uploaded file")
        
        if not cookies_content:
            logging.error("No cookies provided")
            return jsonify({'error': 'No cookies provided'}), 400
        
        # Save cookies to a temporary file
        cookies_path = os.path.join(os.getcwd(), f'temp_session_{datetime.now().strftime("%Y%m%d%H%M%S")}.json')
        with open(cookies_path, 'w') as f:
            f.write(cookies_content)
        logging.info(f"Saved cookies to temporary file: {cookies_path}")
        
        custom_message = request.form.get('customMessage', 'Hello {username}, this is a test message!')
        messages = [custom_message]
        logging.info(f"Custom message: {custom_message}")
        
        logging.info("Starting DM sending process")
        result = asyncio.run(send_dm_messages(messages, contacts, cookies_path))
        
        # Remove the temporary cookies file
        os.remove(cookies_path)
        logging.info(f"Removed temporary cookies file: {cookies_path}")
        
        if result is None:
            logging.error("DM sending process failed")
            return jsonify({'error': 'DM sending process failed'}), 500
        
        success, failed = result
        logging.info(f"DM sending process completed. Success: {len(success)}, Failed: {len(failed)}")
        
        return jsonify({
            'success': success,
            'failed': failed
        })
    
    except Exception as e:
        logging.exception(f"An error occurred during the DM sending process: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logging.info("Starting Flask application")
    app.run(debug=True)