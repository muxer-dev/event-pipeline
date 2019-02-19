import boto3
from freezegun import freeze_time
from mock import patch
from moto import mock_s3

from fixtures.payloads import MEETUP_EVENT
from src import extract

EXTRACT_BUCKET = "events-pipeline-extract"


@patch("uuid.uuid4")
@patch("src.extract.meetup.get_events_by_member")
def test_extract(mock_meetup, mock_uuid):
    mock_uuid.return_value = "a7b84906-49dd-45df-9e3c-9977145db8d7"
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
    expected_response = {
        "pointer": "events-pipeline-extract/2019/01/01/00/a7b84906-49dd-45df-9e3c-9977145db8d7.json",
        "bucket": "events-pipeline-extract",
        "key": "2019/01/01/00/a7b84906-49dd-45df-9e3c-9977145db8d7.json",
    }

    with mock_s3():
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket=EXTRACT_BUCKET)

        with freeze_time("2019-01-01"):
            result = extract.handle(event, [])

    assert result == expected_response
