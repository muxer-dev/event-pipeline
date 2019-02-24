import os

from eventbrite import Eventbrite

EVENTBRITE_API_TOKEN = os.getenv("EVENTBRITE_API_TOKEN")

client = Eventbrite(EVENTBRITE_API_TOKEN)


def get_events_by_location(location):
    """ Gets events using a given members id.
    """
    response = client.get(
        f"/events/search/?q=technology&location.address={location}&sort_by=-date"
    )
    events = response["events"]

    return events
