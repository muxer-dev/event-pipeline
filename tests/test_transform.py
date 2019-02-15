# local imports
from src import transform


def test_transform():
    data = {}
    event = {"data": [data]}

    expected_body = {
        "message": "Your transform function executed successfully!",
        "data": event,
    }
    expected_result = {"statusCode": 200, "body": expected_body}

    result = transform.handle(event, [])
    assert result == expected_result
