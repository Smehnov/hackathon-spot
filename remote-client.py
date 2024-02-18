import socket
import json

# Define the IP address and port of the module running on the Spot
MODULE_IP = '0.0.0.0'  # Replace with the actual IP address
MODULE_PORT = 12345  # Replace with the actual port

def send_spot_instructions(instructions):
    try:
        # Create a socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((MODULE_IP, MODULE_PORT))

            # Convert instructions to JSON format
            instructions_json = json.dumps(instructions)

            # Send instructions to the module
            s.sendall(instructions_json.encode())

            # Receive response from the module if needed
            # response = s.recv(1024)
            # print("Response:", response.decode())

    except Exception as e:
        print("An error occurred while sending instructions to Spot:", e)

# Example instructions to move Spot forward by 0.5 meters
instructions = {
    "action": "move_forward",
    "distance": 0.5
}

# Send instructions to Spot
send_spot_instructions(instructions)

# Listen for more instructions and send them to Spot as needed
while True:
    # User input
    action = input("Enter an action for Spot (e.g., move_forward, turn_left, etc.): ")
    distance = float(input("Enter the distance or angle for the action: "))
    instructions = {
        "action": action,
        "distance": distance
    }

    # Send instructions to Spot
    send_spot_instructions(instructions)

