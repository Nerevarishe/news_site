from flask import Flask, escape
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app)


def messageReceived():
    print('Message was received')


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received my event: ' + str(json))

    # TODO: Убедиться в безопасности - всё ли экранирует функция
    def escape_html(json):
        response = {}
        for k, v in json.items():
            d = {k: escape(v)}
            response.update(d)
        return response

    socketio.emit('my response', escape_html(json), callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
