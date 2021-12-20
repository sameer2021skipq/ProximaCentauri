from s3Function import s3PutData

def lambda_handler(events, context):
    s3 = s3PutData();
    list_one = s3.s3_data();
    s3.downloadData()
    
    

  