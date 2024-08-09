from chalice import Chalice, Response
from src.models.user import UserCreate, UserLogin
from src.models.account import AccountCreate
from src.models.campaign import CampaignCreate
from chalice import CORSConfig
from src.utils.auth import create_access_token, get_current_user, get_password_hash, verify_password, get_user_by_email
from src.utils.db_operations import create_user, create_account, create_campaign, get_user_accounts, get_user_campaigns
from src.utils.queue_manager import enqueue_message

app = Chalice(app_name='mass-dm-sender')

cors_config = CORSConfig(
    allow_origin='https://your-frontend-domain.vercel.app',
    allow_headers=['Content-Type', 'Authorization']
)

@app.authorizer()
def token_auth(auth_request):
    token = auth_request.token
    user_id = decode_token(token)
    return {'principalId': user_id}

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

@app.route('/api/accounts', methods=['POST'], authorizer=token_auth)
def add_account():
    account_data = app.current_request.json_body
    user_id = app.current_request.context['authorizer']['principalId']
    account_create = AccountCreate(**account_data, user_id=user_id)
    account = create_account(account_create)
    return {'message': 'Account added successfully', 'account_id': account.id}

@app.route('/api/accounts', methods=['GET'], authorizer=token_auth)
def get_accounts():
    user_id = app.current_request.context['authorizer']['principalId']
    accounts = get_user_accounts(user_id)
    return {'accounts': [account.dict() for account in accounts]}

@app.route('/api/campaigns', methods=['POST'], content_types=['multipart/form-data'], authorizer=token_auth)
def create_new_campaign():
    user_id = app.current_request.context['authorizer']['principalId']
    
    # Get form data
    form_data = app.current_request.form
    
    # Get file data
    leads_file = app.current_request.files.get('leads')
    
    # Process campaign data
    campaign_data = {
        'name': form_data.get('name'),
        'message': form_data.get('message'),
        'user_id': user_id
    }
    campaign_create = CampaignCreate(**campaign_data)
    campaign = create_campaign(campaign_create)

    # Process leads file if provided
    leads = []
    if leads_file:
        # Read CSV file
        csv_file = io.StringIO(leads_file.read().decode('utf-8'))
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            leads.append(row)
        
        # Here you would typically save or process the leads
        # For example, you might want to associate them with the campaign
        campaign.add_leads(leads)

    return {'message': 'Campaign created successfully', 'campaign_id': str(campaign.id), 'leads_count': len(leads)}

@app.route('/api/campaigns', methods=['GET'], authorizer=token_auth)
def get_campaigns():
    user_id = app.current_request.context['authorizer']['principalId']
    campaigns = get_user_campaigns(user_id)
    return {'campaigns': [campaign.dict() for campaign in campaigns]}

@app.route('/api/send-message', methods=['POST'], authorizer=token_auth)
def send_message():
    message_data = app.current_request.json_body
    user_id = app.current_request.context['authorizer']['principalId']
    message_data['user_id'] = user_id
    message_id = enqueue_message(message_data)
    return {'message': 'Message queued successfully', 'message_id': message_id}
