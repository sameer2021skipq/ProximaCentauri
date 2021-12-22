from s3Function import s3PutData
import constants as constants

def lambda_handler(events, context):
    s3 = s3PutData();
    urls_list = s3.readDataBucket();
    constants.URL_TO_MONITOR_LIST = urls_list
    return urls_list

  