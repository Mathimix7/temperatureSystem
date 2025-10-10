def wifiSymbol(display,x,y):
    #First signal
    display.pixel(x+0,y+3)
    display.pixel(x+1,y+2)
    display.pixel(x+2,y+1)
    display.pixel(x+3,y+0)
    display.pixel(x+4,y+0)
    display.pixel(x+5,y+0)
    display.pixel(x+6,y+0)
    display.pixel(x+7,y+0)
    display.pixel(x+8,y+0)
    display.pixel(x+9,y+0)
    display.pixel(x+10,y+0)
    display.pixel(x+11,y+1)
    display.pixel(x+12,y+2)
    display.pixel(x+13,y+3)
    #Second signal
    display.pixel(x+2,y+5)
    display.pixel(x+3,y+4)
    display.pixel(x+4,y+3)
    display.pixel(x+5,y+3)
    display.pixel(x+6,y+3)
    display.pixel(x+7,y+3)
    display.pixel(x+8,y+3)
    display.pixel(x+9,y+3)
    display.pixel(x+10,y+4)
    display.pixel(x+11,y+5)
    #Third Signal
    display.pixel(x+4,y+7)
    display.pixel(x+5,y+6)
    display.pixel(x+6,y+6)
    display.pixel(x+7,y+6)
    display.pixel(x+8,y+6)
    display.pixel(x+9,y+7)
    #Square
    display.pixel(x+6,y+9)
    display.pixel(x+7,y+9)
    display.pixel(x+6,y+10)
    display.pixel(x+7,y+10)

def temperatureSymbol(display,x,y,fill):
    #Top
    display.pixel(x+3, y+0)
    display.pixel(x+4, y+0)
    display.pixel(x+5, y+0)
    #Lines Left & Right
    display.pixel(x+2, y+1)
    display.pixel(x+6, y+1)
    display.pixel(x+2, y+2)
    display.pixel(x+6, y+2)
    display.pixel(x+2, y+3)
    display.pixel(x+6, y+3)
    display.pixel(x+2, y+4)
    display.pixel(x+6, y+4)
    display.pixel(x+2, y+5)
    display.pixel(x+6, y+5)
    display.pixel(x+2, y+6)
    display.pixel(x+6, y+6)
    display.pixel(x+2, y+7)
    display.pixel(x+6, y+7)
    display.pixel(x+2, y+8)
    display.pixel(x+6, y+8)
    #Ball Bottom
    display.pixel(x+1, y+9)
    display.pixel(x+7, y+9)
    display.pixel(x+1, y+10)
    display.pixel(x+7, y+10)
    display.pixel(x+0, y+11)
    display.pixel(x+8, y+11)
    display.pixel(x+0, y+12)
    display.pixel(x+8, y+12)
    display.pixel(x+1, y+13)
    display.pixel(x+7, y+13)
    display.pixel(x+2, y+14)
    display.pixel(x+6, y+14)
    #Base
    display.pixel(x+3,y+15)
    display.pixel(x+4,y+15)
    display.pixel(x+5,y+15)
    #Wind Representation
    #First
    display.pixel(x+8,y+2)
    display.pixel(x+9,y+2)
    display.pixel(x+10,y+2)
    #Second
    display.pixel(x+8,y+4)
    display.pixel(x+9,y+4)
    #Third
    display.pixel(x+8,y+6)
    display.pixel(x+9,y+6)
    display.pixel(x+10,y+6)
    #Fill
    if fill >= 1:
        display.pixel(x+3,y+14)
        display.pixel(x+4,y+14)
        display.pixel(x+5,y+14)
    if fill >= 2:
        display.pixel(x+2,y+13)
        display.pixel(x+3,y+13)
        display.pixel(x+4,y+13)
        display.pixel(x+5,y+13)
        display.pixel(x+6,y+13)
    if fill >= 3:
        display.pixel(x+1,y+12)
        display.pixel(x+2,y+12)
        display.pixel(x+3,y+12)
        display.pixel(x+4,y+12)
        display.pixel(x+5,y+12)
        display.pixel(x+6,y+12)
        display.pixel(x+7,y+12)
    if fill >= 4:
        display.pixel(x+1,y+11)
        display.pixel(x+2,y+11)
        display.pixel(x+3,y+11)
        display.pixel(x+4,y+11)
        display.pixel(x+5,y+11)
        display.pixel(x+6,y+11)
        display.pixel(x+7,y+11)
    if fill >= 5:
        display.pixel(x+2,y+10)
        display.pixel(x+3,y+10)
        display.pixel(x+4,y+10)
        display.pixel(x+5,y+10)
        display.pixel(x+6,y+10)
    if fill >= 6:
        display.pixel(x+2,y+9)
        display.pixel(x+3,y+9)
        display.pixel(x+4,y+9)
        display.pixel(x+5,y+9)
        display.pixel(x+6,y+9)
    if fill >= 7:
        display.pixel(x+3,y+8)
        display.pixel(x+4,y+8)
        display.pixel(x+5,y+8)
    if fill >= 8:
        display.pixel(x+3,y+7)
        display.pixel(x+4,y+7)
        display.pixel(x+5,y+7)
    if fill >= 9:
        display.pixel(x+3,y+6)
        display.pixel(x+4,y+6)
        display.pixel(x+5,y+6)
    if fill >= 10:
        display.pixel(x+3,y+5)
        display.pixel(x+4,y+5)
        display.pixel(x+5,y+5)
    if fill >= 11:
        display.pixel(x+3,y+4)
        display.pixel(x+4,y+4)
        display.pixel(x+5,y+4)
    if fill >= 12:
        display.pixel(x+3,y+3)
        display.pixel(x+4,y+3)
        display.pixel(x+5,y+3)
    if fill >= 13:
        display.pixel(x+3,y+2)
        display.pixel(x+4,y+2)
        display.pixel(x+5,y+2)
    if fill >= 14:
        display.pixel(x+3,y+1)
        display.pixel(x+4,y+1)
        display.pixel(x+5,y+1)
        
def humiditySymbol(display,x,y):
    #Triangle top
    display.pixel(x+7,y+0)
    display.pixel(x+6,y+1)
    display.pixel(x+8,y+1)
    display.pixel(x+5,y+2)
    display.pixel(x+9,y+2)
    display.pixel(x+4,y+3)
    display.pixel(x+10,y+3)
    display.pixel(x+3,y+4)
    display.pixel(x+11,y+4)
    display.pixel(x+2,y+5)
    display.pixel(x+12,y+5)
    display.pixel(x+1,y+6)
    display.pixel(x+13,y+6)
    display.pixel(x+0,y+7)
    display.pixel(x+14,y+7)
    display.pixel(x+0,y+8)
    display.pixel(x+14,y+8)
    display.pixel(x+0,y+9)
    display.pixel(x+14,y+9)
    display.pixel(x+0,y+10)
    display.pixel(x+14,y+10)
    display.pixel(x+0,y+11)
    display.pixel(x+14,y+11)
    display.pixel(x+1,y+12)
    display.pixel(x+13,y+12)
    display.pixel(x+2,y+13)
    display.pixel(x+12,y+13)
    display.pixel(x+3,y+14)
    display.pixel(x+11,y+14)
    #Bottom/Base
    display.pixel(x+4,y+15)
    display.pixel(x+5,y+15)
    display.pixel(x+6,y+15)
    display.pixel(x+7,y+15)
    display.pixel(x+8,y+15)
    display.pixel(x+9,y+15)
    display.pixel(x+10,y+15)
    # % sign
    #First dot
    display.pixel(x+4, y+7)
    display.pixel(x+5, y+7)
    display.pixel(x+4, y+8)
    display.pixel(x+5, y+8)
    #Line
    display.line(x+5,y+11,x+9,y+7, 0xffff)
    #Second dot
    display.pixel(x+9,y+10)
    display.pixel(x+10,y+10)
    display.pixel(x+9,y+11)
    display.pixel(x+10,y+11)

def batterySymbol(display, x, y, fill_level):
    """
    Draw a battery icon with fill level
    fill_level: 0-4 (0=empty, 4=full)
    Battery dimensions: 18x10 pixels
    """
    # Battery body outline - 10 pixels tall
    display.rect(x, y, 16, 10, 0xffff)
    
    # Battery tip/terminal - centered vertically
    display.rect(x+16, y+3, 2, 4, 0xffff)
    
    # Fill battery based on level (each segment is 3 pixels wide and 6 pixels tall)
    if fill_level >= 1:
        display.fill_rect(x+2, y+2, 3, 6, 0xffff)  # First segment
    if fill_level >= 2:
        display.fill_rect(x+5, y+2, 3, 6, 0xffff)  # Second segment
    if fill_level >= 3:
        display.fill_rect(x+8, y+2, 3, 6, 0xffff)  # Third segment
    if fill_level >= 4:
        display.fill_rect(x+11, y+2, 3, 6, 0xffff)  # Fourth segment (full)

def getBatteryLevel(voltage):
    """
    Convert voltage (in millivolts) to battery fill level (0-4)
    Typical Li-ion/LiPo voltage range: 3.0V (empty) to 4.2V (full)
    """
    voltage_mv = voltage
    
    # Convert to volts if needed
    if voltage_mv > 1000:  # Assume it's in millivolts
        voltage_v = voltage_mv / 1000.0
    else:
        voltage_v = voltage_mv
    
    # Battery voltage thresholds
    if voltage_v >= 4.0:
        return 4  # Full
    elif voltage_v >= 3.7:
        return 3  # Good
    elif voltage_v >= 3.4:
        return 2  # Medium
    elif voltage_v >= 3.1:
        return 1  # Low
    else:
        return 0  # Empty/Critical


