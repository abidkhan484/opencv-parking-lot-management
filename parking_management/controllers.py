import yaml
from .motion_detector import MotionDetector

CAMERA_ID_WITH_DETECTOR_OBJECTS = {}

def create_motion_detector_object(camera_id):
    camera_details = get_cameraId_with_coordinates_and_videoURL(camera_id)
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
    return cameraId_with_coordinates_and_videoURL[camera_id]


