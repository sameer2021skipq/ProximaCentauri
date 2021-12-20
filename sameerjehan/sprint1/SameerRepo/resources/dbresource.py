import boto3
import constants as constants

class dynamoData:
    def __init__(self):
        self.resource = boto3.resource('dynamodb') 
        
    def insert_data(self, message, createdDate):
        table = self.resource.Table("SameerTableTwo")
        table.put_item(Item = {
            'Name' : message, 
            'CreationDate' : createdDate
        })
        

            