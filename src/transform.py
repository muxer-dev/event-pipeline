import os

import boto3
from jsonpointer import resolve_pointer as resolve

from src.common.logger import logger
from src.transformers.meetup import transform_meetup
from src.util.s3 import read_from_s3, upload_to_s3

SUPPORTED_TYPES = {"meetup": transform_meetup}

TRANSFORM_BUCKET = os.getenv("TRANSFORM_BUCKET")

s3 = boto3.client("s3")


def handle(event, context):
    logger.info(f"transform: {event}")

    bucket = resolve(event, "/bucket", [])
    key = resolve(event, "/key", [])

    file = read_from_s3(s3, bucket, key)

    # TODO for each in file
    events = resolve(file[0], "/events", [])
    type = resolve(file[0], "/type", None)
    location = resolve(file[0], "/location", None)

    transformed_events = []

    if type in SUPPORTED_TYPES:
        transform = SUPPORTED_TYPES.get(type)

        events = transform(events, location)
        payload = {"events": events, "type": "meetup", "location": "belfast"}

        transformed_events.append(payload)

    s3_file_path = None
    if events:
        bucket, key = upload_to_s3(s3, TRANSFORM_BUCKET, transformed_events)
        s3_file_path = f"{bucket}/{key}"

    return {"pointer": s3_file_path, "bucket": bucket, "key": key}
