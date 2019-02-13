from mock import patch

from lib import extract


@patch("lib.extract.meetup.get_events_by_member")
def test_extract(mock_meetup):
    mock_meetup.return_value = [{"example": "data"}]

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
        "data": [
            {"events": [{"example": "data"}], "type": "meetup", "location": "belfast"}
        ]
    }

    result = extract.handle(event, [])

    assert result == expected_result
