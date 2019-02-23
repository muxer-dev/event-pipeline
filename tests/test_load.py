import json

import boto3
from mock import patch
from moto import mock_s3
from src import load

TRANSFORM_BUCKET = "events-pipeline-transform"


@patch("src.load.requests.post")
def test_load(mock_post):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 200

    event = {
        "pointer": "events-pipeline-transform/2019/01/01/00/ff0e7277-1704-42a4-aada-65408c801199.json",
        "bucket": "events-pipeline-transform",
        "key": "2019/01/01/00/ff0e7277-1704-42a4-aada-65408c801199.json",
    }

    records = [
        {
            "events": [
                {
                    "name": "Workplace Superheroes - With great power comes great responsibility",
                    "url": "https://www.meetup.com/DevOps-Belfast/events/257403537/",
                    "start": "2019-02-19 18:30:00Z",
                    "end": "2019-02-19 18:30:00Z",
                    "duration": 10000,
                    "topics": [],
                    "entry": ["free"],
                    "category": "DevOps Belfast",
                    "source": "meetup",
                    "location": "belfast",
                }
            ],
            "type": "meetup",
            "location": "belfast",
        }
    ]

    with mock_s3():
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket=TRANSFORM_BUCKET)

        bucket = "events-pipeline-transform"
        key = "2019/01/01/00/ff0e7277-1704-42a4-aada-65408c801199.json"

        contents = bytes(json.dumps(records, indent=2).encode("UTF-8"))
        s3.put_object(Body=contents, Bucket=bucket, Key=key)

        result = load.handle(event, [])

    expected_result = {"responses": []}

    assert result == expected_result
