try:
    import machine
    import sh1106
    import REFSAN12
    import sys

    stop_button = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
    i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21)) # ESP32
    print(i2c.scan())

    display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3C)
    display.printstring(0, 0, f"Starting...", REFSAN12)
    display.show()
    if stop_button.value() == 0:
        display.fill(0)
        display.printstring(0, 0, f"Stoping...\nButton pressed!", REFSAN12)
        display.show()
        sys.exit()

    from wifimanager import WifiManager
    import time
    import urequests
    import ubinascii
    import network
    import socket
    import icons
    import adafruit_sht31d
    import ariblk
    import _thread

    ip = "192.168.68.136"
    port = "5555"

    # i2c = machine.SoftI2C(scl=machine.Pin(35), sda=machine.Pin(33)) # ESP32 S2
    sensor = adafruit_sht31d.SHT31D(i2c)
    display2 = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3D)
    uart = machine.UART(1, 115200)
    uart.init(115200, bits=8, parity=None, stop=1, rx=34, tx=33)

    wm = WifiManager(display)
    macAddress = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print(macAddress)
    rtc = machine.RTC()
    #with open("name.dat", "r") as f:
    #    name = f.read()
    #print(name)

    try:
        timeNow = urequests.get(f"http://{ip}:{port}/time").json()
        rtc.datetime((int(timeNow["year"]), int(timeNow["month"]), int(timeNow["day"]), int(timeNow["weekday"]), int(timeNow["hour"]), int(timeNow["minute"]), int(timeNow["second"]), 0))
        apiON = True
    except:
        rtc.datetime((0, 0, 0, 0, 0, 0, 0, 0))
        apiON = False

    tempOutside = "N/A"
    humOutside = "N/A"
    corf = "C"
    threadStartedWIFI = False
    threadStartedAPI = False

    def resetAVGS():
        global tempAverage, humAverage, tempOutsideAVG, humOutsideAVG
        tempAverage = sensor.temperature
        humAverage = sensor.relative_humidity
        tempOutsideAVG = None
        humOutsideAVG = None

    resetAVGS()

    def formatUARTdata(data):
        try:
            data = data.decode("utf-8")
            temp, hum, sid = data.split(":")
            temp = int(temp[1:])/10
            hum = str(int(hum[1:])/10)
            hum = hum.split(".")
            hum = hum[0] + "." + hum[1][:1]
            return float(temp), float(hum), sid
        except:
            print(data)

    def checkForTempType(temp, corf, second=None):
        if second == None:
            if corf == "F":
                temperatureNow = str(round(temp*9/5 + 32, 2))
            else:
                temperatureNow = str(round(temp, 1))
            temperatureNow = temperatureNow.split(".")
            temperatureNow = temperatureNow[0] + "." + temperatureNow[1][:1]
            return temperatureNow, corf
        if second % 5 == 0:
            if corf == "F":
                corf = "C"
            else:
                corf = "F"
        if corf == "F":
            temperatureNow = str(round(temp*9/5 + 32, 2))
        else:
            temperatureNow = str(round(temp, 1))
        temperatureNow = temperatureNow.split(".")
        temperatureNow = temperatureNow[0] + "." + temperatureNow[1][:1]
        return temperatureNow, corf

    def connectThread():
        global apiON
        wm.connect()
        threadStartedWIFI = False
        try:
            timeNow = urequests.get(f"http://{ip}:{port}/time").json()
            rtc.datetime((int(timeNow["year"]), int(timeNow["month"]), int(timeNow["day"]), int(timeNow["weekday"]), int(timeNow["hour"]), int(timeNow["minute"]), int(timeNow["second"]), 0))
            apiON = True
            resetAVGS()
        except:
            apiON = False 

    def checkAPIstatus():
        while True:
            print("a")
            global apiON
            try:
                timeNow = urequests.get(f"http://{ip}:{port}/time").json()
                rtc.datetime((int(timeNow["year"]), int(timeNow["month"]), int(timeNow["day"]), int(timeNow["weekday"]), int(timeNow["hour"]), int(timeNow["minute"]), int(timeNow["second"]), 0))
                apiON = True
                threadStartedAPI = False
                resetAVGS()
                break
            except Exception as e:
                print(e)
                display.fill(0)
                display.hline(0,14,128,0xffff)
                icons.wifiSymbol(display, 114,0)
                display.printstring(0,20,f"API failed.\nTrying to connect...\n{e}", REFSAN12)
                display.show()
                apiON = False
            time.sleep(5)
    lastSecond = 0
    while True:
        if stop_button.value() == 0:
            display.fill(0)
            display.printstring(0, 0, f"Stoping...\nButton pressed!", REFSAN12)
            display.show()
            sys.exit()
        if wm.is_connected() and apiON:
            timeNow = rtc.datetime()
            month,day,hour, minute, second = timeNow[1], timeNow[2], timeNow[4], timeNow[5], timeNow[6]
            print(second)
            if lastSecond != second-1:
                currentSecond = second
                second = lastSecond + 1
                lastSecond = currentSecond 
            else:
                lastSecond = second
            if second % 5 == 0:
                try:
                    headers = {
                        "macAddress": macAddress,
                        "temp": round(sensor.temperature, 1),
                        "humidity": round(sensor.relative_humidity)
                    }
                    response = urequests.post(f"http://{ip}:{port}/updateCurrent/0", json=headers)
                    if temperatureNowOutside != "N/A":
                        headers = {
                            "macAddress": macAddress,
                            "temp": round(tempOutside, 1),
                            "humidity": round(humOutside)
                        }
                        response = urequests.post(f"http://{ip}:{port}/updateCurrent/1", json=headers)
                except:
                    print("could not send current temp")
            display.fill(0)
            display2.fill(0)
            display.hline(0,14,128,0xffff)
            display2.hline(0,14,128,0xffff)
            icons.wifiSymbol(display, 114,0)
            icons.wifiSymbol(display2, 114,0)
            tempAverage = (tempAverage + sensor.temperature)/2
            humAverage = (humAverage + sensor.relative_humidity)/2
            if len(str(timeNow[4])) == 1:
                hour = f"0{str(timeNow[4])}"
            if len(str(timeNow[5])) == 1:
                minute = str(minute)
                minute = "0"+minute
            if len(str(timeNow[1])) == 1:
                month = f"0{str(timeNow[1])}"
            if len(str(timeNow[2])) == 1:
                day = f"0{str(timeNow[2])}"
            display.text(f"{day}/{month}", 43, 0)
            display2.text(f"{hour}:{minute}", 43, 0)
            fill = round(sensor.temperature//2.5)
            if uart.any():
                try:
                    tempOutside, humOutside, batteryValue = formatUARTdata(uart.read())
                except:
                    pass
                if tempOutsideAVG == None:
                    tempOutsideAVG = tempOutside
                if humOutsideAVG == None:
                    humOutsideAVG = humOutside
                tempOutsideAVG = (tempOutside + tempOutsideAVG)/2
                humOutsideAVG = (humOutside + humOutsideAVG)/2
            display.text("IN",0,0)
            icons.temperatureSymbol(display, 30, 20, fill)
            data = checkForTempType(sensor.temperature, corf, second)
            if data:
                temperatureNow, corf = data
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
            display2.text("OUT",0,0)
            display2.printstring(45, 20, f"{temperatureNowOutside} {corf}", ariblk)
            print(humOutside)
            if humOutside != "N/A":
                hum = str(humOutside)
                hum = hum.split(".")
                hum = hum[0] + "." + hum[1][:1]
            else:
                hum = humOutside
            display2.printstring(45, 42, f"{hum} %", ariblk)
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
                    try:
                        timeNow = urequests.get(f"http://{ip}:{port}/time").json()
                        rtc.datetime((int(timeNow["year"]), int(timeNow["month"]), int(timeNow["day"]), int(timeNow["weekday"]), int(timeNow["hour"]), int(timeNow["minute"]), int(timeNow["second"]), 0))
                        headers = {
                            "macAddress": macAddress,
                            "time": int(timeNow["unix"]),
                            "temp": round(tempAverage, 1),
                            "timeStamp": int(timeNow["minuteSinceToday"])/10 - 1,
                            "humidity": round(humAverage)
                        }
                        response = urequests.post(f"http://{ip}:{port}/create/0", json=headers)
                        tempAverage = sensor.temperature
                        humAverage = sensor.relative_humidity
                        if tempOutsideAVG != None:
                            headers = {
                                "macAddress": macAddress,
                                "time": int(timeNow["unix"]),
                                "temp": round(tempOutsideAVG, 1),
                                "timeStamp": int(timeNow["minuteSinceToday"])/10 - 1,
                                "humidity": round(humOutsideAVG)
                            }
                            response = urequests.post(f"http://{ip}:{port}/create/1", json=headers)
                            tempOutsideAVG = None
                            humOutsideAVG = None
                        else:
                            tempOutside = "N/A"
                            humOutside = "N/A"
                    except Exception as e:
                        print(e)
                        apiON = False
                    try:
                        response = urequests.post(f"http://{ip}:{port}/updateBattery/1/{batteryValue}")
                    except:
                        print("Did not send value")
                        
            else:
                if status == "true":
                    with open("sent.dat", "w") as f:
                        f.write("false")
        else:
            display2.fill(0)
            display2.hline(0,14,128,0xffff)
            timeNow = rtc.datetime()
            second = timeNow[6]
            display2.text("IN", 25, 2)
            display2.text("OUT", 85, 2)
            if uart.any():
                try:
                    tempOutside, humOutside, _ = formatUARTdata(uart.read())
                except Exception as e:
                    print(e)
            fill = round(sensor.temperature//2.5)
            icons.temperatureSymbol(display2, 3, 20, fill)
            data = checkForTempType(sensor.temperature, corf, second)
            if data:
                temperatureNow, corf = data
            display2.printstring(18, 20, f"{temperatureNow} {corf}", REFSAN12)
            icons.humiditySymbol(display2, 0,40)
            display2.printstring(18, 42, f"{round(sensor.relative_humidity, 1)}%", REFSAN12)
            if not isinstance(tempOutside, str):
                temperatureNowOutside, _ = checkForTempType(tempOutside, corf)
                fill = round(tempOutside//2.5)
            else:
                temperatureNowOutside = tempOutside
                fill = 0
            icons.temperatureSymbol(display2, 68, 20, fill)
            icons.humiditySymbol(display2, 65,40)
            display2.printstring(83, 20, f"{temperatureNowOutside} {corf}", REFSAN12)
            if humOutside != "N/A":
                hum = str(humOutside)
                hum = hum.split(".")
                hum = hum[0] + "." + hum[1][:1]
            else:
                hum = humOutside
            display2.printstring(83, 42, f"{hum} %", REFSAN12)
            display2.show()
            if not wm.is_connected():
                if not threadStartedWIFI:
                    _thread.start_new_thread(connectThread, ())
                    threadStartedWIFI = True
            elif not apiON:
                display.fill(0)
                display.hline(0,14,128,0xffff)
                icons.wifiSymbol(display, 114,0)
                display.printstring(0,20,"API failed.\nTrying to connect...", REFSAN12)
                display.show()
                if not threadStartedAPI:
                    _thread.start_new_thread(checkAPIstatus, ())
                    threadStartedAPI = True
                
        time.sleep(1)

except Exception as e:
    print(e)
    #machine.reset()



