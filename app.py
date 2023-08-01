from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    response_gpt = chat_with_gpt3(message)
    response = 'Server:' + response_gpt
    emit('response_message', response, broadcast=True)

def chat_with_gpt3(prompt):
    api_key = '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'  # my_project ใส่ API key ที่ได้รับจาก OpenAI ที่นี่
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt},
        ],
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.json()['error']['message']}"


if __name__ == '__main__':
    socketio.run(app)
