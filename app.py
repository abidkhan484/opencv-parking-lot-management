from flask import Flask, render_template, Response, url_for

from flask_socketio import SocketIO, emit
from threading import Thread, Event

from time import sleep

from parking_management.controllers import (
    create_motion_detector_object, 
    get_total_availability, 
    get_current_availability_insert_to_DB,
    CAMERA_ID_WITH_DETECTOR_OBJECTS,
    playVideoUsingCameraId,
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()
def get_parking_space_availability():
    while not thread_stop_event.isSet():
        current_availability = get_total_availability()
        socketio.emit('availability', current_availability, namespace='/availability')
        # try to make it asynchronously
        sleep(2)


@app.route('/')
def homepage():
    camera_ids = [
        'camera1', 
        'camera2'
    ]
    video_urls = [url_for('video_feed', camera_id=camera_id) for camera_id in camera_ids]
    return render_template("index.html", video_urls=video_urls)

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

@app.route("/video_feed/<string:camera_id>")
def video_feed(camera_id):
    if camera_id not in CAMERA_ID_WITH_DETECTOR_OBJECTS:
        create_motion_detector_object(camera_id)
    detector = CAMERA_ID_WITH_DETECTOR_OBJECTS[camera_id]

    return Response(
        detector.detect_motion(), 
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/total-availability-count")
def total_availability_count():
    return get_current_availability_insert_to_DB()

@app.route("/play-video/<string:camera_id>")
def video_without_coordinates(camera_id):
    return Response(
        playVideoUsingCameraId(camera_id), 
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/video-to-image/<string:camera_id>")
def video_to_image_to_set_coordinates(camera_id):
    video_url = url_for('video_without_coordinates', camera_id=camera_id)
    return render_template("video-to-image.html", video_url=video_url)

@app.route("/preview-image")
def preview_image_to_set_coordinates():
    return render_template("preview-image.html")

if __name__ == '__main__':
    socketio.run(app)

