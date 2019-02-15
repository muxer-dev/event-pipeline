from src.common.logger import logger


def handle(event, context):
    logger.info(f"transform: {event}")

    body = {"message": "Your transform function executed successfully!", "data": event}

    response = {"statusCode": 200, "body": body}

    return response
