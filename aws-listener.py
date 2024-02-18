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
    access_key = row_data[0].strip()
    secret_key = row_data[1].strip()

# Initialize SQS client
queue_url = 'https://sqs.us-east-2.amazonaws.com/905418297534/MyQueue.fifo'
session = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name="us-east-2")
sqs = session.client('sqs')

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.output.decode('utf-8')}"

def listen_and_execute():
    remaining_wait_time = 20
    while remaining_wait_time > 0:
        # Short polling, wait up to 5 seconds for a message
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )

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
                remaining_wait_time = 20
                break  # Exit inner loop after processing a message

        # No message received, reduce remaining wait time
        remaining_wait_time -= min(5, remaining_wait_time)

    # No message received after 20 seconds, handle it (log, error, exit)
    print("No message received after", 20, "seconds.")

if __name__ == "__main__":
    listen_and_execute()
