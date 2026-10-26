import os
from dotenv import load_dotenv
load_dotenv()
import boto3

print("Testing AWS Rekognition with provided credentials...")
region = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")
ak = os.environ.get("AWS_ACCESS_KEY_ID")
sk = os.environ.get("AWS_SECRET_ACCESS_KEY")
cid = os.environ.get("REKOGNITION_COLLECTION_ID", "raisakshya-attendance")

print(f"Region: {region}")
print(f"Access Key: {ak[:4]}...{ak[-4:] if ak else ''}")

client = boto3.client(
    "rekognition",
    region_name=region,
    aws_access_key_id=ak,
    aws_secret_access_key=sk
)

try:
    resp = client.list_collections(MaxResults=10)
    print("SUCCESS! AWS Rekognition connected!")
    colls = resp.get("CollectionIds", [])
    print(f"Existing collections: {colls}")

    if cid not in colls:
        create_resp = client.create_collection(CollectionId=cid)
        print(f"Successfully created collection '{cid}'! ARN: {create_resp.get('CollectionArn')}")
    else:
        print(f"Collection '{cid}' already exists and is active!")
except Exception as e:
    print(f"Error connecting to AWS: {e}")
