
import datetime
import urllib3
import constants as constants
from cloudwatch_putMetric import cloudWatchPutMetric

def lambda_handler(events, context):
    values = dict()
    cw = cloudWatchPutMetric();

    
    
    avail = get_availability()
    avail_2 = get_availability_two()
    avail_3 = get_availability_three()
    avail_4 = get_availability_four()
    
    dimensions = [
        {"Name": "URL","Value": constants.URL_TO_MONITOR},
        {"Name": "Region","Value": "DUB"}
    ]
    dimensions_two = [
        {"Name": "URL","Value": constants.URL_TO_MONITOR_TWO},
        {"Name": "Region","Value": "DUB"}
    ]
    dimensions_three = [
        {"Name": "URL","Value": constants.URL_TO_MONITOR_THREE},
        {"Name": "Region","Value": "DUB"}
    ]
    dimensions_four = [
        {"Name": "URL","Value": constants.URL_TO_MONITOR_FOUR},
        {"Name": "Region","Value": "DUB"}
    ]
    
    
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_AVAILABILITY,dimensions,avail)
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_TWO_AVAILABILITY,dimensions_two,avail_2)
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_THREE_AVAILABILITY,dimensions_three,avail_3)
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_FOUR_AVAILABILITY,dimensions_four,avail_4)
    
    ####FIRST URL############
    
    
    latency = get_latency()
    latency_2 = get_latency_two()
    latency_3 = get_latency_three()
    latency_4 = get_latency_four()
    
    dimensions = [
        {"Name": "URL","Value": constants.URL_TO_MONITOR},
        {"Name": "Region","Value": "DUB"}
    ]
    dimensions_two = [
        {"Name": "URL","Value": constants.URL_TO_MONITOR_TWO},
        {"Name": "Region","Value": "DUB"}
    ]
    dimensions_three = [
        {"Name": "URL","Value": constants.URL_TO_MONITOR_THREE},
        {"Name": "Region","Value": "DUB"}
    ]
    dimensions_four = [
        {"Name": "URL","Value": constants.URL_TO_MONITOR_FOUR},
        {"Name": "Region","Value": "DUB"}
    ]
    
    
  #  cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_LATENCY,dimensions,latency)
  
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_LATENCY,dimensions,latency)
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_TWO_LATENCY,dimensions_two,latency_2)
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_THREE_LATENCY,dimensions_three,latency_3)
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_FOUR_LATENCY,dimensions_four,latency_4)
    
    
    values.update({"availability":avail, "Latency":latency})
    values.update({"availability_second_url":avail_2, "Latency_second_url":latency_2})
    values.update({"availability_third_url":avail_3, "Latency_third_url":latency_3})
    values.update({"availability_fourth_url":avail_4, "Latency_fourth_url":latency_4})
    
    return values 
    
    
###########FIRST URL#########33    
def get_availability():
    http = urllib3.PoolManager()
    response = http.request("GET", constants.URL_TO_MONITOR)
    if response.status == 200:
        return 1.0
    else:
        return 0.0
        
    
    
def get_latency():
    http = urllib3.PoolManager() #creating a poolmanager instance for sending requests
    start = datetime.datetime.now()
    response = http.request("GET", constants.URL_TO_MONITOR)
    end = datetime.datetime.now()
    delta = end - start 
    latencySec = round(delta.microseconds * .000001, 6)
    return latencySec
    
########SECOND URL#############
def get_availability_two():
    http = urllib3.PoolManager()
    response = http.request("GET", constants.URL_TO_MONITOR_TWO)
    if response.status == 200:
        return 1.0
    else:
        return 0.0
        
    
    
def get_latency_two():
    http = urllib3.PoolManager() #creating a poolmanager instance for sending requests
    start = datetime.datetime.now()
    response = http.request("GET", constants.URL_TO_MONITOR_TWO)
    end = datetime.datetime.now()
    delta = end - start 
    latencySec = round(delta.microseconds * .000001, 6)
    return latencySec
#####THIRD URL##########
def get_availability_three():
    http = urllib3.PoolManager()
    response = http.request("GET", constants.URL_TO_MONITOR_THREE)
    if response.status == 200:
        return 1.0
    else:
        return 0.0
        
    
    
def get_latency_three():
    http = urllib3.PoolManager() #creating a poolmanager instance for sending requests
    start = datetime.datetime.now()
    response = http.request("GET", constants.URL_TO_MONITOR_THREE)
    end = datetime.datetime.now()
    delta = end - start 
    latencySec = round(delta.microseconds * .000001, 6)
    return latencySec

#######FOURTH URL##########
def get_availability_four():
    http = urllib3.PoolManager()
    response = http.request("GET", constants.URL_TO_MONITOR_FOUR)
    if response.status == 200:
        return 1.0
    else:
        return 0.0
        
    
    
def get_latency_four():
    http = urllib3.PoolManager() #creating a poolmanager instance for sending requests
    start = datetime.datetime.now()
    response = http.request("GET", constants.URL_TO_MONITOR_FOUR)
    end = datetime.datetime.now()
    delta = end - start 
    latencySec = round(delta.microseconds * .000001, 6)
    return latencySec
    
# import datetime
# import urllib3
# import constants as constants
# from cloudwatch_putMetric import cloudWatchPutMetric

# def lambda_handler(events, context):
#     values = dict()
#     cw = cloudWatchPutMetric();
    
    
    
#     avail = get_availability()
#     dimensions = [
#         {"Name": "URL","Value": constants.URL_TO_MONITOR}
#         # {"Name": "Region","Value": "DUB"}
#     ]
    
    
#     cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_AVAILABILITY,dimensions,avail)
    
    
#     latency = get_latency()
#     dimensions = [
#         {"Name": "URL","Value": constants.URL_TO_MONITOR}
#         # {"Name": "Region","Value": "DUB"}
#     ]
    
    
#     cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_LATENCY,dimensions,latency)
    
#     values.update({"availability":avail, "Latency":latency})
#     return values 
    
    
    
# def get_availability():
#     http = urllib3.PoolManager()
#     response = http.request("GET", constants.URL_TO_MONITOR)
#     if response.status == 200:
#         return 1.0
#     else:
#         return 0.0
    
    
# def get_latency():
#     http = urllib3.PoolManager() #creating a poolmanager instance for sending requests
#     start = datetime.datetime.now()
#     response = http.request("GET", constants.URL_TO_MONITOR)
#     end = datetime.datetime.now()
#     delta = end - start 
#     latencySec = round(delta.microseconds * .000001, 6)
#     return latencySec

# import datetime
# import urllib3
# import constants as constants
# from cloudwatch_putMetric import cloudWatchPutMetric

# def lambda_handler(events, context):
#     values = dict()
#     cw = cloudWatchPutMetric();
    
    
    
#     avail = get_availability()
#     dimensions = [
#         {"Name": "URL","Value": constants.URL_TO_MONITOR}
#         # {"Name": "Region","Value": "DUB"}
#     ]
    
    
#     cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_AVAILABILITY,dimensions,avail)
    
    
#     latency = get_latency()
#     dimensions = [
#         {"Name": "URL","Value": constants.URL_TO_MONITOR}
#         # {"Name": "Region","Value": "DUB"}
#     ]
    
    
#     cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_LATENCY,dimensions,latency)
    
#     values.update({"availability":avail, "Latency":latency})
#     return values 
    
    
    
# def get_availability():
#     http = urllib3.PoolManager()
#     response = http.request("GET", constants.URL_TO_MONITOR)
#     if response.status == 200:
#         return 1.0
#     else:
#         return 0.0
    
    
# def get_latency():
#     http = urllib3.PoolManager() #creating a poolmanager instance for sending requests
#     start = datetime.datetime.now()
#     response = http.request("GET", constants.URL_TO_MONITOR)
#     end = datetime.datetime.now()
#     delta = end - start 
#     latencySec = round(delta.microseconds * .000001, 6)
#     return latencySec
# xxx----------