import yaml
import logging
from flask import url_for
from parking_management.video_processor.motion_detector import MotionDetector
from parking_management.video_processor.coordinates_generator import playVideoUsingVideoURL
from .headless_browse import get_current_data_using_headless_browser

from .models import CameraDetails

CAMERA_ID_WITH_DETECTOR_OBJECTS = {}

def create_motion_detector_object(camera_id):
    camera_details = get_cameraId_with_coordinates_and_videoURL(camera_id)
    # return proper response if coordinates not found
    with open(camera_details['coordinates'], "r") as data:
        points = yaml.safe_load(data)
        detector = MotionDetector(camera_details['video'], points)
        if camera_id not in CAMERA_ID_WITH_DETECTOR_OBJECTS:
            CAMERA_ID_WITH_DETECTOR_OBJECTS[camera_id] = detector

def get_total_availability():
    occupied, available = 0, 0
    availability = {'occupied': 0, 'available': 0}
    for slot in CAMERA_ID_WITH_DETECTOR_OBJECTS:
        camera_details = CAMERA_ID_WITH_DETECTOR_OBJECTS[slot].get_current_availability()
        availability['available'] += camera_details['available']
        availability['occupied'] += camera_details['occupied']

    return {'occupied': str(availability['occupied']), 'available': str(availability['available'])}

def get_all_camera_info():
    all_camera_object = CameraDetails.query.all()
    all_camera_details = []
    count = 0
    for camera_info in all_camera_object:
        count += 1
        all_camera_details.append({
            'SL': count,
            'camera_url': camera_info.camera_url,
            'coordinates_path': camera_info.coordinates,
            'edit_url': url_for(
                "parking_management.video_to_image_to_set_coordinates", 
                camera_id=camera_info.id
            ),
            'delete_url': url_for("parking_management.delete_camera_info", camera_id=camera_info.id),
        })
    return all_camera_details

def add_new_camera_info(camera_url, coordinates=None):
    pass

def delete_camera_info(camera_id):
    # write the delete query
    status = CameraDetails.query.filter_by(camera_id=camera_id).first_or_404()
    return status

def edit_camera_info(camera_id):
    # write the update query
    status = CameraDetails.query.filter(camera_id=camera_id)
    return status

def get_cameraId_with_coordinates_and_videoURL(camera_id):
    cameraId_with_coordinates_and_videoURL = {
        'camera1': {
            'coordinates': 'data/availability3.yml',
            'video': 'videos/parking_video7.mp4'
        },
        'camera2': {
            'coordinates': 'data/coordinates_1.yml',
            'video': 'videos/parking_lot_1.mp4'
        }
    }

    return cameraId_with_coordinates_and_videoURL[camera_id] \
        if camera_id in cameraId_with_coordinates_and_videoURL \
            else {'coordinates': '', 'video': ''}

def get_current_availability_insert_to_DB():
    availability = get_current_data_using_headless_browser()
    logging.info(f"Availability are {availability}")
    # validate the data and insert to DB
    return availability

def playVideoUsingCameraId(camera_id):
    # write an exception if camera id not exist
    camera_object = get_cameraId_with_coordinates_and_videoURL(camera_id)
    video_url = camera_object['video']

    return playVideoUsingVideoURL(video_url)

def generate_video_and_coordinates_url_for_homepage(camera_ids):
    video_urls, coordinates_generator_urls = [], []
    for camera_id in camera_ids:
        camera_details = get_cameraId_with_coordinates_and_videoURL(camera_id)
        if camera_details['coordinates']:
            video_urls.append(
                url_for('parking_management.video_feed', camera_id=camera_id)
            )
        else:
            video_urls.append(
                url_for('parking_management.video_without_coordinates', camera_id=camera_id)
            )

        coordinates_generator_urls.append(
            url_for('parking_management.video_to_image_to_set_coordinates', camera_id=camera_id)
        )

    logging.debug(f"Generated video URLs" + ", ".join(video_urls))
    logging.debug(f"Generated empty coordinates video URLs" + ", ".join(coordinates_generator_urls))


    return [video_urls, coordinates_generator_urls]
