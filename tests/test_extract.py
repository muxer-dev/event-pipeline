from mock import patch

from src import extract

from fixtures.payloads import MEETUP_EVENT


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
    expected_result = {
        "data": [{"events": [MEETUP_EVENT], "type": "meetup", "location": "belfast"}]
    }

    result = extract.handle(event, [])

    assert result == expected_result
