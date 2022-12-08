from copy import deepcopy
from fastapi import FastAPI
from pydantic import BaseModel
import json
import uvicorn
import datetime
import os

app = FastAPI(openapi_url="")

with open("D:\Projects-Python\PythonAPI\json.json", "r") as f:
    DATA = json.load(f)

class Item(BaseModel):
    macAddress: str
    time: int
    temp: float
    timeStamp: int
    humidity: int = None

class Device(BaseModel):
    macAddress: str
    name: str

class Device2(BaseModel):
    macAddress: str
    name: str
    id: int

def saveData():
    with open("D:\Projects-Python\PythonAPI\json.json", "w") as f:
        json.dump(DATA, f)

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

@app.get("/")
def home():
    return DATA

@app.get("/device/{device_id}")
def device(device_id: int):
    return DATA[device_id]

@app.get("/time")
def get_time():
    presentDate = datetime.datetime.now()
    unix_timestamp = str(round(datetime.datetime.timestamp(presentDate)))
    currentHour, currentMinute = presentDate.strftime("%H:%M").split(":")
    year = presentDate.strftime("%Y")
    month = presentDate.strftime("%m")
    day = presentDate.strftime("%d")
    second = presentDate.strftime("%S")
    weekday = presentDate.strftime('%w')
    minuteSinceToday = str(int(currentHour)*60 + int(currentMinute))
    return {"unix": unix_timestamp, "year":year, "month":month, "day":day, "weekday":weekday,"hour": currentHour, "minute": currentMinute, "second":second, "minuteSinceToday": minuteSinceToday}

@app.post("/create/{device_id}")
def create(device_id: int, item: Item):
    if DATA[device_id]["macAddress"] == item.macAddress:
        DATA[device_id]["timestamps"][item.timeStamp] = item.time
        DATA[device_id]["temperature"][item.timeStamp] = item.temp
        if item.humidity != None:
            DATA[device_id]["humidity"][item.timeStamp] = item.humidity
        saveData()
    else:
        return {"Error": "The ID does not match with the name"}
    return DATA

@app.post("/new")
def new(device: Device):
    id = len(DATA)
    timestaps = []
    temperature = []
    humidity = []
    for _ in range(144):
        timestaps.append('N/A')
        temperature.append('N/A')
        humidity.append('N/A')
    DATA.append({"macAddress": device.macAddress,"name": device.name, "id": id, "timestamps": timestaps, "temperature": temperature, "humidity": humidity})
    saveData()
    return id

@app.post("/reset/{device_id}")
def reset(device_id: int):
    timestaps = []
    temperature = []
    humidity = []
    for _ in range(144):
        timestaps.append('N/A')
        temperature.append('N/A')
        humidity.append('N/A')
    DATA[device_id]["timestamps"] = timestaps
    DATA[device_id]["temperature"] = timestaps
    DATA[device_id]["humidity"] = humidity
    saveData()
    return {"status": "success"}

@app.get("/day/{unixTime}")
def day(device: Device2, unixTime: int):
    unixTime = roundTimeStamp(unixTime)
    fileNum = getFileNumber(unixTime)
    name = str(device.id)+"_"+device.macAddress.replace(":","-")+"_"+device.name+"_"+str(fileNum)+".json"
    folderName = os.path.join("./TempData", str(device.id)+"_"+device.macAddress.replace(":","-")+"_"+device.name)
    path = os.path.join(folderName, name)
    result = None
    with open(path, "r") as f:
        data = json.load(f)
    for x in range(len(data)-1):
        x = x+1
        if data[x]["day"] == unixTime:
            result = deepcopy(data[x])
    return result if result else {"Error": f"No data found from {datetime.datetime.fromtimestamp(unixTime)}"}
            

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", host="192.168.68.128", reload=True)