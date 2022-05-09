import cv2 as open_cv
import imutils
import logging
from config.constants import VIDEO_HEIGHT, VIDEO_WIDTH

def playVideoUsingVideoURL(video):
    # print(f"Video URL: {video}")
    cap = open_cv.VideoCapture(video)
    if (cap.isOpened()== False):
        logging.debug(f"Video URL: {video}")

    while(cap.isOpened()):
        ret, frame = cap.read()
        frame = imutils.resize(frame, VIDEO_WIDTH, VIDEO_HEIGHT)
        if ret == True:
            (flag, encodedImage) = open_cv.imencode('.jpeg', frame)
            if not flag:
                continue
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encodedImage) + b'\r\n')
        else:
            break

    cap.release()
