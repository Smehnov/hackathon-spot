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
        response = fetch("/", method='POST')
        print(response)

        capture_image()
        spot.move_head_in_points(yaws=[0.2, 0],
                                 pitches=[0.3, 0],
                                 rolls=[0.4, 0],
                                 sleep_after_point_reached=1)
        capture_image()
        spot.move_head_in_points(yaws=[0, 0.4],
                                 pitches=[0, 0.5],
                                 rolls=[0, 0.7],
                                 sleep_after_point_reached=1)


        


if __name__ == '__main__':
    main()
