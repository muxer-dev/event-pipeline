from src.common.logger import logger


def handle(event, context):
    logger.info(f"load: {event}")

    body = {"message": "Your load function executed successfully!", "data": event}

    response = {"statusCode": 200, "body": body}

    return response
