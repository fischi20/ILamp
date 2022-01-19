# from sense_hat import SenseHat
from time import sleep
import sys
from Adafruit_IO import Client, MQTTClient
from src.config_loader import load_config
from src.adafruit import create_clients, setup_MQTTClient, get_client, get_last, upload_data

config = load_config(__file__)
if not config: # exits if no config was found
    sys.exit()

feeds = config.get("feeds") # feeds dictionary
feed_list = list() # feeds list
for(k, value) in feeds.items(): #creates an array of all the feeds for mqtt client
    feed_list.append(value)

#* globals
color = (0, 0, 0)
light_on = False

# sense = SenseHat()
# sense.clear()
# sense.low_light = config.get('low_light_mode') or False


def hex_to_rgb(value):
    """
    Converts a hex value to an RGB tuple

    Argument:
    value - hex value
    """
    value = value.lstrip('#')
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

def set_color(new_color):
    """
    Sets the color of the light

    Argument:
    color - RGB tuple representing a color or hex value
    """
    global color
    if(type(new_color) == str):
        color = hex_to_rgb(new_color)
    
    color = new_color
    if(light_on):
        #updateLight(sense, color)
        print("Light color: " + str(color))

def set_light(state):
    """
    Sets the light on or off

    Argument:
    state - boolean
    """
    global light_on
    light_on = state
    if(light_on):
        set_color(color)
    #else:
    #  sense.clear()   

def updateLight(sense, color):
    """
    Argument:
    sense - senseHat
    color - RGB tuple representing a color
    """
    for x in range(8):
        for y in range(8):
            sense.set_pixel(x,y, color)


# doesn't work
def alarmMode(sense):
    """
    A mode which in case of emergency makes SenseHat blink

    Argument:
    sense - senseHat
    """
    red = (255, 0, 0)
    while True:
        updateLight(sense, red)
        sleep(1)
        sense.clear()

def feed_handler(client, feed_id, payload):
    """
    Prints the new value every time one of the specified feeds has a new value
    """
    if(feed_id == feeds.get("light_toggle")):
        if(payload == 'True'):
            print("Light on")
        else:
            # sense.clear()
            print("Light off")
            
    if(feed_id == feeds.get("light_color")): #handles color change
        set_color(payload)


create_clients(config.get("Adafruit_IO_username"), config.get("Adafruit_IO_key"))
setup_MQTTClient(feed_handler, feed_list)
client = get_client()

client.connect()

set_light(get_last(feeds.get("light_toggle"))) # load the state of the light
set_color(get_last(feeds.get("light_color"))) # load default color from adafruit_io


# loops to check for new data
client.loop_background()

"""
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

    sense.clear(color)
    sleep(5) # sleep for n seconds
"""
