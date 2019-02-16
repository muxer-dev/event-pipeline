from mock import patch

from fixtures.transformed import MEETUP_TRANSFORMED_EVENT
from src import load


@patch("src.load.requests.post")
def test_load(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 200

    event = {
        "sources": [
            {
                "events": [MEETUP_TRANSFORMED_EVENT],
                "type": "meetup",
                "location": "belfast",
            }
        ]
    }

    result = load.handle(event, [])

    expected_result = {"responses": [{"success": 1, "failure": 0}]}

    assert result == expected_result
