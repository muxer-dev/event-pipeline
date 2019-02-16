# local imports
from src import load


def test_load():
    data = {}
    event = {"data": [data]}

    expected_body = {
        "message": "Your load function executed successfully!",
        "data": event,
    }
    expected_result = {"statusCode": 200, "body": expected_body}

    result = load.handle(event, [])
    assert result == expected_result
