import boto3
import constants as constants
import json

class s3PutData:
    def __init__(self):
        self.resource = boto3.resource('s3')
        
    def readDataBucket(self):
        bucket = self.resource.Bucket('newsameerbucketsprint2')
        for obj in bucket.objects.all():
            key = obj.key
            body = obj.get()['Body'].read()
        urls = {}
        urls = (json.loads(body))
        urls_list = []
        for key in urls.keys():
            urls_list.append(urls[key])
        
        return urls_list
        
   
        
  