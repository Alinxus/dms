from flask import Flask, request, jsonify
from flask_cors import CORS
from src.models.user import UserCreate, UserLogin
from src.models.account import AccountCreate
from src.models.campaign import CampaignCreate
from src.utils.auth import create_access_token, get_current_user, get_password_hash, verify_password, get_user_by_email
from src.utils.db_operations import create_user, create_account, create_campaign, get_user_accounts, get_user_campaigns
from src.utils.queue_manager import enqueue_message
from functools import wraps
import io
import csv

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://your-frontend-domain.vercel.app"}})

def token_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            current_user = get_current_user(token)
            if not current_user:
                return jsonify({'message': 'Invalid token'}), 401
        except:
            return jsonify({'message': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/register', methods=['POST'])
def register():
    user_data = request.json
    user_create = UserCreate(**user_data)
    password_hash = get_password_hash(user_create.password)
    user = create_user(user_create, password_hash)
    return jsonify({'message': 'User created successfully', 'user_id': user.id})

@app.route('/api/login', methods=['POST'])
def login():
    user_data = request.json
    user_login = UserLogin(**user_data)
    user = get_user_by_email(user_login.email)
    if not user or not verify_password(user_login.password, user.password_hash):
        return jsonify({'error': 'Invalid email or password'}), 401
    access_token = create_access_token(user)
    return jsonify({'access_token': access_token, 'token_type': 'bearer'})

@app.route('/api/accounts', methods=['POST'])
@token_auth_required
def add_account(current_user):
    account_data = request.json
    account_create = AccountCreate(**account_data, user_id=current_user.id)
    account = create_account(account_create)
    return jsonify({'message': 'Account added successfully', 'account_id': account.id})

@app.route('/api/accounts', methods=['GET'])
@token_auth_required
def get_accounts(current_user):
    accounts = get_user_accounts(current_user.id)
    return jsonify({'accounts': [account.dict() for account in accounts]})

@app.route('/api/campaigns', methods=['POST'])
@token_auth_required
def create_new_campaign(current_user):
    form_data = request.form
    leads_file = request.files.get('leads')
    
    campaign_data = {
        'name': form_data.get('name'),
        'message': form_data.get('message'),
        'user_id': current_user.id
    }
    campaign_create = CampaignCreate(**campaign_data)
    campaign = create_campaign(campaign_create)

    leads = []
    if leads_file:
        csv_file = io.StringIO(leads_file.read().decode('utf-8'))
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            leads.append(row)
        
        # Here you would typically save or process the leads
        # For example, you might want to associate them with the campaign
        campaign.add_leads(leads)

    return jsonify({'message': 'Campaign created successfully', 'campaign_id': str(campaign.id), 'leads_count': len(leads)})

@app.route('/api/campaigns', methods=['GET'])
@token_auth_required
def get_campaigns(current_user):
    campaigns = get_user_campaigns(current_user.id)
    return jsonify({'campaigns': [campaign.dict() for campaign in campaigns]})

@app.route('/api/send-message', methods=['POST'])
@token_auth_required
def send_message(current_user):
    message_data = request.json
    message_data['user_id'] = current_user.id
    message_id = enqueue_message(message_data)
    return jsonify({'message': 'Message queued successfully', 'message_id': message_id})

if __name__ == '__main__':
    app.run(debug=True)