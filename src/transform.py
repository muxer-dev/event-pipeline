from jsonpointer import resolve_pointer as resolve

from common.logger import logger

from transformers.meetup import transform_meetup

SUPPORTED_TYPES = {"meetup": transform_meetup}


def handle(event, context):
    logger.info(f"transform: {event}")

    sources = resolve(event, "/data", [])

    transformed_events = []
    for source in sources:
        type = resolve(source, "/type", None)
        location = resolve(source, "/location", None)
        events = resolve(source, "/events", [])

        if type in SUPPORTED_TYPES:
            transform = SUPPORTED_TYPES.get(type)

            events = transform(events, location)
            payload = {"events": events, "type": "meetup", "location": "belfast"}

            transformed_events.append(payload)

    return {"data": transformed_events}
