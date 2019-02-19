import boto3
from freezegun import freeze_time
from mock import patch
from moto import mock_s3

from src import transform

TRANSFORM_BUCKET = "events-pipeline-transform"


@patch("uuid.uuid4")
@patch("src.transform.read_from_s3")
def test_transform(mock_read, mock_uuid):
    mock_uuid.return_value = "ff0e7277-1704-42a4-aada-65408c801199"
    meetup_event = {
        "created": 1414188635000,
        "description": "<p>Talk/Topic: Workplace Superheroes - With great power comes great </p>",
        "duration": 7200000,
        "event_url": "https://www.meetup.com/DevOps-Belfast/events/257403537/",
        "group": {
            "created": 1403890596000,
            "group_lat": 54.599998474121094,
            "group_lon": -5.929999828338623,
            "id": 15358562,
            "join_mode": "open",
            "name": "DevOps Belfast",
            "urlname": "DevOps-Belfast",
            "who": "Excellent Engineers",
        },
        "headcount": 0,
        "id": "dfpsxkyzdbzb",
        "maybe_rsvp_count": 0,
        "name": "Workplace Superheroes - With great power comes great "
        "responsibility",
        "rsvp_limit": 80,
        "status": "upcoming",
        "time": 1550601000000,
        "updated": 1549632597000,
        "utc_offset": 0,
        "venue": {
            "address_1": "Donegall Square W",
            "city": "Belfast",
            "country": "gb",
            "id": 26153278,
            "lat": 54.59609,
            "localized_country_name": "United Kingdom",
            "lon": -5.931652,
            "name": "Catalyst Belfast Fintech Hub",
            "repinned": True,
        },
        "visibility": "public",
        "waitlist_count": 0,
        "yes_rsvp_count": 57,
    }
    mock_read.return_value = [
        {"events": [meetup_event], "location": "belfast", "type": "meetup"}
    ]

    event = {
        "pointer": "events-pipeline-extract/2019/01/01/00/ff0e7277-1704-42a4-aada-65408c801199.json",
        "bucket": "events-pipeline-extract",
        "key": "2019/01/01/00/ff0e7277-1704-42a4-aada-65408c801199.json",
    }

    # expected_result = {
    #     "data": [
    #         {
    #             "events": [
    #                 {
    #                     "name": "Workplace Superheroes - With great power comes great responsibility",
    #                     "description": "<p>Talk/Topic: Workplace Superheroes - With great power comes great </p>",
    #                     "url": "https://www.meetup.com/DevOps-Belfast/events/257403537/",
    #                     "start": "2019-02-19 18:30:00Z",
    #                     "end": "2019-02-19 18:30:00Z",
    #                     "duration": 10000,
    #                     "topics": [],
    #                     "entry": ["free"],
    #                     "category": "DevOps Belfast",
    #                     "source": "meetup",
    #                     "location": "belfast",
    #                 }
    #             ],
    #             "type": "meetup",
    #             "location": "belfast",
    #         }
    #     ]
    # }

    expected_result = {
        "pointer": "events-pipeline-transform/2019/01/01/00/ff0e7277-1704-42a4-aada-65408c801199.json",
        "bucket": "events-pipeline-transform",
        "key": "2019/01/01/00/ff0e7277-1704-42a4-aada-65408c801199.json",
    }

    with mock_s3():
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket=TRANSFORM_BUCKET)

        with freeze_time("2019-01-01"):
            result = transform.handle(event, [])

    assert result == expected_result
