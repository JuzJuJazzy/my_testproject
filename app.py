from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    response = 'Server: You said - ' + message
    emit('response_message', response, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
