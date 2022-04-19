from flask import Flask
from flask_socketio import SocketIO
import logging
from parking_management import socketio
from parking_management.urls import parking_bp


def create_app():
    app = Flask(__name__)
    # app.config['SECRET_KEY'] = 'secret!'
    # app.config['DEBUG'] = True
    logging.basicConfig(level=logging.INFO)

    ## Initialize Config
    app.config.from_pyfile('config/config.py')
    app.register_blueprint(parking_bp, url_prefix='/')

    socketio.init_app(app)

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    # app.run(host='0.0.0.0', port=port)
    socketio.run(host='0.0.0.0', port=port)
