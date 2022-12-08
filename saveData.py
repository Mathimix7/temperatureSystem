import datetime
import time
import requests
import json
import os

def roundTimeStamp(time):
    return int(datetime.datetime.timestamp(datetime.datetime.fromtimestamp(time).replace(hour=0, minute=0, second=0, microsecond=0))) # Round unix timestap to 00:00:00 of that day

def getFileNumber(date):
    time = datetime.datetime.fromtimestamp(date)
    timeNowSTR = time.strftime("%Y/%m/%d")
    with open("datafilesalgorithm.json", "r") as f:
        data = json.load(f)
    startingTimeSTR = data["startingYear"]+"/"+data["startingMonth"]+"/"+data["startingDay"]
    delta = datetime.datetime.strptime(timeNowSTR, "%Y/%m/%d") - datetime.datetime.strptime(startingTimeSTR, "%Y/%m/%d")
    number = int(delta.days / 30)
    return number

def saveData(id):
    response = requests.get(f"http://192.168.68.136:5555/device/{id}").json()
    timestamp = roundTimeStamp(datetime.datetime.timestamp(datetime.datetime.now()))
    fileNum = getFileNumber(timestamp)
    name = str(response["id"])+"_"+response["macAddress"].replace(":","-")+"_"+response["name"]+"_"+str(fileNum)+".json"
    folderName = os.path.join("TempData", str(response["id"])+"_"+response["macAddress"].replace(":","-")+"_"+response["name"])
    if not os.path.exists(folderName):
        os.mkdir(folderName)
    path = os.path.join(folderName, name)
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        data.append({"day": timestamp,"timestamps": response["timestamps"],"temperature": response["temperature"], "humidity": response["humidity"]})
    else:
        data = [{"macAddress": response["macAddress"], "name":response["name"], "id": response["id"]}, {"day": timestamp,"timestamps": response["timestamps"],"temperature": response["temperature"], "humidity": response["humidity"]}]
    with open(path, 'w') as f:
        json.dump(data, f)


# period1 = int(time.mktime((datetime.datetime.now() + datetime.timedelta(days=0)).timetuple()))
# a = roundTimeStamp(period1)
# getFileNumber(a)

while True:
    if not os.path.exists("TempData"):
        os.mkdir("TempData")
    timeNow = datetime.datetime.now() + datetime.timedelta(hours=3, minutes=22, seconds=40)
    timeNow = timeNow.strftime("%H:%M:%S")
    print(timeNow)
    if timeNow == "00:00:10":
        response = requests.get(f"http://192.168.68.136:5555/").json()
        for id in range(len(response)):
            saveData(id)
    time.sleep(1)


