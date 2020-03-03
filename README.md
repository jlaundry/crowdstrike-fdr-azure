# CrowdStrike FDR Azure

This is a simple Function app that fetches CrowdStrike Falcon Data Replicator files and stores them in an Azure blob storage container.

## Getting Started (Azure Resource Manager Template)

Coming "soon".

## Getting Started (manual Azure resource creation)

1. First, do the usual virtualenv dance to build a local environment:

python3 -m venv .env
source .env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

2. Create an Azure Storage container, and note the connection string.

3. Create an Azure Function App (Python runtime), and set the following environment variables:

```
FDR_REGION = "us-west-1"
FDR_AWS_KEY = "AKxxxxxxx"
FDR_AWS_SECRET = "xxxxxxx"
FDR_QUEUE_URL = "https://sqs.us-west-1.amazonaws.com/xxxxx/xxxxxxx"

FDRStorage = "storage-container-connection-string"
```

4. Deploy the app, and either wait 15 minutes for the timer to fire, or manually run the FetchFromSQS function.

