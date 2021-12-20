import boto3
import botocore
import constants as constants
import os

#initiate s3 resource
#s3 = boto3.resource('s3')

# select bucket

class s3PutData:
    def __init__(self):
       
        
        self.resource = boto3.resource('s3')
        self.db = boto3.resource('dynamodb')
        
        
        
        
    def downloadData(self):
        BUCKET_NAME = 'my-bucket' # replace with your bucket name
        KEY = 'sample.json' # replace with your object key

        s3 = boto3.resource('s3')

        try:
            s3.Bucket(BUCKET_NAME).download_file(KEY, 'sample.json')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

 
        
        # with open('readme.txt', 'w') as f:
        #     f.write(body)