import socket
import threading
import struct


ROTATION_ANGLE = {
    'back_fisheye_image': 0,
    'frontleft_fisheye_image': -78,
    'frontright_fisheye_image': -102,
    'left_fisheye_image': 0,
    'right_fisheye_image': 180
}


def read_from_client(client_socket, address, file_name_prefix):
    i = 0
    try:
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

    except Exception as e:
        print(f"Error reading from {address}: {e}")


def handle_client_connection(client_socket: socket.socket, address, file_name_prefix):
    try:
        with client_socket:
            print(f"Connection from {address} has been established.")

            # Create and start the reading thread
            reading_thread = threading.Thread(
                target=read_from_client,
                args=(client_socket, address, file_name_prefix))
            reading_thread.start()

            while True:
                command = input("Enter command: ")
                if command == "ligma":
                    break
                client_socket.sendall((command + '\n').encode('utf-8'))

            # Wait for the reading thread to finish before closing the connection
            reading_thread.join()
    except Exception as e:
        print(f"An error occurred with the client {address}: {e}")


def start_server(host, port, file_name_prefix):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, address = server_socket.accept()
            # For each connection, create a new thread to handle the client
            client_thread = threading.Thread(target=handle_client_connection,
                                             args=(client_socket, address, file_name_prefix))
            client_thread.start()


# Configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 8080  # Port number to listen on
FILE_NAME_PREFIX = 'received_data'  # Prefix for the file names where data is stored

# Start the server
if __name__ == "__main__":
    start_server(HOST, PORT, FILE_NAME_PREFIX)
