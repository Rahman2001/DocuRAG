import logging
import sys
from uuid import uuid4

from flask import Flask, redirect
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_session import Session

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
