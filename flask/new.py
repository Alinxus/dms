from flask import Flask, request, jsonify, render_template
from send import send_instagram_dms
from send_linkedin import send_linkedin_dms
from twitter import send_twitter_dms
from tiktok import send_tiktok_dms
import json
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-dms', methods=['POST'])
def send_dms():
    try:
        platform = request.form.get('platform')
        proxy = request.form.get('proxy')
        logger.info(f"Received request for platform: {platform}")

        usernames = request.form.get('usernames', '').split('\n')
        usernames = [username.strip() for username in usernames if username.strip()]

        num_variations = int(request.form.get('NUM_VARIATIONS', 1))
        messages = [request.form.get(f'DM_MESSAGE_{i+1}', f'Default message {i+1}') for i in range(num_variations)]

        cookies_file = request.files.get('cookiesFile')
        if not cookies_file:
            return jsonify({'error': f'No cookies file provided for {platform.capitalize()}'}), 400
        
        cookies = cookies_file.read().decode('utf-8')
        
        try:
            json.loads(cookies)
        except json.JSONDecodeError as e:
            return jsonify({'error': f'Invalid JSON in cookies file for {platform.capitalize()}'}), 400

        if platform == 'instagram':
            success, failed = send_instagram_dms(messages, cookies, usernames, proxy)
        elif platform == 'linkedin':
            success, failed = send_linkedin_dms(cookies, messages, usernames, proxy)
        elif platform == 'twitter':
            success, failed = send_twitter_dms(messages, cookies, usernames, proxy)
        elif platform == 'tiktok':
            success, failed = send_tiktok_dms(messages, cookies, usernames, proxy)
        else:
            return jsonify({'error': 'Invalid platform specified'}), 400

        logger.info(f"DM sending complete. Success: {len(success)}, Failed: {len(failed)}")
        return jsonify({
            'success': success,
            'failed': failed
        })

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)