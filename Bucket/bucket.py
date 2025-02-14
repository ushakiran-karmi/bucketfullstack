import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Debug: Print environment variables
print("AWS_ACCESS_KEY:", os.getenv("AWS_ACCESS_KEY"))
print("AWS_SECRET_KEY:", os.getenv("AWS_SECRET_KEY"))
print("AWS_REGION:", os.getenv("AWS_REGION"))

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# FastAPI instance
app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; replace with ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Request model for validation
class BucketRequest(BaseModel):
    bucket_name: str

@app.post("/create-bucket/")
def create_bucket(request: BucketRequest):
    """
    Creates an S3 bucket via FastAPI POST request.
    """
    bucket_name = request.bucket_name.strip()

    if not bucket_name:
        raise HTTPException(status_code=400, detail="Bucket name cannot be empty.")

    if not AWS_REGION:
        raise HTTPException(status_code=500, detail="AWS_REGION is not set in the environment variables.")

    try:
        # Configure the S3 client
        if AWS_REGION == "us-east-1":
            print("EXecute it")
            s3_client = boto3.client(
                "s3",
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY
            )
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY,
                region_name=AWS_REGION
            )
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": AWS_REGION}
            )

        return {"message": f"Bucket '{bucket_name}' created successfully in region '{AWS_REGION}'!"}

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"ClientError: {e}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {e}")