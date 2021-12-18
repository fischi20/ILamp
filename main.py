from sense_hat import SenseHat
from time import sleep


def updateLight(sense, color):
    """
    Argument:
    sense - senseHat
    color - RGB tuple representing a color
    """
    for x in range(8):
        for y in range(8):
            sense.set_pixel(x,y, color)


sense = SenseHat()
sense.clear()
# sense.low_light = True

color = (255,255,141) # mild yellow
room_temperature = 20

while True:
    temp = sense.get_temperature(); # getting current temperature
    print(temp) 

    if temp < room_temperature:
        color = (160, 219, 255)

    if temp >= room_temperature:
        if temp < room_temperature + 2:
            color = (254, 253, 172)

        elif temp < room_temperature + 4:
            color = (255, 205, 0)

        else:
            color = (227, 147, 0) # dark orange 

    updateLight(sense, color)
    sleep(5) # sleep for n seconds