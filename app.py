from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    if 'username' not in session:
        session['username'] = f"User_{uuid.uuid4().hex[:6]}"
    return render_template('index.html', username=session['username'])

@socketio.on('message')
def handle_message(data):
    emit('message', {'username': data['username'], 'message': data['message']}, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    emit('typing', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)