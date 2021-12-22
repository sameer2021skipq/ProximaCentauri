import datetime
import urllib3
import constants as constants
from cloudwatch_putMetric import cloudWatchPutMetric

def lambda_handler(events, context):
    values = dict()
    cw = cloudWatchPutMetric();
    constants.URL_TO_MONITOR_LIST = ["https://www.espn.com/","https://www.dawn.com/","https://www.facebook.com/","https://www.messenger.com/"]
    
    for i in range(len(constants.URL_TO_MONITOR_LIST)):
        
        avail = get_availability(constants.URL_TO_MONITOR_LIST[i])
        dimensions = [
            {"Name": "URL","Value": constants.URL_TO_MONITOR_LIST[i]},
           # {"Name": "Region","Value": "DUB"}
            ]
    
    
        cw.put_data(constants.URL_TO_MONITOR_NAMESPACE, constants.URL_MONITOR_AVAILABILITY+constants.URL_TO_MONITOR_LIST[i],dimensions,avail)
    
        latency = get_latency(constants.URL_TO_MONITOR_LIST[i])
        dimensions = [
            {"Name": "URL","Value": constants.URL_TO_MONITOR_LIST[i]},
          #  {"Name": "Region","Value": "DUB"}
        ]
    
    
        cw.put_data(constants.URL_TO_MONITOR_NAMESPACE, constants.URL_MONITOR_LATENCY+constants.URL_TO_MONITOR_LIST[i],dimensions,latency)
    
        values.update({"availability":avail, "Latency":latency})
        
    return values 
    
    
    
def get_availability(monitored_url):
    http = urllib3.PoolManager()
    response = http.request("GET", monitored_url)
    if response.status == 200:
        return 1.0
    else:
        return 0.0
    
    
def get_latency(monitored_url_latency):
    http = urllib3.PoolManager() #creating a poolmanager instance for sending requests
    start = datetime.datetime.now()
    response = http.request("GET", monitored_url_latency)
    end = datetime.datetime.now()
    delta = end - start 
    latencySec = round(delta.microseconds * .000001, 6)
    return latencySec

