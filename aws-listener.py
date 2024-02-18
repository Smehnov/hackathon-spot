import boto3
import subprocess

# Read credentials from file
with open("rootkey.csv", "r") as file:
    lines = file.readlines()  # Read all lines into a list

    # Skip the header row (assuming it exists)
    header = lines[0]

    # Access the second row (index 1) and split it into cells
    row_data = lines[1].split(",")

    # Extract cells A2 and B2
    access_key = row_data[0]
    secret_key = row_data[1]

# Initialize SQS client
queue_url = 'https://sqs.us-east-2.amazonaws.com/905418297534/MyQueue.fifo'
session = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
sqs = session.client('sqs')

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.output.decode('utf-8')}"

def listen_and_execute():
    # Initial wait time for polling
    wait_time_seconds = 0
    while wait_time_seconds <= 90:
        # Receive messages from the queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            VisibilityTimeout=0,
            WaitTimeSeconds=min(90, 90 - wait_time_seconds)  # Adjusted wait time
        )

        # Check if there are any messages
        if 'Messages' in response:
            for message in response['Messages']:
                # Extract command from the message
                command = message['Body']

                # Execute the command
                result = execute_command(command)

                # Print the result
                print(result)

                # Delete the message from the queue
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )

                # Reset wait time if a message is received
                wait_time_seconds = 0
        else:
            # Increment wait time if no messages received
            wait_time_seconds += 20  # Long polling, waits up to 20 seconds for a message

if __name__ == "__main__":
    listen_and_execute()
