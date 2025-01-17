import logging
import sys

from flask import Flask, url_for, session, redirect
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_session import Session

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google_auth_oauthlib.flow import InstalledAppFlow

from model import *

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app, supports_credentials=True)

__model = None

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/api/docurag/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_secrets_file(
        OAUTH_CLIENT_CREDENTIALS_PATH, scopes=OAUTH_SCOPES)
    flow.redirect_uri = url_for('callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='select_account')

    # Save the state so we can verify the request later
    session['state'] = state
    print(f'session state: {state}')
    return redirect(authorization_url)


@app.route('/api/docurag/oauth/callback', methods=['GET', 'POST'])
def callback():
    # Verify the request state
    if request.args.get('state') != session['state']:
        raise Exception('Invalid state')

    # Create the OAuth flow object
    flow = InstalledAppFlow.from_client_secrets_file(
        OAUTH_CLIENT_CREDENTIALS_PATH, scopes=OAUTH_SCOPES, state=session['state'])
    flow.redirect_uri = url_for('callback', _external=True)

    # Exchange the authorization code for an access token
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Save the credentials to the session
    credentials = flow.credentials
    session['credentials'] = dict(credentials)

    return redirect(url_for('index'))


@app.route('/api/question', methods=['GET'])
def chat_llm():
    question = request.args.get('question')
    logging.info("question: `%s`", question)

    resp = __model.chat(question)
    data = {'answer': resp}

    return jsonify(data), 200


if __name__ == '__main__':
    # __model = Model()
    # __model.init_rag_corpus('docurag-article1-corpus')
    # __model.init_llm()

    app.run(host='0.0.0.0', port=7654, debug=True)
