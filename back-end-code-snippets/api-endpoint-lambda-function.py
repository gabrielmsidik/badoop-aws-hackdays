import json
import logging
import boto3


session = boto3.Session(
    region_name="us-east-2") # us-east-2 is us east (ohio)
    
db_client = session.client('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    logger.info("Event: " + str(event))
    logger.info("Context: " + str(context))
    
    payload = event["payload"]
    assignee = '"' + payload["user"] + '"'
    assigner_number = payload["assigner"]
    latlon = payload["location"]
    gmaps_link = '"' + latlon + '"'
    
    logger.info("assignee: " + assignee)
    
    try:
        operation = event["operation"]
    except:
        logger.info("Key Error")
        operation = "create" # Current default function (to add alert into badoop-table)
        
    item = {
        'alertee':{
            'S': '{\"name\": ' + assignee + ',\"location\": ' + gmaps_link + '}'},
        'alerter':{'S': assigner_number}
    }
    logger.info("Item: " + str(item))
    # logger.info("Currently disconnected from badoop-table")
    if (operation == "create"):
        db_client.put_item(
            TableName='badoop-table',
            Item=item
        )
    
    return {
        'statusCode': 200,
        'body': 'Lambda Handler handed event.'
    }
