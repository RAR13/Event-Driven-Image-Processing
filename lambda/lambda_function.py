import boto3
from PIL import Image
import os
import io

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    # Get bucket and object key
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    dest_bucket = source_bucket + '-processed'
    
    # Download the image
    response = s3.get_object(Bucket=source_bucket, Key=key)
    image_content = response['Body'].read()
    
    # Resize image
    image = Image.open(io.BytesIO(image_content))
    image = image.resize((100, 100))
    
    # Save to buffer
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    
    # Upload to destination bucket
    s3.put_object(Bucket=dest_bucket, Key=key, Body=buffer)
    
    return {
        'statusCode': 200,
        'body': f'Image processed and uploaded to {dest_bucket}'
    }