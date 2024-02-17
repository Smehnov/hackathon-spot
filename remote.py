import socket
import json
from spot_controller import SpotController

# Define the IP address and port for the server to listen on
SERVER_IP = '0.0.0.0'  # Listen on all available network interfaces
SERVER_PORT = 12345  # Choose a port number for communication

# Initialize SpotController with your credentials and robot IP
SPOT_USERNAME = "admin"
SPOT_PASSWORD = "2zqa8dgw7lor"
ROBOT_IP = "10.0.0.3"

def handle_client_connection(client_socket):
    try:
        # Receive data from the client
        data = client_socket.recv(1024).decode()

        # Parse the received JSON data
        instructions = json.loads(data)

        # Perform the action based on the instructions received
        if instructions["action"] == "move_forward":
            distance = instructions["distance"]
            # Move Spot forward by the specified distance
            # Example: spot.move_to_goal(goal_x=distance, goal_y=0)
            print(f"Moving Spot forward by {distance} meters")

        # You can add more actions here based on your requirements

        # Send a response back to the client if needed
        # client_socket.sendall(b"Instruction received and executed successfully")

    except Exception as e:
        print("An error occurred while processing client instructions:", e)

    finally:
        # Close the client socket
        client_socket.close()

def start_server():
    # Create a socket for the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the specified IP address and port
        server_socket.bind((SERVER_IP, SERVER_PORT))

        # Listen for incoming connections
        server_socket.listen(5)
        print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

        while True:
            # Accept incoming connections
            client_socket, _ = server_socket.accept()
            print("Client connected")

            # Handle the client connection in a separate thread or process
            handle_client_connection(client_socket)

# Main function
if __name__ == "__main__":
    start_server()
