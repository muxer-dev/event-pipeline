# local imports
from fixtures.payloads import MEETUP_EVENT
from fixtures.transformed import MEETUP_TRANSFORMED_EVENT
from src import transform


def test_transform():
    event = {
        "data": [{"events": [MEETUP_EVENT], "type": "meetup", "location": "belfast"}]
    }

    expected_result = {
        "data": [
            {
                "events": [MEETUP_TRANSFORMED_EVENT],
                "type": "meetup",
                "location": "belfast",
            }
        ]
    }

    result = transform.handle(event, [])

    assert result == expected_result
