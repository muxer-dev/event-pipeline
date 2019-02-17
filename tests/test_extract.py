from mock import patch

from fixtures.extracted import MEETUP_EXTRACTED_EVENTS
from fixtures.payloads import MEETUP_EVENT
from src import extract


@patch("src.extract.meetup.get_events_by_member")
def test_extract(mock_meetup):
    mock_meetup.return_value = [MEETUP_EVENT]

    event = {
        "sources": [
            {
                "location": "belfast",
                "endpoint": "https://muxer.co.uk/events",
                "type": "meetup",
                "meetup": {"member_id": 123123},
            }
        ]
    }
    expected_result = MEETUP_EXTRACTED_EVENTS

    result = extract.handle(event, [])

    assert result == expected_result
