from flask import render_template, Response, url_for, Blueprint, request, redirect, flash
from flask_socketio import SocketIO, emit
from threading import Thread, Event
import logging
from time import sleep
from . import socketio, db
from .models import CameraDetails


from parking_management.controllers import (
    create_motion_detector_object, 
    get_total_availability, 
    get_current_availability_insert_to_DB,
    CAMERA_ID_WITH_DETECTOR_OBJECTS,
    playVideoUsingCameraId,
    generate_video_and_coordinates_url_for_homepage,
    get_all_camera_info,
    insert_camera_info_to_DB,
    edit_camera_info_using_id,
    delete_camera_info_using_id,
)


parking_bp = Blueprint('parking_management', __name__)


thread = Thread()
thread_stop_event = Event()
def get_parking_space_availability():
    while not thread_stop_event.isSet():
        current_availability = get_total_availability()
        socketio.emit('availability', current_availability, namespace='/availability')
        # try to make it asynchronously
        sleep(0.5)


@parking_bp.route('/')
def homepage():
    camera_ids = [
        '1', 
        '3'
    ]

    [video_urls, coordinates_generator_urls] = generate_video_and_coordinates_url_for_homepage(camera_ids)

    return render_template(
        "index.html",
        camera_ids=camera_ids,
        video_urls=video_urls,
        coordinates_generator_urls=coordinates_generator_urls
    )

@socketio.on('connect', namespace='/availability')
def availability_websocket_connect():
    global thread
    logging.debug('Client connected')

    if not thread.isAlive():
        logging.debug("Starting Thread")
        thread = socketio.start_background_task(get_parking_space_availability)

@socketio.on('disconnect', namespace='/availability')
def availability_websocket_disconnect():
    logging.debug('Client disconnected')

@parking_bp.route("/video_feed/<string:camera_id>")
def video_feed(camera_id):
    if camera_id not in CAMERA_ID_WITH_DETECTOR_OBJECTS:
        create_motion_detector_object(camera_id)
    detector = CAMERA_ID_WITH_DETECTOR_OBJECTS[camera_id]

    return Response(
        detector.detect_motion(), 
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@parking_bp.route("/total-availability-count")
def total_availability_count():
    return get_current_availability_insert_to_DB()

@parking_bp.route("/play-video/<string:camera_id>")
def video_without_coordinates(camera_id):
    return Response(
        playVideoUsingCameraId(camera_id), 
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@parking_bp.route("/video-to-image/<string:camera_id>")
def video_to_image_to_set_coordinates(camera_id):
    video_url = url_for('parking_management.video_without_coordinates', camera_id=camera_id)
    return render_template("video-to-image.html", video_url=video_url)

@parking_bp.route("/all-camera")
def get_all_camera():
    all_camera_details = get_all_camera_info()
    add_camera_url = url_for("parking_management.add_camera_form")
    return render_template(
        "camera-listing.html", 
        all_camera_details=all_camera_details, 
        add_camera_url=add_camera_url
    )

@parking_bp.route("/add-camera")
def add_camera_form():
    camera_post_url = url_for("parking_management.add_new_camera_info")
    return render_template("add-camera.html", camera_post_url=camera_post_url)

@parking_bp.route("/add-new-camera", methods=("POST",))
def add_new_camera_info():
    # add validation
    camera_url = request.form.get("camera_url")
    status = insert_camera_info_to_DB(camera_url)
    if status:
        flash("New camera added successfully.")
    else:
        flash("Camera added failed")
    return redirect(url_for("parking_management.add_camera_form"))

@parking_bp.route("/edit-coordinates/<string:camera_id>", methods=("POST",))
def update_coordinates_of_camera_info(camera_id):
    coordinates = request.get_json()
    coordinates = coordinates['coordinates'] if coordinates else []
    resp = edit_camera_info_using_id(camera_id=camera_id, coordinates=coordinates)
    return Response({'success': True}) if resp else Response({'success': False})

@parking_bp.route("/delete-camera/<string:camera_id>")
def delete_camera_info(camera_id):
    resp = delete_camera_info_using_id(camera_id=camera_id)
    return redirect(url_for("parking_management.get_all_camera"))

