import boto3
import botocore
import constants as constants
import os

def lambda_handler(events, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SameerTableTwoSprintTwo')
    update = table.update_item(
        
     #   {'id':{'S':'test_id'}},
             Key={
                 "Name": 'MessageID',
                 'CreationDate': 'AlarmCreationDate'
            },
            UpdateExpression="SET threshold = :threshold , monitorurl = :dataType",
            ExpressionAttributeValues={
                ':dataType' : "",
                ':threshold': ""
            },
            ReturnValues = "UPDATED_NEW"
        )
    return update
    
        
       
       