import socket
from threading import Thread, Lock
import struct
import enum


ROTATION_ANGLE = {
    'back_fisheye_image': 0,
    'frontleft_fisheye_image': -78,
    'frontright_fisheye_image': -102,
    'left_fisheye_image': 0,
    'right_fisheye_image': 180
}


class RobotStates(enum):
    WAITING_FOR_COMMAND = 1  # commands are of the form take me to something
    TARGETING = 2  # back and forth between robot and server with yolo and images
    WALKING = 3  # robot is facing towards the target and will start walking


robot_state = RobotStates.WAITING_FOR_COMMAND
robot_state_mutex = Lock()


def int_from_bytes(bytes,):
    return struct.unpack('<I', bytes)[0]



def handle_new_file(file):
    pass


def read_from_client(client_socket, address, file_name_prefix):
    i = 0
    while True:  # Continually read messages
        # Read the length of the incoming message (4 bytes, little endian)
        length_bytes = client_socket.recv(4)
        if not length_bytes:
            print("Connection closed by the client.")
            break  # Exit the loop if no data is received (connection closed)

        # Unpack the length to an integer
        length = struct.unpack('<I', length_bytes)[0]
        print(f"Expecting {length} bytes of data.")

        # Initialize an empty byte array for the data
        data = b''

        # Read the specified amount of data
        while len(data) < length:
            chunk = client_socket.recv(length - len(data))
            if not chunk:
                print("Connection closed by the client during data reception.")
                break  # Exit the loop if no data is received (connection closed)
            data += chunk

        # Write the data to a file
        file_name = f"{file_name_prefix}_{address[0]}_{address[1]}_{i}.bin"
        i += 1
        with open(file_name, 'ab') as file:  # Append mode
            file.write(data)
            print(f"Data written to {file_name}")


def handle_client_connection(client_socket: socket.socket, address, file_name_prefix):
    with client_socket:
        print(f"Connection from {address} has been established.")

        # Create and start the reading thread
        reading_thread = Thread(
            target=read_from_client,
            args=(client_socket, address, file_name_prefix))
        reading_thread.start()

        while True:
            command = input("Enter command: ")
            if command == "ligma":
                break
            client_socket.sendall((command + '\n').encode('utf-8'))

        reading_thread.join()


def start_server(host, port, file_name_prefix):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Server listening on {host}:{port}")

        # only accept one connection, end after one connection
        client_socket, address = server_socket.accept()
        handle_client_connection(client_socket, address, file_name_prefix)



HOST = '0.0.0.0'
PORT = 8080
FILE_NAME_PREFIX = 'received_data'

# Start the server
if __name__ == "__main__":
    start_server(HOST, PORT, FILE_NAME_PREFIX)
