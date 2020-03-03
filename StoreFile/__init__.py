
import io
import logging
import os

import azure.functions as func

import boto3


def main(msg: func.QueueMessage, outfile: func.Out[func.InputStream]) -> None:
    filename = msg.get_body().decode('utf-8')
    logging.info(f"Working on queue item: {filename}")

    s3 = boto3.client('s3',
        region_name=os.environ['FDR_REGION'],
        aws_access_key_id=os.environ['FDR_AWS_KEY'],
        aws_secret_access_key=os.environ['FDR_AWS_SECRET']
    )

    (bucket, path) = filename.split("/", 1)
    content = io.BytesIO()
    s3.download_fileobj(bucket, path, content)

    content.seek(0)
    outfile.set(content)

    logging.info("Done")
