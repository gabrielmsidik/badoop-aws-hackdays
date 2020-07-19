import json
import logging
import boto3


session = boto3.Session(
    region_name="us-east-1") # us-east-2 is us east (ohio) - does not support SMS MAKE SURE USE us-east-1!
    
sns_client = session.client('sns')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    
    logger.info("Event: " + str(event))
    logger.info("Context: " + str(context))

    
    try:
        records = event["Records"]
        logger.info("LATEST LOGGING")
        logger.info("records: " + str(records))
        
        parsed_dynamodb_obj = records[0]["dynamodb"]["Keys"]
        logger.info(parsed_dynamodb_obj)
        
        alertee_details = parsed_dynamodb_obj["alertee"]["S"]
        logger.info(alertee_details)
        alertee_parsed_details = json.loads(alertee_details)
        alertee_name = alertee_parsed_details["name"]
        alertee_location = alertee_parsed_details["location"]
        
        message = "%s may be in trouble!! Here is his/her latest location: %s" % (alertee_name, alertee_location)
        alerter_phone_number = parsed_dynamodb_obj["alerter"]["S"]
        
        logger.info("Alertee: " + str(alertee_name))
        logger.info("Alerter: " + str(alerter_phone_number))
        logger.info("Message: " + message)
        
    
        response = sns_client.publish(
            PhoneNumber=alerter_phone_number,
            Message=message,
            MessageAttributes={
                'AWS.SNS.SMS.SenderID': {
                    'DataType': 'String',
                    'StringValue': 'BaDoop'
                },
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Transactional'
                }
            }
        )
    except :
        logger.info("Some error somewhere, hopefully this clears the stream")
        
        response = "ERROR: EXCEPT BLOCK REACHED"
    
    return response
