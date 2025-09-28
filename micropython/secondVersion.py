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
    temperatureNow = "N/A"
    temperatureNowOutside = "N/A"
    batteryValue = None
    corf = "C"
    threadStartedWIFI = False
    threadStartedAPI = False
    state_lock = _thread.allocate_lock()
    TEMP_TOGGLE_INTERVAL_MS = 5000
    last_temp_toggle_ms = time.ticks_ms()

    def set_api_status(value):
        global apiON
        state_lock.acquire()
        try:
            apiON = value
        finally:
            state_lock.release()

    def get_api_status():
        state_lock.acquire()
        try:
            return apiON
        finally:
            state_lock.release()

    def set_wifi_thread_flag(value):
        global threadStartedWIFI
        state_lock.acquire()
        try:
            threadStartedWIFI = value
        finally:
            state_lock.release()

    def is_wifi_thread_running():
        state_lock.acquire()
        try:
            return threadStartedWIFI
        finally:
            state_lock.release()

    def set_api_thread_flag(value):
        global threadStartedAPI
        state_lock.acquire()
        try:
            threadStartedAPI = value
        finally:
            state_lock.release()

    def is_api_thread_running():
        state_lock.acquire()
        try:
            return threadStartedAPI
        finally:
            state_lock.release()

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
            print(sid)
            return float(temp), float(hum), sid
        except:
            print(data)

    def checkForTempType(temp, corf, second=None):
        global last_temp_toggle_ms
        if temp is None:
            return "N/A", corf

        if second is not None:
            now_ms = time.ticks_ms()
            if time.ticks_diff(now_ms, last_temp_toggle_ms) >= TEMP_TOGGLE_INTERVAL_MS:
                last_temp_toggle_ms = now_ms
                corf = "C" if corf == "F" else "F"

        if corf == "F":
            temperature_now = str(round(temp * 9 / 5 + 32, 2))
        else:
            temperature_now = str(round(temp, 1))

        temperature_now = temperature_now.split(".")
        if len(temperature_now) == 1:
            temperature_now.append("0")
        temperature_now = temperature_now[0] + "." + temperature_now[1][:1]
        return temperature_now, corf

    def connectThread():
        try:
            wm.connect()
            response = urequests.get(f"http://{ip}:{port}/time")
            timeNow = response.json()
            response.close()
            rtc.datetime((int(timeNow["year"]), int(timeNow["month"]), int(timeNow["day"]), int(timeNow["weekday"]), int(timeNow["hour"]), int(timeNow["minute"]), int(timeNow["second"]), 0))
            set_api_status(True)
            resetAVGS()
        except Exception as e:
            print("Wi-Fi reconnect failed:", e)
            set_api_status(False)
        finally:
            set_wifi_thread_flag(False)

    def checkAPIstatus():
        while True:
            print("a")
            try:
                response = urequests.get(f"http://{ip}:{port}/time")
                timeNow = response.json()
                response.close()
                rtc.datetime((int(timeNow["year"]), int(timeNow["month"]), int(timeNow["day"]), int(timeNow["weekday"]), int(timeNow["hour"]), int(timeNow["minute"]), int(timeNow["second"]), 0))
                set_api_status(True)
                resetAVGS()
                break
            except Exception as e:
                print(e)
                display.fill(0)
                display.hline(0,14,128,0xffff)
                icons.wifiSymbol(display, 114,0)
                display.printstring(0,20,f"API failed.\nTrying to connect...\n{e}", REFSAN12)
                display.show()
                set_api_status(False)
            time.sleep(5)
        set_api_thread_flag(False)
    lastSecond = 0
    while True:
        if stop_button.value() == 0:
            display.fill(0)
            display.printstring(0, 0, f"Stoping...\nButton pressed!", REFSAN12)
            display.show()
            sys.exit()
        if wm.is_connected() and get_api_status():
            timeNow = rtc.datetime()
            month, day, hour, minute, second = timeNow[1], timeNow[2], timeNow[4], timeNow[5], timeNow[6]
            if lastSecond != second - 1:
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
                    response.close()
                    if isinstance(tempOutside, (int, float)):
                        headers = {
                            "macAddress": macAddress,
                            "temp": round(tempOutside, 1),
                            "humidity": round(humOutside)
                        }
                        response = urequests.post(f"http://{ip}:{port}/updateCurrent/1", json=headers)
                        response.close()
                except Exception as e:
                    print("could not send current temp", e)

            display.fill(0)
            display2.fill(0)
            display.hline(0, 14, 128, 0xffff)
            display2.hline(0, 14, 128, 0xffff)
            icons.wifiSymbol(display, 114, 0)
            icons.wifiSymbol(display2, 114, 0)
            tempAverage = (tempAverage + sensor.temperature) / 2
            humAverage = (humAverage + sensor.relative_humidity) / 2

            if len(str(timeNow[4])) == 1:
                hour = f"0{str(timeNow[4])}"
            if len(str(timeNow[5])) == 1:
                minute = "0" + str(minute)
            if len(str(timeNow[1])) == 1:
                month = f"0{str(timeNow[1])}"
            if len(str(timeNow[2])) == 1:
                day = f"0{str(timeNow[2])}"

            display.text(f"{day}/{month}", 43, 0)
            display2.text(f"{hour}:{minute}", 43, 0)

            fill = round(sensor.temperature // 2.5)
            if uart.any():
                try:
                    parsed = formatUARTdata(uart.read())
                    if parsed:
                        tempOutside, humOutside, batteryValue = parsed
                        if tempOutsideAVG is None:
                            tempOutsideAVG = tempOutside
                        else:
                            tempOutsideAVG = (tempOutside + tempOutsideAVG) / 2
                        if humOutsideAVG is None:
                            humOutsideAVG = humOutside
                        else:
                            humOutsideAVG = (humOutside + humOutsideAVG) / 2
                except Exception as e:
                    print("ERROR reading uart:", e)
            else:
                print("NO UART DATA")

            display.text("IN", 0, 0)
            icons.temperatureSymbol(display, 30, 20, fill)
            data = checkForTempType(sensor.temperature, corf, second)
            if data:
                temperatureNow, corf = data
            display.printstring(45, 20, f"{temperatureNow} {corf}", ariblk)
            icons.humiditySymbol(display, 27, 40)
            display.printstring(45, 42, f"{round(sensor.relative_humidity, 1)}%", ariblk)

            if isinstance(tempOutside, (int, float)):
                temperatureNowOutside, _ = checkForTempType(tempOutside, corf)
                fill = round(tempOutside // 2.5)
            else:
                temperatureNowOutside = tempOutside
                fill = 0

            icons.temperatureSymbol(display2, 30, 20, fill)
            icons.humiditySymbol(display2, 27, 40)
            display2.text("OUT", 0, 0)
            display2.printstring(45, 20, f"{temperatureNowOutside} {corf}", ariblk)

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

            if str(timeNow[4] * 60 + timeNow[5]).endswith("0"):
                if status == "false":
                    with open("sent.dat", "w") as f:
                        f.write("true")
                    print("Time to send")
                    try:
                        response = urequests.get(f"http://{ip}:{port}/time")
                        timeNow = response.json()
                        response.close()
                        rtc.datetime((int(timeNow["year"]), int(timeNow["month"]), int(timeNow["day"]), int(timeNow["weekday"]), int(timeNow["hour"]), int(timeNow["minute"]), int(timeNow["second"]), 0))
                        headers = {
                            "macAddress": macAddress,
                            "time": int(timeNow["unix"]),
                            "temp": round(tempAverage, 1),
                            "timeStamp": int(timeNow["minuteSinceToday"])/10 - 1,
                            "humidity": round(humAverage)
                        }
                        response = urequests.post(f"http://{ip}:{port}/create/0", json=headers)
                        response.close()
                        tempAverage = sensor.temperature
                        humAverage = sensor.relative_humidity
                        if tempOutsideAVG is not None:
                            headers = {
                                "macAddress": macAddress,
                                "time": int(timeNow["unix"]),
                                "temp": round(tempOutsideAVG, 1),
                                "timeStamp": int(timeNow["minuteSinceToday"])/10 - 1,
                                "humidity": round(humOutsideAVG)
                            }
                            response = urequests.post(f"http://{ip}:{port}/create/1", json=headers)
                            response.close()
                            tempOutsideAVG = None
                            humOutsideAVG = None
                        else:
                            tempOutside = "N/A"
                            humOutside = "N/A"
                    except Exception as e:
                        print(e)
                        set_api_status(False)

                    try:
                        if batteryValue:
                            battery_numeric = str(int(batteryValue[1:]))
                            response = urequests.post(f"http://{ip}:{port}/updateBattery/1/{battery_numeric}")
                            response.close()
                    except Exception as e:
                        print("Did not send value", e)
            else:
                if status == "true":
                    with open("sent.dat", "w") as f:
                        f.write("false")
        else:
            display2.fill(0)
            display2.hline(0, 14, 128, 0xffff)
            timeNow = rtc.datetime()
            second = timeNow[6]
            display2.text("IN", 25, 2)
            display2.text("OUT", 85, 2)

            if uart.any():
                try:
                    parsed = formatUARTdata(uart.read())
                    if parsed:
                        tempOutside, humOutside, _ = parsed
                except Exception as e:
                    print("ERROR reading uart:", e)

            fill = round(sensor.temperature // 2.5)
            icons.temperatureSymbol(display2, 3, 20, fill)
            data = checkForTempType(sensor.temperature, corf, second)
            if data:
                temperatureNow, corf = data
            display2.printstring(18, 20, f"{temperatureNow} {corf}", REFSAN12)
            icons.humiditySymbol(display2, 0, 40)
            display2.printstring(18, 42, f"{round(sensor.relative_humidity, 1)}%", REFSAN12)

            if isinstance(tempOutside, (int, float)):
                temperatureNowOutside, _ = checkForTempType(tempOutside, corf)
                fill = round(tempOutside // 2.5)
            else:
                temperatureNowOutside = tempOutside
                fill = 0

            icons.temperatureSymbol(display2, 68, 20, fill)
            icons.humiditySymbol(display2, 65, 40)
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
                if not is_wifi_thread_running():
                    set_wifi_thread_flag(True)
                    try:
                        _thread.start_new_thread(connectThread, ())
                    except Exception as e:
                        print("Failed to start Wi-Fi thread:", e)
                        set_wifi_thread_flag(False)
            elif not get_api_status():
                display.fill(0)
                display.hline(0, 14, 128, 0xffff)
                icons.wifiSymbol(display, 114, 0)
                display.printstring(0, 20, "API failed.\nTrying to connect...", REFSAN12)
                display.show()
                if not is_api_thread_running():
                    set_api_thread_flag(True)
                    try:
                        _thread.start_new_thread(checkAPIstatus, ())
                    except Exception as e:
                        print("Failed to start API thread:", e)
                        set_api_thread_flag(False)

        time.sleep(1)

except Exception as e:
    print(e)
    machine.reset()
