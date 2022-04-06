import yaml
import logging
from .motion_detector import MotionDetector
from .headless_browse import get_current_data_using_headless_browser
from .coordinates_generator import playVideoUsingVideoURL

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
    print(availability)
    # validate the data and insert to DB
    return availability

def playVideoUsingCameraId(camera_id):
    # write an exception if camera id not exist
    camera_object = get_cameraId_with_coordinates_and_videoURL(camera_id)
    video_url = camera_object['video']

    return playVideoUsingVideoURL(video_url)

