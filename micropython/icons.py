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

