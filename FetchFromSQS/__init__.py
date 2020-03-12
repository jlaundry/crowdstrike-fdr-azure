
from datetime import datetime, timezone
import json
import logging
import os
import typing

import azure.functions as func

import boto3

VISIBILITY_TIMEOUT = 300
MESSAGE_LIMIT = 10


# def main(mytimer: func.TimerRequest, msg: func.Out[func.QueueMessage]) -> None:
def main(mytimer: func.TimerRequest, msg: func.Out[typing.List[str]]) -> None:
    start_time = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    logging.info(f"Timer trigger started at {start_time} (pastdue:{mytimer.past_due})")

    sqs = boto3.resource('sqs',
        region_name=os.environ['FDR_REGION'],
        aws_access_key_id=os.environ['FDR_AWS_KEY'],
        aws_secret_access_key=os.environ['FDR_AWS_SECRET']
    )

    queue = sqs.Queue(url=os.environ['FDR_QUEUE_URL'])

    queue_output = []
    queue_count = 0
    file_count = 0
    bytes_sum = 0

    for fdr_queue_item in queue.receive_messages(MaxNumberOfMessages=MESSAGE_LIMIT, VisibilityTimeout=VISIBILITY_TIMEOUT):
        queue_count += 1
        body = json.loads(fdr_queue_item.body)
        logging.info(f"SQS item: {body}")

        bytes_sum += body['totalSize']

        for s3_file in body['files']:
            file_count += 1
            queue_output.append(f"{body['bucket']}/{s3_file['path']}")

        fdr_queue_item.delete()
    
    msg.set(queue_output)
    logging.info(f"Done. Messages:{queue_count} Files:{file_count} Bytes:{bytes_sum}")
