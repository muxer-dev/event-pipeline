import datetime


def transform_meetup(events, location):
    transformed_events = []
    for event in events:
        start = datetime.datetime.fromtimestamp(int(event["time"] / 1000)).strftime(
            "%Y-%m-%d %H:%M:%SZ"
        )

        # TODO update to end time
        end = datetime.datetime.fromtimestamp(int(event["time"] / 1000)).strftime(
            "%Y-%m-%d %H:%M:%SZ"
        )

        # TODO calculate duration fo event
        duration = 10000

        transformed_events.append(
            {
                "name": event["name"],
                "description": event["description"],
                "url": event["event_url"],
                "start": start,
                "end": end,
                "duration": duration,
                "topics": [],
                "entry": ["free"],
                "category": event["group"]["name"],
                "source": "meetup",
                "location": location,
            }
        )

    return transformed_events
