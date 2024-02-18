import os
import time
from spot_controller import SpotController
import socket
import threading
import numpy as np

ROBOT_IP = "10.0.0.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']

HOST_PORT = 8080
HOST_ADDRESS = os.environ['HOST_ADDRESS']


def main():
    #example of using micro and speakers
    print("Start recording audio")
    sample_name = "aaaa.wav"
    cmd = f'arecord -vv --format=cd --device={os.environ["AUDIO_INPUT_DEVICE"]} -r 48000 --duration=10 -c 1 {sample_name}'
    print(cmd)
    os.system(cmd)
    print("Playing sound")
    os.system(f"ffplay -nodisp -autoexit -loglevel quiet {sample_name}")

    # Capture image
    import cv2
    camera_capture = cv2.VideoCapture(0)
    rv, image = camera_capture.read()
    print(f"Image Dimensions: {image.shape}")
    camera_capture.release()

    with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:

        time.sleep(1)

        # Move head to specified positions with intermediate time.sleep
        spot.move_head_in_points(yaws=[0.2, 0],
                                 pitches=[0.3, 0],
                                 rolls=[0.4, 0],
                                 sleep_after_point_reached=1)

        time.sleep(1)

        # # Make Spot to move by goal_x meters forward and goal_y meters left
        # spot.move_to_goal(goal_x=0.5, goal_y=0)
        # time.sleep(3)
        #
        # # Control Spot by velocity in m/s (or in rad/s for rotation)
        # spot.move_by_velocity_control(v_x=-0.3, v_y=0, v_rot=0, cmd_duration=2)
        # time.sleep(3)

        if spot is None:
            print("Failed to initialize Spot")
            return

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((HOST_ADDRESS, HOST_PORT))
            print(f"Successfully connected to {HOST_ADDRESS}:{HOST_PORT}")

            # You can send and receive data here using s.sendall() and s.recv()
            # Example: s.sendall(b'Hello, server')
        except Exception as e:
            print(f"Failed to connect to {HOST_ADDRESS}:{HOST_PORT}")
            print(f"Error: {e}")
            s.close()
            return

        buffer = ''

        while True:
            data = s.recv(2**12)

            print(f"received: {data.decode('utf-8')}")

            if not data:
                print("Disconnected from the server.")
                break

            buffer += data.decode('utf-8')

            print(f"buffer: {buffer}")

            while '\n' in buffer:
                command, buffer = buffer.split('\n', 1)

                print(f"command: {command}")

                if command == "take_image":
                    depth, visual = spot.capture_depth_and_visual_image('frontleft')
                    depth_bytes = depth.tobytes()
                    visual_bytes = visual.tobytes()
                    s.send(len(depth_bytes).to_bytes(4, 'little'))
                    s.send(depth_bytes)
                    s.send(len(visual_bytes).to_bytes(4, 'little'))
                    s.send(visual_bytes)
                elif command == "":
                    pass
                else:
                    pass

        s.close()


# 10.19.187.105

if __name__ == '__main__':
    main()
