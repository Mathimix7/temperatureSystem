from wifimanager import WifiManager
import time
import urequests
import ubinascii
import network
import socket
import icons
import machine
import sh1106
import adafruit_sht31d
import ariblk

ip = "192.168.68.136"
port = "5555"

i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21)) # ESP32
#i2c = machine.SoftI2C(scl=machine.Pin(35), sda=machine.Pin(33)) # ESP32 S2
sensor = adafruit_sht31d.SHT31D(i2c)
display = sh1106.SH1106_I2C(128, 64, i2c, None)

wm = WifiManager(display)
wm.connect()

with open("name.dat", "r") as f:
    name = f.read()
print(name)

data = urequests.get(f"http://{ip}:{port}/")
macAddress = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
for device in data.json():
    if device["macAddress"] == macAddress:
        with open("id.dat", "w") as f:
            f.write(str(device["id"]))
        break
else:
    json = {
        "macAddress": macAddress,
        "name": name
    }
    response = urequests.post(f"http://{ip}:{port}/new", json=json)
    with open("id.dat", "w") as f:
        f.write(str(response.json()))

rtc = machine.RTC()
timeNow = urequests.get(f"http://{ip}:{port}/time").json()
rtc.datetime((int(timeNow["year"]), int(timeNow["month"]), int(timeNow["day"]), int(timeNow["weekday"]), int(timeNow["hour"]), int(timeNow["minute"]), int(timeNow["second"]), 0))
tempAverage = sensor.temperature
humAverage = sensor.relative_humidity
corf = "C"
while True:
    display.fill(0)
    display.hline(0,14,128,0xffff)
    if wm.is_connected():
        icons.wifiSymbol(display, 114,0)
        timeNow = rtc.datetime()
        tempAverage = (tempAverage + sensor.temperature)/2
        humAverage = (humAverage + sensor.relative_humidity)/2
        hour, minute, second = timeNow[4], timeNow[5], timeNow[6]
        if len(str(timeNow[4])) == 1:
            hour = f"0{str(timeNow[4])}"
        if len(str(timeNow[5])) == 1:
            minute = f"0{str(timeNow[5])}"
        display.text(f"{hour}:{minute}", 43, 0)
        fill = round(sensor.temperature//2.5)
        icons.temperatureSymbol(display, 30, 20, fill)
        if second % 5 == 0:
            if corf == "F":
                corf = "C"
            else:
                corf = "F"
        if corf == "F":
            temperatureNow = str(round(sensor.temperature*9/5 + 32, 1))
        else:
            temperatureNow = str(round(sensor.temperature, 1))
        temperatureNow = temperatureNow.split(".")
        temperatureNow = temperatureNow[0] + "." + temperatureNow[1][:1]
        display.printstring(45, 20, f"{temperatureNow} {corf}", ariblk)
        icons.humiditySymbol(display, 27,40)
        display.printstring(45, 42, f"{round(sensor.relative_humidity, 1)}%", ariblk)
        display.show()
        with open("sent.dat") as f:
            status = f.read()
        if str(timeNow[4]*60 + timeNow[5]).endswith("0"):
            if status == "false":
                sent = True
                with open("sent.dat", "w") as f:
                    f.write("true")
                print("Time to send")
                with open("id.dat") as f:
                    objectID = f.read()
                timeNow = urequests.get(f"http://{ip}:{port}/time").json()
                rtc.datetime((int(timeNow["year"]), int(timeNow["month"]), int(timeNow["day"]), int(timeNow["weekday"]), int(timeNow["hour"]), int(timeNow["minute"]), int(timeNow["second"]), 0))
                headers = {
                    "macAddress": macAddress,
                    "time": int(timeNow["unix"]),
                    "temp": round(tempAverage, 1),
                    "timeStamp": int(timeNow["minuteSinceToday"])/10 - 1,
                    "humidity": round(humAverage)
                }
                response = urequests.post(f"http://{ip}:{port}/create/{objectID}", json=headers)
                tempAverage = sensor.temperature
                humAverage = sensor.relative_humidity
        else:
            if status == "true":
                with open("sent.dat", "w") as f:
                    f.write("false")
    else:
        print('Disconnected!')
    time.sleep(1)
