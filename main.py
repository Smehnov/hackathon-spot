import os
import time
from spot_controller import SpotController
import cv2
from req import fetch

ROBOT_IP = "10.0.0.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']


def capture_image():
    camera_capture = cv2.VideoCapture(0)
    rv, image = camera_capture.read()
    print(f"Image Dimensions: {image.shape}")
    camera_capture.release()
    cv2.imwrite(f'/merklebot/job_data/camera_{time.time()}.jpg', image)


def main():
    with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:
        capture_image()
        for i in range(2):
            spot.move_by_velocity_control(1, 1, 10, 10)
            capture_image()


if __name__ == '__main__':
    main()
