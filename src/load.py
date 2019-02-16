import json
import os

import requests
from jsonpointer import resolve_pointer as resolve

from src.common.logger import logger

EVENTS_ENDPOINT = os.getenv("EVENTS_ENDPOINT")


def _post_payloads(payloads):
    success = 0
    failures = 0

    for payload in payloads:
        r = requests.post(
            EVENTS_ENDPOINT,
            headers={"Content-type": "application/json"},
            data=json.dumps(payload),
        )
        logger.info(f"post: {r.status_code}")

        if r.status_code == requests.codes.ok:
            success += 1
        else:
            failures += 1

    return {"success": success, "failure": failures}


def handle(event, context):
    logger.info(f"load: {event}")

    sources = resolve(event, "/sources", [])

    responses = []
    for source in sources:
        events = resolve(source, "/events", [])
        responses.append(_post_payloads(events))

    return {"responses": responses}
