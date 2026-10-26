import os
from dotenv import load_dotenv
load_dotenv()
import boto3
from PIL import Image
import io

region = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")
cid = os.environ.get("REKOGNITION_COLLECTION_ID", "raisakshya-attendance")

client = boto3.client(
    "rekognition",
    region_name=region,
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)

test_img_path = r"d:\project\student faces\268e4791-61db-45cb-b948-2a40ce6e5374.png"
with open(test_img_path, "rb") as f:
    raw_bytes = f.read()

# Convert RGBA to RGB with white background just in case
im = Image.open(io.BytesIO(raw_bytes))
if im.mode in ("RGBA", "P"):
    bg = Image.new("RGB", im.size, (255, 255, 255))
    if im.mode == "RGBA":
        bg.paste(im, mask=im.split()[3])
    else:
        bg.paste(im)
    out_buf = io.BytesIO()
    bg.save(out_buf, format="JPEG", quality=95)
    img_bytes = out_buf.getvalue()
else:
    img_bytes = raw_bytes

print("Attempting to index test face in AWS Rekognition...")
try:
    resp = client.index_faces(
        CollectionId=cid,
        Image={"Bytes": img_bytes},
        ExternalImageId="student_01_Aarav",
        MaxFaces=1,
        QualityFilter="AUTO"
    )
    records = resp.get("FaceRecords", [])
    if records:
        face = records[0]["Face"]
        print(f"SUCCESS! Indexed face in AWS Rekognition:")
        print(f"FaceId: {face.get('FaceId')}")
        print(f"Confidence: {face.get('Confidence')}")
    else:
        print("Note: AWS Rekognition found 0 faces in 3D stylized avatar. Unindexed faces can still be compared 1-to-1.")
except Exception as e:
    print(f"Index faces error: {e}")
