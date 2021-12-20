from sense_hat import SenseHat
from time import sleep
import sys
from Adafruit_IO import Client, MQTTClient
from src.config_loader import load_config
from src.adafruit import create_clients, setup_MQTTClient, get_client



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
        sleep(.5)
        sense.clear()

def feed_handler(client, feed_id, payload):
    """
    Prints the new value every time one of the specified feeds has a new value
    """
    print(f"{feed_id}: {payload}")

config = load_config(__file__)

if not config: # exits if no config was found
    sys.exit()

sense = SenseHat()
sense.clear()
sense.low_light = config.get('low_light_mode') or False

create_clients(config.get("Adafruit_IO_username"), config.get("Adafruit_IO_key"))
setup_MQTTClient(feed_handler, config.get('feeds'))
client = get_client()

client.connect()

# loops to check for new data
client.loop_background()

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
