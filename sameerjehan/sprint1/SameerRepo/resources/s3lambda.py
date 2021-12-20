from s3Function import s3PutData

def lambda_handler(events, context):
    s3 = s3PutData();
    s3.downloadData()
    
    

  