from dbresource import dynamoData
import json

def lambda_handler(events, context):
    db = dynamoData();
    message = events['Records'][0]['Sns']['Message']
    message = json.loads(message)
    db.insert_data(message['AlarmName'], message['StateChangeTime'])
   
