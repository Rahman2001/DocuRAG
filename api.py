import logging
import sys

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from model import *

app = Flask(__name__)
CORS(app)

__model = None

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/api/question', methods=['GET'])
def chat_llm():
    question = request.args.get('question')
    logging.info("question: `%s`", question)

    resp = __model.chat(question)
    data = {'answer': resp}

    return jsonify(data), 200


if __name__ == '__main__':
    __model = Model()
    __model.init_rag_corpus('docurag-article1-corpus')
    __model.init_llm()

    app.run(host='0.0.0.0', port=7654, debug=True)
