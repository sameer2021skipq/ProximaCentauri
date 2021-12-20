import boto3
import botocore
import constants as constants
import os

#initiate s3 resource
#s3 = boto3.resource('s3')

# select bucket

class s3PutData:
    def __init__(self):
        # self.session = boto3.Session( 
        #     aws_access_key_id='AKIAUTEXLE6CGARZHOO6', 
        #     aws_secret_access_key='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')
            
        # self.resource = self.session.resource('s3')
        
        self.resource = boto3.resource('s3')
        self.db = boto3.resource('dynamodb')
        
        
        
    def s3_data(self):
        session = boto3.Session( 
         aws_access_key_id='AKIAUTEXLE6CGARZHOO6', 
         aws_secret_access_key='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')
         
        s3 = session.resource('s3')
        
        bucket = s3.Bucket('sameerbucketnew')

        for obj in bucket.objects.all():
            key = obj.key
            body = obj.get()['Body'].read()
            
        my_json = body.decode('utf8').replace("'", '"')
        changed_string = str(my_json)
        url_dict = eval(changed_string)
        l1 = []
        for urls in list(url_dict.keys()):
            l1.append(url_dict[urls])
            
      #  constants.URL_TO_MONITOR = l1[0]
        
        # constants.URL_TO_MONITOR_ONE = l1[0]
        # constants.URL_TO_MONITOR_TWO = l1[1]
        # constants.URL_TO_MONITOR_THREE = l1[2]
        # constants.URL_TO_MONITOR_FOUR = l1[3]
        
            
        return l1
        
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