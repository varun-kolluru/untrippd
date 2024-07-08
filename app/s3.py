import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
from fastapi import HTTPException
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

async def upload_image_to_s3(file: UploadFile):
    try:
        file_extension = file.filename.split(".")[-1]
        file_key = f"{uuid.uuid4()}.{file_extension}"

        s3.upload_fileobj(
            file.file,
            AWS_S3_BUCKET_NAME,
            file_key,
            ExtraArgs={"ContentType": file.content_type}
        )
        return f"https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{file_key}"
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="AWS credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
