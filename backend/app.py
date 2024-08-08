from chalice import Chalice, Response
from src.models.user import UserCreate, UserLogin
from src.models.account import AccountCreate
from src.models.campaign import CampaignCreate
from src.utils.auth import create_access_token, get_current_user, get_password_hash, verify_password, get_user_by_email
from src.utils.db_operations import create_user, create_account, create_campaign, get_user_accounts, get_user_campaigns
from src.utils.queue_manager import enqueue_messageimport csv
from flask import request, jsonify
from werkzeug.utils import secure_filename

app = Chalice(app_name='mass-dm-sender')

@app.route('/api/register', methods=['POST'])
def register():
    user_data = app.current_request.json_body
    user_create = UserCreate(**user_data)
    password_hash = get_password_hash(user_create.password)
    user = create_user(user_create, password_hash)
    return {'message': 'User created successfully', 'user_id': user.id}

@app.route('/api/login', methods=['POST'])
def login():
    user_data = app.current_request.json_body
    user_login = UserLogin(**user_data)
    user = get_user_by_email(user_login.email)
    if not user or not verify_password(user_login.password, user.password_hash):
        return Response(body={'error': 'Invalid email or password'}, status_code=401)
    access_token = create_access_token(user)
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.route('/api/accounts', methods=['POST'], authorizer='token_auth')
def add_account():
    account_data = app.current_request.json_body
    user_id = app.current_request.context['authorizer']['principalId']
    account_create = AccountCreate(**account_data, user_id=user_id)
    account = create_account(account_create)
    return {'message': 'Account added successfully', 'account_id': account.id}

@app.route('/api/accounts', methods=['GET'], authorizer='token_auth')
def get_accounts():
    user_id = app.current_request.context['authorizer']['principalId']
    accounts = get_user_accounts(user_id)
    return {'accounts': [account.dict() for account in accounts]}

@app.route('/api/campaigns', methods=['POST'], authorizer='token_auth')
def create_new_campaign():
    campaign_data = app.current_request.json_body
    user_id = app.current_request.context['authorizer']['principalId']
    campaign_create = CampaignCreate(**campaign_data, user_id=user_id)
    campaign = create_campaign(campaign_create)leads_file = request.files.get('leads')

    if leads_file:
        filename = secure_filename(leads_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        leads_file.save(file_path)

        leads = []
        with open(file_path, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                leads.append(row)

    return {'message': 'Campaign created successfully', 'campaign_id': campaign.id}

@app.route('/api/campaigns', methods=['GET'], authorizer='token_auth')
def get_campaigns():
    user_id = app.current_request.context['authorizer']['principalId']
    campaigns = get_user_campaigns(user_id)
    return {'campaigns': [campaign.dict() for campaign in campaigns]}

@app.route('/api/send-message', methods=['POST'], authorizer='token_auth')
def send_message():
    message_data = app.current_request.json_body
    user_id = app.current_request.context['authorizer']['principalId']
    message_data['user_id'] = user_id
    message_id = enqueue_message(message_data)
    return {'message': 'Message queued successfully', 'message_id': message_id}

@app.authorizer()
def token_auth(auth_request):
    token = auth_request.token
    user = get_current_user(token)
    if user is None:
        raise Exception('Unauthorized')
    return {'principalId': user.id}