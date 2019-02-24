def transform(events, location):
    transformed_events = []
    for event in events:
        # TODO calculate duration fo event
        duration = 10000

        transformed_events.append(
            {
                "name": event["name"]["text"],
                "description": event["description"]["text"],
                "url": event.get("url", ""),
                "start": event["start"]["utc"],
                "end": event["end"]["utc"],
                "duration": duration,
                "topics": [],
                "entry": ["ticket"],
                "category": event["name"]["text"],
                "source": "eventbrite",
                "location": location,
            }
        )

    return transformed_events
