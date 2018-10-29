from flask import Flask
from flask_socketio import SocketIO
from config import Config


app = Flask(__name__)
socketio = SocketIO(app)


def messageReceived(methods=['GET', 'POST']):
    print('Message was received')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
