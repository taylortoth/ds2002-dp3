import boto3
from botocore.exceptions import ClientError

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/kne9xt"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_messages():
    messages = []
    
    try:
        # Receive messages from SQS queue
        while True:
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=['All'],
                MaxNumberOfMessages=10,
                MessageAttributeNames=['All']
            )
            
            if "Messages" in response:
                for message in response['Messages']:
                    order = int(message['MessageAttributes']['order']['StringValue'])
                    word = message['MessageAttributes']['word']['StringValue']
                    handle = message['ReceiptHandle']
                    messages.append({"order": order, "word": word, "handle": handle})
            else:
                break
        
        # Sort messages based on the 'order' attribute
        messages.sort(key=lambda x: x['order'])
        
        # Reassemble the phrase
        phrase = " ".join([message['word'] for message in messages])
        
        # Write the phrase to a file
        with open("phrase.txt", "a") as file:
            file.write(phrase)
        
        print("Phrase reassembled and saved to phrase.txt")
        
        # Delete messages from the queue
        for message in messages:
            delete_message(message['handle'])
    except ClientError as e:
        print(e.response['Error']['Message'])

# Trigger the function
if __name__ == "__main__":
    get_messages()