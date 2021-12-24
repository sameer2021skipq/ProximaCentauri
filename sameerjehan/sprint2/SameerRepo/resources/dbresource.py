import boto3
import constants as constants

class dynamoData:
    def __init__(self):
        self.resource = boto3.resource('dynamodb') 
        
    def insert_data(self, message, createdDate):
        table = self.resource.Table("SameerTableTwoSprintTwo")
        table.put_item(Item = {
            'Name' : message, 
            'CreationDate' : createdDate,
            
        })
        
    def update_tabledata(self, message, createdDate, url_monitor, threshold_breached):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('SameerTableTwoSprintTwo')
        update = table.update_item(
            Key={
                 "Name": message,
                 'CreationDate': createdDate
            },
            UpdateExpression="SET threshold = :threshold , monitorurl = :dataType",
            ExpressionAttributeValues={
                ':dataType' : url_monitor,
                ':threshold': threshold_breached
            },
            ReturnValues = "UPDATED_NEW"
        )
        

            