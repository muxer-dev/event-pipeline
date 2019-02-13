from jsonpointer import resolve_pointer as resolve

from common.logger import logger
from lib.sources import meetup


def handle(event, context):
    logger.info(f"extract: {event}")

    sources = resolve(event, "/sources", [])

    retrieved_events = []

    for source in sources:
        type = source.get("type", None)

        if type == "meetup":
            member_id = resolve(source, "/meetup/member_id", None)
            location = resolve(source, "/location", None)

            events = meetup.get_events_by_member(member_id)

            sourced_events = {"events": events, "type": type, "location": location}

            retrieved_events.append(sourced_events)

    return {"data": retrieved_events}
