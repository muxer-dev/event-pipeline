import json
import math
import os
import threading
from threading import Thread

import requests

import boto3
from jsonpointer import resolve_pointer as resolve
from src.common.logger import logger
from src.util.s3 import read_from_s3

EVENTS_ENDPOINT = os.getenv("EVENTS_ENDPOINT")


s3 = boto3.client("s3")


def WorkerThread(identifier, events):
    event_size = len(events)
    logger.info(f"sending {event_size} from thread {identifier}")
    dispatch_payloads(events)
    logger.info(f"finished sending {event_size} from thread {identifier}")


def chunkify(l, n):
    """Yield n number of striped chunkify from l."""
    for i in range(0, n):
        yield l[i::n]


def dispatch_payloads(payloads):
    for payload in payloads:
        response = requests.post(
            EVENTS_ENDPOINT,
            headers={"Content-type": "application/json"},
            data=json.dumps(payload),
        )
        logger.info(f"post: {response.status_code}")

        if response.status_code < 200 or response.status_code >= 300:
            logger.info(f"failed: {payload} {response.status_code}")


def handle(event, context):
    logger.info(f"load: {event}")

    bucket = resolve(event, "/bucket", [])
    key = resolve(event, "/key", [])

    file = read_from_s3(s3, bucket, key)

    events = resolve(file[0], "/events", [])

    total_events = len(events)
    partition_size = math.ceil(total_events / 10)
    partitions = chunkify(events, partition_size)

    worker_threads = []
    for index, partition in enumerate(partitions):
        worker_thread = Thread(target=WorkerThread, args=(index, partition))
        worker_threads.append(worker_thread)
        worker_thread.start()

    while threading.active_count() > 1:
        for worker_thread in worker_threads:
            worker_thread.join()

    logger.info(f"finished sending {total_events} events")

    return {"responses": []}
