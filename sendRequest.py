import requests
import datetime
import time

def updateTemperature():
    presentDate = datetime.datetime.now()
    unix_timestamp = datetime.datetime.timestamp(presentDate)
    headers = {
        "macAddress": "40:22:d8:77:5b:9c",
        "time": unix_timestamp,
        "temp": 21,
        "timeStamp": 143
    }
    response = requests.post("http://192.168.68.136:5555/create/0", json=headers)
    print(response)

def newThermometer(): 
    headers = {
        "macAddress": "9c:9c:1f:e2:b7:48",
        "name": "Test"
    }
    response = requests.post("http://192.168.68.136:5555/new", json=headers)
    print(response.json())

def reset(num): 
    response = requests.post(f"http://192.168.68.136:5555/reset/{num}")
    print(response.json())

# response = requests.get(f"http://192.168.68.136:5555/device/1").json()
# #with open(response["macAddress"]+"-"+response["name"], 'w'):
# #    [{"day": }]

# period1 = int(time.mktime((datetime.datetime.now() - datetime.timedelta(days=7)).timetuple()))
# timeNow = int(datetime.datetime.timestamp(datetime.datetime.fromtimestamp(period1).replace(hour=0, minute=0, second=0, microsecond=0))) # Round unix timestap to 00:00:00 of that day
# print(timeNow)

def getOldData():
    presentDate = datetime.datetime.now()-datetime.timedelta(days=0)
    unix_timestamp = int(datetime.datetime.timestamp(presentDate))
    headers = {
        "macAddress": "40:22:d8:77:5b:9c",
        "name": "Kitchen-IN",
        "id": 0
    }
    response = requests.get(f"http://192.168.68.128:5000/day/{unix_timestamp}", json=headers)
    print(response.json())

getOldData()
