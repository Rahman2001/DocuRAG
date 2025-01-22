import json
import logging
import sys
from uuid import uuid4

from flask import Flask, redirect
from flask import jsonify
from flask import request
from flask_cors import CORS

from utils import email, check_link
from db import MongoDB
from flask_session import Session

from google_auth_oauthlib.flow import InstalledAppFlow

from model import *

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app, supports_credentials=True)

__model = None
__mongodb = None

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/api/docurag/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    docusign_state = request.args.get('state')
    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_secrets_file(
        OAUTH_CLIENT_CREDENTIALS_PATH, scopes=OAUTH_SCOPES)
    flow.redirect_uri = request.args.get("redirect_uri")
    authorization_url, google_state = flow.authorization_url(
        access_type='offline',
        prompt='select_account',
        state=docusign_state
    )
    return redirect(authorization_url)


@app.route('/api/docurag/oauth/token', methods=['GET', 'POST'])
def token():
    print(f'request url : {request.url}')
    access_token = uuid4()
    refresh_token = uuid4()
    return {'access_token': access_token, 'refresh_token': refresh_token}


@app.route('/api/docurag/getTypeNames', methods=['GET', 'POST'])
def get_type_names():
    with open('get_type_names.json') as f:
        return json.load(f)


@app.route('/api/docurag/getTypeDefinitions', methods=['GET', 'POST'])
def get_type_definitions():
    with open('get_type_definitions.json') as f:
        return json.load(f)


@app.route('/api/docurag/createRecord', methods=['POST'])
def create_record():
    print(f'create_record request body: {request.json}')
    # save email and idempotencyKey in database
    record_id = __mongodb.create_record(request.json)
    # send a message via email containing a link to the AI RAG chat
    link = DOCURAG_DOMAIN + DOCURAG_CHAT_UI_ENDPOINT + '?_id={}'.format(record_id)
    result = email.send_email(RECEIVER_ACCOUNT_ID, f'link to AI RAG: {link}')
    print(f'result of sending email: {result}')
    return {'recordId': f'{record_id}-success'}


@app.route('/api/docurag/searchRecord', methods=['POST'])
def search_record():
    return {
        "records": [
            {
                "Id": uuid4(),
                "Name": "Signer"
            }
        ]
    }


@app.route('/api/docurag/patchRecord', methods=['POST'])
def patch_record():
    return {'success': True}


@app.route('/api/docurag', methods=['GET'])
def authenticate():
    _id = request.args.get('_id', None)
    if _id is None:
        return jsonify({'error': 'Unauthorized Request'}), 401
    document = __mongodb.get_by_id(_id)
    if document is None:
        return jsonify({'error': 'Unauthorized Request'}), 401
    if check_link.is_expired(document['datetime']):
        return jsonify({'error': 'Bad Request'}), 404

    return redirect(GRADIO_APP_ENDPOINT)


@app.route('/api/docurag/chat', methods=['GET', 'POST'])
def chat_llm():
    message = request.json['message']
    logging.info("message: `%s`", message)
    #
    # resp = __model.chat(message)
    # data = {'answer': resp}
    data = {'answer': 'This is your answer'}

    return data


if __name__ == '__main__':
    # __model = Model()
    # __model.init_rag_corpus('docurag-article1-corpus')
    # __model.init_llm()
    __mongodb = MongoDB('docurag-db', 'appointment')

    app.run(host='0.0.0.0', port=7654, debug=True)
