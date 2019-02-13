import os

import meetup.api

MEETUP_API_TOKEN = os.getenv("MEETUP_API_TOKEN")

client = meetup.api.Client(MEETUP_API_TOKEN)


def get_events_by_member(id):
    """ Gets events using a given members id.
    """
    response = client.GetEvents({"member_id": id})

    return [event for event in response.results]
