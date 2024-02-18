import boto3

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

def send_message(message):
    try:
        # Send message to the queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )
        print(f"Message sent: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    # Prompt user to enter a message
    message = input("Enter message to send: ")

    # Send the message to the queue
    send_message(message)
