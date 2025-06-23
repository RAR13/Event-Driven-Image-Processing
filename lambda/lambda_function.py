import boto3
from PIL import Image
import os
import io
import logging

logging.basicConfig(level=logging.INFO)
s3 = boto3.client('s3')
DEST_BUCKET = "image-processing-destination-rose01"

def lambda_handler(event, context):
    logging.info(f"Received event: {event}")

    try:
        # Extract bucket and object key from the event
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        logging.info(f"Fetching image '{key}' from bucket '{source_bucket}'")

        # Download the image from S3
        response = s3.get_object(Bucket=source_bucket, Key=key)
        image_content = response['Body'].read()

        # Open and resize the image
        image = Image.open(io.BytesIO(image_content))
        image = image.resize((100, 100))
        logging.info("Image resized successfully")

        # Save the resized image to a buffer
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)

        # Create a new filename and upload to destination bucket
        dest_key = f"resized-{os.path.basename(key)}"
        s3.put_object(Bucket=DEST_BUCKET, Key=dest_key, Body=buffer)
        logging.info(f"Uploaded resized image to '{DEST_BUCKET}/{dest_key}'")

        return {
            'statusCode': 200,
            'body': f"Image processed and uploaded to {DEST_BUCKET}/{dest_key}"
        }

    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }