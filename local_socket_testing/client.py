import socket
import numpy as np
import os
import cv2
import time

HOST_PORT = 8080
HOST_ADDRESS = "localhost"


def send_file(file, sock):
    # send 4 byte integer representing number of characters in the filename.
    # send filename.
    # send 4 byte integer representing number of bytes in file.
    # send file contents.

    sock.sendall(len(file).to_bytes(4, 'little'))
    sock.sendall(file.encode('utf-8'))

    with open(file, 'rb') as f:
        bt = f.read()
        sock.sendall(len(bt).to_bytes(4, 'little'))
        sock.sendall(bt)


def take_image_handler(spot, sock, command=None):
    sources = ['back_fisheye_image', 'frontleft_fisheye_image', 'frontright_fisheye_image', 'left_fisheye_image',
               'right_fisheye_image']

    img = 128 * np.ones((512, 512, 3), dtype=np.uint8)
    filename = str(int(time.time() * 1000)) + '_' + 'frontleft_fisheye_image' + '.jpg'
    cv2.imwrite(filename, img)

    send_file(filename, sock)


def move_towards_point_handler(spot, sock, command):
    pass


def asr_handler(spot, sock, command):
    pass


COMMAND_HANDLERS = {'take_image': take_image_handler,
                    'move_towards_point': move_towards_point_handler,
                    'start_asr': asr_handler}


def main():
    spot = "Balls"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((HOST_ADDRESS, HOST_PORT))
        print(f"Successfully connected to {HOST_ADDRESS}:{HOST_PORT}")

    except Exception as e:
        print(f"Failed to connect to {HOST_ADDRESS}:{HOST_PORT}")
        print(f"Error: {e}")
        s.close()
        return

    buffer = ''

    while True:
        data = s.recv(4096)
        if not data:
            print("Disconnected from the server.")
            break

        buffer += data.decode('utf-8')
        while '\n' in buffer:
            command, buffer = buffer.split('\n', 1)

            for comm, handler in COMMAND_HANDLERS.items():
                if comm in command:
                    handler(spot, s, command)
                    break

    s.close()


# 10.19.187.105

if __name__ == '__main__':
    main()


