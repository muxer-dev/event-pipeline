import json
import os

import boto3
from jsonpointer import resolve_pointer as resolve

from common.logger import logger
from sources import meetup
from util.s3 import upload_to_s3

EXTRACT_BUCKET = os.getenv("EXTRACT_BUCKET")

s3 = boto3.client("s3")


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

    # TODO write to s3
    s3_file_path = None
    if events:
        s3_file_path = upload_to_s3(s3, EXTRACT_BUCKET, events)

    # TODO create file pointer

    return {"pointer": s3_file_path}
