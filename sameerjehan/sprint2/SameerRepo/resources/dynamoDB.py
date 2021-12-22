from dbresource import dynamoData
import json

def lambda_handler(events, context):
    db = dynamoData();
   
    messageID = events['Records'][0]['Sns']['MessageId']
    statechange = events['Records'][0]['Sns']['Timestamp']
    message = events['Records'][0]['Sns']['Message']
    message_2 = json.loads(message)
    monitored_url = message_2['Trigger']['Dimensions'][0]['value']
    threshold_set = str(message_2['Trigger']['Threshold'])
#    message = json.loads(messageID)
   # db.insert_data(messageID, statechange)
    db.update_tabledata(messageID, statechange, monitored_url, threshold_set)
   
