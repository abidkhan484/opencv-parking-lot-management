from flask import Flask, render_template, Response

from flask_socketio import SocketIO, emit
from threading import Thread, Event

from time import sleep

from parking_management.controllers import play_video, get_current_availability

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()
def get_parking_space_availability():
    while not thread_stop_event.isSet():
        current_availability = get_current_availability()
        socketio.emit('availability', current_availability, namespace='/availability')
        # try to make it asynchronously
        sleep(2)


@app.route('/')
def hello():
    return render_template("index.html")

@socketio.on('connect', namespace='/availability')
def availability_websocket_connect():
    global thread
    print('Client connected')

    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(get_parking_space_availability)

@socketio.on('disconnect', namespace='/availability')
def availability_websocket_disconnect():
    print('Client disconnected')

@app.route("/video_feed")
def video_feed():
    return Response(play_video(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/total-availability-count")
def total_availability_count():
    pass

if __name__ == '__main__':
    socketio.run(app)

