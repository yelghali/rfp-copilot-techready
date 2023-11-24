import logging, json, os
import azure.functions as func
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy
from azure.cosmos import CosmosClient, PartitionKey

import sys
sys.path.append("..")
from utilities.helpers.AzureBlobStorageHelper import AzureBlobStorageClient

bp_extract_rfp_questions_xlsx = func.Blueprint()

DOCUMENT_PROCESSING_QUEUE_NAME = os.getenv('DOCUMENT_PROCESSING_QUEUE_NAME', 'doc-processing')

@bp_extract_rfp_questions_xlsx.route(route="ExtractRFPQuestions")
def extract_rfp_questions_xlsx(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Requested to start processing all documents received')
    data = req.get_json()
    logging.info(data)

    # Initialize Cosmos Client
    url = os.environ['COSMOSDB_ENDPOINT']
    key = os.environ['COSMOSDB_KEY']
    client = CosmosClient(url, credential=key)

    # Get database
    database_name = os.environ['COSMOSDB_DBNAME']
    database = client.get_database_client(database_name)

    # Get container
    container_name = os.environ['COSMOSDB_CONTAINER_NAME_RFP_EXCEL_SOURCE']
    container = database.get_container_client(container_name)

    # Insert data into Cosmos DB
    container.upsert_item(data)

    return func.HttpResponse(f"Conversion started successfully for documents.", status_code=200)