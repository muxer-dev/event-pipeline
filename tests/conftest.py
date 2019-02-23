# stdlib imports
import boto3
import pytest
# third party imports
from moto import mock_s3


@pytest.yield_fixture(scope="function")
def s3_fixture():
    mock_s3().start()

    client = boto3.client("s3")
    resource = boto3.resource("s3")

    yield client, resource

    mock_s3().stop()
