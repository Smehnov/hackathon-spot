import socket
import os
import numpy as np

HOST_PORT = 8080
HOST_ADDRESS = "localhost"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((HOST_ADDRESS, HOST_PORT))
    print(f"Successfully connected to {HOST_ADDRESS}:{HOST_PORT}")

except Exception as e:
    print(f"Failed to connect to {HOST_ADDRESS}:{HOST_PORT}")
    print(f"Error: {e}")
    s.close()
    exit(1)

buffer = ''

while True:
    data = s.recv(4096)

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
            # depth, visual = spot.capture_depth_and_visual_image('frontleft')
            depth = np.ones((500, 500), dtype=np.uint8)
            visual = np.ones((500, 500), dtype=np.uint8)
            depth_bytes = depth.tobytes()
            visual_bytes = visual.tobytes()
            s.sendall(len(depth_bytes).to_bytes(4, 'little'))
            s.sendall(depth_bytes)
            s.sendall(len(visual_bytes).to_bytes(4, 'little'))
            s.sendall(visual_bytes)
        elif command == "":
            pass
        else:
            pass

s.close()