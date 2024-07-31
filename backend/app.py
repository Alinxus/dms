# backend/app.py

from chalice import Chalice, AuthResponse
from chalice.app import AuthRoute
from src.models.user import UserCreate, UserLogin
from src.models.account import AccountCreate
from src.models.campaign import CampaignCreate
from src.utils.auth import create_access_token, get_current_user, get_password_hash, verify_password
from src.utils.db_operations import create_user, create_account, create_campaign, get_user_accounts
from src.utils.queue_manager import enqueue_message

app = Chalice(app_name='mass-dm-sender')

@app.route('/register', methods=['POST'])
def register():
    user_data = app.current_request.json_body
    user_create = UserCreate(**user_data)
    password_hash = get_password_hash(user_create.password)
    user = create_user(user_create, password_hash)
    return {'message': 'User created successfully', 'user_id': user.id}

@app.route('/login', methods=['POST'])
def login():
    user_data = app.current_request.json_body
    user_login = UserLogin(**user_data)
    user = get_user_by_email(user_login.email)
    if not user or not verify_password(user_login.password, user.password_hash):
        return {'error': 'Invalid email or password'}, 401
    access_token = create_access_token(user)
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.authorizer()
def token_auth(auth_request):
    token = auth_request.token
    user = get_current_user(token)
    if user is None:
        return AuthResponse(routes=[], principal_id=None)
    return AuthResponse(routes=[AuthRoute('*', ['*'])], principal_id=user.id)

@app.route('/accounts', methods=['POST'], authorizer=token_auth)
def add_account():
    account_data = app.current_request.json_body
    account_create = AccountCreate(**account_data)
    account = create_account(account_create)
    return {'message': 'Account added successfully', 'account_id': account.id}

@app.route('/accounts', methods=['GET'], authorizer=token_auth)
def get_accounts():
    user_id = app.current_request.context['authorizer']['principalId']
    accounts = get_user_accounts(user_id)
    return {'accounts': [account.dict() for account in accounts]}

@app.route('/campaigns', methods=['POST'], authorizer=token_auth)
def create_new_campaign():
    campaign_data = app.current_request.json_body
    campaign_create = CampaignCreate(**campaign_data)
    campaign = create_campaign(campaign_create)
    return {'message': 'Campaign created successfully', 'campaign_id': campaign.id}

@app.route('/send-message', methods=['POST'], authorizer=token_auth)
def send_message():
    message_data = app.current_request.json_body
    user_id = app.current_request.context['authorizer']['principalId']
    message_data['user_id'] = user_id
    message_id = enqueue_message(message_data)
    return {'message': 'Message queued successfully', 'message_id': message_id}