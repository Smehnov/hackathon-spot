import boto3

# Read credentials from file
def read_credentials():
    with open('rootkey.csv', 'r') as file:
        lines = file.readlines()
        access_key = lines[1].split(',')[2].strip()
        secret_key = lines[2].split(',')[2].strip()
        return access_key, secret_key

access_key, secret_key = read_credentials()

# Initialize SQS client
sqs = boto3.client('sqs', region_name='us-east-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
queue_url = 'https://sqs.us-east-2.amazonaws.com/905418297534/MyQueue.fifo'

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
