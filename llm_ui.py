import gradio as gr
import requests
from credentials import *


def answer(message, history):
    print(f'message: {message}')
    response = requests.post(DOCURAG_DOMAIN + DOCURAG_CHAT_ENDPOINT,
                             json={"message": message}).json().get('answer')
    print(f'response: {response}')
    return response


chat = gr.ChatInterface(
    answer,
    type="messages"
)
chat.launch(server_name='0.0.0.0', server_port=1243)
