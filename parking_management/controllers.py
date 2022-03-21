import yaml
from .motion_detector import MotionDetector

def play_video():
    # make the data file and set in the below variable
    data_file = 'data/availability3.yml'
    start_frame = 400

    with open(data_file, "r") as data:
        points = yaml.safe_load(data)
        # set the video file in the below method
        detector = MotionDetector(
            'videos/parking_video7.mp4', points, int(start_frame))
        return detector.detect_motion()

def get_current_availability():
    return {'occupied': str(MotionDetector.OCCUPIED), 'available': str(MotionDetector.LENGTH - MotionDetector.OCCUPIED)}

def play_all_videos():
    video_objects = {
        'camera1': {
            'coordinates': 'data/availability3.yml',
            'video': 'videos/parking_video7.mp4'
        }
    }



