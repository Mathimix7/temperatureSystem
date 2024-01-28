import machine
import sh1106
import REFSAN12

i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21)) # ESP32
print(i2c.scan())

display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3D)
display.printstring(0, 0, f"Starting...", REFSAN12)
display.show()

from wifimanager import WifiManager
import time
import urequests
import ubinascii
import network
import socket
import icons
import adafruit_sht31d
import ariblk

ip = "192.168.68.128"
port = "5000"

# i2c = machine.SoftI2C(scl=machine.Pin(35), sda=machine.Pin(33)) # ESP32 S2
sensor = adafruit_sht31d.SHT31D(i2c)
display2 = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3C)
uart = machine.UART(1, 115200)
uart.init(115200, bits=8, parity=None, stop=1, rx=33, tx=32)

wm = WifiManager(display)
wm.connect()

print(wm.is_connected())
with open("name.dat", "r") as f:
    name = f.read()
print(name)

try:
    data = urequests.get(f"http://{ip}:{port}/")
except OSError:
    print(wm.is_connected())
    wm.connect()
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
tempOutsideAVG = None
humOutsideAVG = None
tempOutside = "N/A"
humOutside = "N/A"
corf = "C"

def formatUARTdata(data):
    data = data.decode("utf-8")
    temp, hum, sid = data.split(":")
    temp = int(temp[1:])/10
    hum = int(hum[1:])
    return temp, hum, sid

def checkForTempType(temp, corf, second=None):
    if second == None:
        if corf == "F":
            temperatureNow = round(temp*9/5 + 32, 1)
        else:
            temperatureNow = round(temp, 1)
        return temperatureNow, corf
    if second % 5 == 0:
        if corf == "F":
            corf = "C"
        else:
            corf = "F"
    if corf == "F":
        temperatureNow = round(temp*9/5 + 32, 1)
    else:
        temperatureNow = round(temp, 1)
    return temperatureNow, corf

while True:
    display.fill(0)
    display2.fill(0)
    display.hline(0,14,128,0xffff)
    display2.hline(0,14,128,0xffff)
    if wm.is_connected():
        icons.wifiSymbol(display, 114,0)
        icons.wifiSymbol(display2, 114,0)
        timeNow = rtc.datetime()
        tempAverage = (tempAverage + sensor.temperature)/2
        humAverage = (humAverage + sensor.relative_humidity)/2
        hour, minute, second = timeNow[4], timeNow[5], timeNow[6]
        if len(str(timeNow[4])) == 1:
            hour = f"0{str(timeNow[4])}"
        if len(str(timeNow[5])) == 1:
            minute = f"0{str(timeNow[5])}"
        display.text(f"{hour}:{minute}", 43, 0)
        display2.text(f"{hour}:{minute}", 43, 0)
        fill = round(sensor.temperature//2.5)
        if uart.any():
            tempOutside, humOutside, _ = formatUARTdata(uart.read())
            if tempOutsideAVG == None:
                tempOutsideAVG = tempOutside
            if humOutsideAVG == None:
                humOutsideAVG = humOutside
            tempOutsideAVG = (tempOutside + tempOutsideAVG)/2
            humOutsideAVG = (humOutside + humOutsideAVG)/2
        icons.temperatureSymbol(display, 30, 20, fill)
        temperatureNow, corf = checkForTempType(sensor.temperature, corf, second)
        display.printstring(45, 20, f"{temperatureNow} {corf}", ariblk)
        icons.humiditySymbol(display, 27,40)
        display.printstring(45, 42, f"{round(sensor.relative_humidity, 1)}%", ariblk)
        if not isinstance(tempOutside, str):
            temperatureNowOutside, _ = checkForTempType(tempOutside, corf)
            fill = round(tempOutside//2.5)
        else:
            temperatureNowOutside = tempOutside
            fill = 0
        
        icons.temperatureSymbol(display2, 30, 20, fill)
        icons.humiditySymbol(display2, 27,40)
        display2.printstring(45, 20, f"{temperatureNowOutside} {corf}", ariblk)
        display2.printstring(45, 42, f"{humOutside} %", ariblk)
        
        display.show()
        display2.show()
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
        wm.connect()
    time.sleep(1)