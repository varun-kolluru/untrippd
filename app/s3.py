import os
from dotenv import load_dotenv
import aioboto3

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")

session = aioboto3.Session()

async def get_presigned_url_post(key: str):
    async with session.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    ) as s3_client:
        try:
            presigned_post = await s3_client.generate_presigned_post(
                Bucket=AWS_S3_BUCKET_NAME,
                Key=key,
                Conditions=None,
                ExpiresIn=360
            )
            return {"url": presigned_post["url"], "fields": presigned_post["fields"]}
        except Exception as e:
            return str(e)
    
async def get_presigned_url_get(key: str):
    async with session.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    ) as s3_client:
        try:
            presigned_url = await s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': AWS_S3_BUCKET_NAME, 'Key': key},
                ExpiresIn=360  # URL expiration time in seconds
            )
            return {"url": presigned_url}
        except Exception as e:
            return str(e)
    
async def delete_s3_file(key: str):
    async with session.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    ) as s3_client:
        try:
            response =await s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=key)
            return str(response)
        except Exception as e:
            return str(e)
        

    

