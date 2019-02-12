from common.logger import logger


def handle(event, context):
    logger.info(f"extract: {event}")
    # TODO pull `location` from event

    body = {"message": "Your extract function executed successfully!", "data": event}

    response = {"statusCode": 200, "body": body}

    return response
