from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
import json
import logging
from datetime import datetime
import os
import uuid
from tiktok import send_tiktok_dms
from send import send_instagram_dms
from twitter import send_twitter_dms
from facebook import send_facebook_dms
from send_linkedin import send_linkedin_dms

app = Flask(__name__)
app.run(host='0.0.0.0')
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app, logger=True, engineio_logger=False)

# Disable Flask logging
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

sessions = {}

@app.route('/')
def index():
    return render_template('index.html', sessions=sessions)

@app.route('/create_session', methods=['GET', 'POST'])
def create_session():
    if request.method == 'POST':
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            'platform': request.form.get('platform'),
            'proxy': request.form.get('proxy'),
            'usernames': request.form.get('usernames', '').split('\n'),
            'messages': request.form.getlist('message'),
            'status': 'Configured',
            'results': [],
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'cookies': None
        }
        return redirect(url_for('view_session', session_id=session_id))
    return render_template('create_session.html')

@app.route('/view_session/<session_id>')
def view_session(session_id):
    session = sessions.get(session_id)
    if not session:
        return "Session not found", 404
    return render_template('view_session.html', session_id=session_id, session=session)

@app.route('/upload_cookies/<session_id>', methods=['POST'])
def upload_cookies(session_id):
    if 'cookies' not in request.files:
        return "No file part", 400
    file = request.files['cookies']
    if file.filename == '':
        return "No selected file", 400
    if file:
        cookies = file.read().decode('utf-8')
        try:
            json.loads(cookies)  # Validate JSON
            sessions[session_id]['cookies'] = cookies
            sessions[session_id]['status'] = 'Ready'
            return redirect(url_for('view_session', session_id=session_id))
        except json.JSONDecodeError:
            return "Invalid JSON file", 400

@app.route('/run_session/<session_id>')
def run_session(session_id):
    session = sessions.get(session_id)
    if not session or session['status'] != 'Ready':
        return "Session not ready", 400

    socketio.start_background_task(run_dm_sender, session_id)
    return redirect(url_for('view_session', session_id=session_id))

def run_dm_sender(session_id):
    session = sessions[session_id]
    session['status'] = 'Running'
    socketio.emit('status_update', {'status': 'Running'})

    try:
        platform = session['platform']
        messages = session['messages']
        cookies = session['cookies']
        usernames = session['usernames']
        proxy = session['proxy']

        if platform == 'tiktok':
            success, failed = send_tiktok_dms(messages, cookies, usernames, proxy)
        elif platform == 'instagram':
            success, failed = send_instagram_dms(messages, cookies, usernames, proxy)
        elif platform == 'twitter':
            success, failed = send_twitter_dms(messages, cookies, usernames, proxy)
        elif platform == 'facebook':
            success, failed = send_facebook_dms(messages, cookies, usernames, proxy)
        elif platform == 'linkedin':
            success, failed = send_linkedin_dms(messages, cookies, usernames, proxy)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

        session['results'] = [
            {'username': username, 'status': 'Success', 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            for username in success
        ] + [
            {'username': username, 'status': 'Failed', 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            for username in failed
        ]
        
        session['status'] = 'Completed'
        socketio.emit('status_update', {'status': 'Completed'})
        # Remove the print statement
    except Exception as e:
        # Remove the print statement
        session['status'] = 'Error'
        session['error'] = str(e)
        socketio.emit('status_update', {'status': 'Error', 'error': str(e)})

    socketio.emit('session_complete', {'success': len(success), 'failed': len(failed)})

@app.route('/sessions')
def list_sessions():
    return render_template('sessions.html', sessions=sessions)

@socketio.on('connect')
def handle_connect():
    # Remove the print statement
    pass

@socketio.on('disconnect')
def handle_disconnect():
    # Remove the print statement
    pass

if __name__ == "__main__":
   is_production = os.environ.get('FLASK_ENV') == 'production'
   port = int(os.environ.get('PORT', 5000))
   debug = not is_production

   print(f"Starting app on {host}:{port} with debug={debug}")
   socketio.run(app, host=host, port=port, debug=debug)