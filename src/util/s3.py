# stdlib imports
import json
import uuid
from datetime import datetime

from jsonpointer import resolve_pointer as resolve


def upload_to_s3(s3, bucket, records):
    file_id = str(uuid.uuid4())
    now = datetime.now().strftime("%Y/%m/%d/%H")
    key = f"{now}/{file_id}.json"

    contents = bytes(json.dumps(records, indent=2).encode("UTF-8"))
    response = s3.put_object(Body=contents, Bucket=bucket, Key=key)

    status_code = resolve(response, "/ResponseMetadata/HTTPStatusCode")
    if status_code < 200 and status_code >= 300:
        raise Exception("Failed to create file on S3")

<<<<<<< HEAD
    return f"{bucket}/{key}"
=======
    return bucket, key


def read_from_s3(s3, bucket, key):
    file_contents = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    response = json.loads(file_contents)

    return response
>>>>>>> e4476bc... Implementing POST step function
