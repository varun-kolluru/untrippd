import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")

s3_client = boto3.client("s3",aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY,region_name=AWS_REGION_NAME)

def get_presigned_url_post(key: str):
    try:
        presigned_post =s3_client.generate_presigned_post(
            Bucket=AWS_S3_BUCKET_NAME,
            Key=key,
            Conditions=None,
            ExpiresIn=360
        )
        return {"url": presigned_post["url"], "fields": presigned_post["fields"]}
    except Exception as e:
        return str(e)
    
def get_presigned_url_get(key: str):
    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': AWS_S3_BUCKET_NAME, 'Key': key},
            ExpiresIn=360  # URL expiration time in seconds
        )
        return {"url": presigned_url}
    except Exception as e:
        return str(e)
    

