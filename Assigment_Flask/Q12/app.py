from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Dummy data for demonstration
data_to_send = {"value": 0}

@app.route('/')
def index():
    return render_template('index.html', data=data_to_send)

@socketio.on('update_data')
def handle_update(data):
    global data_to_send
    data_to_send = {"value": data['value']}
    emit('update_data', data_to_send, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)