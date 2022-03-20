from flask import Flask, render_template, Response
import yaml
from motion_detector import MotionDetector
import logging

from flask_socketio import SocketIO, emit
from threading import Thread, Event

from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()
def get_parking_space_availability():
    while not thread_stop_event.isSet():
        socketio.emit('availability', {'occupied': str(MotionDetector.OCCUPIED), 'available': str(MotionDetector.LENGTH - MotionDetector.OCCUPIED)}, namespace='/availability')
        # try to make it asynchronously
        sleep(2)


@app.route('/')
def hello():
    return render_template("index.html")

@socketio.on('connect', namespace='/availability')
def availability_websocket_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(get_parking_space_availability)

@socketio.on('disconnect', namespace='/availability')
def availability_websocket_disconnect():
    print('Client disconnected')

@app.route("/video_feed")
def video_feed():
    # make the data file and set in the below variable
    data_file = 'data/availability3.yml'
    start_frame = 400

    with open(data_file, "r") as data:
        points = yaml.safe_load(data)
        # set the video file in the below method
        detector = MotionDetector(
            'videos/parking_video7.mp4', points, int(start_frame))
        return Response(detector.detect_motion(),
                        mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    socketio.run(app)

