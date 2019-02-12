# local imports
from lib import extract


def test_extract():
    data = {}
    event = {"data": [data]}

    expected_body = {
        "message": "Your extract function executed successfully!",
        "data": event,
    }
    expected_result = {"statusCode": 200, "body": expected_body}

    result = extract.handle(event, [])
    assert result == expected_result
