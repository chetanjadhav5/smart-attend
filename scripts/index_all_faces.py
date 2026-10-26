import os
import io
from dotenv import load_dotenv
load_dotenv()
import boto3
from PIL import Image

region = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")
cid = os.environ.get("REKOGNITION_COLLECTION_ID", "raisakshya-attendance")

client = boto3.client(
    "rekognition",
    region_name=region,
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)

def prepare_image(img_path):
    with open(img_path, "rb") as f:
        raw = f.read()
    im = Image.open(io.BytesIO(raw))
    if im.mode in ("RGBA", "P"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        if im.mode == "RGBA":
            bg.paste(im, mask=im.split()[3])
        else:
            bg.paste(im)
        out_buf = io.BytesIO()
        bg.save(out_buf, format="JPEG", quality=95)
        return out_buf.getvalue()
    return raw

def index_folder(folder_path, prefix):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".png")]
    print(f"\nIndexing {len(files)} faces from {folder_path}...")
    for idx, fname in enumerate(files, 1):
        ext_id = f"{prefix}_{idx}_{fname[:8]}"
        img_bytes = prepare_image(os.path.join(folder_path, fname))
        try:
            resp = client.index_faces(
                CollectionId=cid,
                Image={"Bytes": img_bytes},
                ExternalImageId=ext_id,
                MaxFaces=1,
                QualityFilter="AUTO"
            )
            recs = resp.get("FaceRecords", [])
            if recs:
                f_id = recs[0]["Face"]["FaceId"]
                conf = round(recs[0]["Face"]["Confidence"], 1)
                print(f"[{idx}/{len(files)}] Indexed {ext_id} -> FaceId: {f_id} (Conf: {conf}%)")
            else:
                print(f"[{idx}/{len(files)}] {ext_id}: No distinct face found by cloud AI")
        except Exception as e:
            print(f"[{idx}/{len(files)}] Error indexing {ext_id}: {e}")

index_folder(r"d:\project\student faces", "student")
index_folder(r"d:\project\teacher faces", "teacher")
print("\nAll faces indexing run completed!")
