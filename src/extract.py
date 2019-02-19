import os

import boto3
from jsonpointer import resolve_pointer as resolve

from src.common.logger import logger
from src.sources import meetup
from src.util.s3 import upload_to_s3

s3 = boto3.client("s3")

EXTRACT_BUCKET = os.getenv("EXTRACT_BUCKET")


def retrieved_events(sources):
    retrieved_events = []
    for source in sources:
        type = source.get("type", None)

        if type == "meetup":
            member_id = resolve(source, "/meetup/member_id", None)
            location = resolve(source, "/location", None)

            events = meetup.get_events_by_member(member_id)

            sourced_events = {"events": events, "type": type, "location": location}

            retrieved_events.append(sourced_events)

    return retrieved_events


def handle(event, context):
    logger.info(f"extract: {event}")

    sources = resolve(event, "/sources", [])
    events = retrieved_events(sources)

    s3_file_path = None
    if events:
        bucket, key = upload_to_s3(s3, EXTRACT_BUCKET, events)
        s3_file_path = f"{bucket}/{key}"

    return {"pointer": s3_file_path, "bucket": bucket, "key": key}
