#from sense_hat import SenseHat
from time import sleep
import sys
from Adafruit_IO import Client, MQTTClient
from src.config_loader import load_config
from src.adafruit import create_clients, setup_MQTTClient, get_client, get_last, upload_data


def hex_to_rgb(value):
    """
    Converts a hex value to an RGB tuple

    Argument:
    value - hex value
    """
    value = value.lstrip('#')
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))

def set_color(new_color, primary_color = True):
    """
    Sets the color of the light

    Argument:
    color - RGB tuple representing a color or hex value
    primary_color - boolean, True if the color is the primary color, False if it is the secondary color
    """
    global color, secondary_color
    if type(new_color) == str:
        if primary_color == True:
            color = hex_to_rgb(new_color)
        else:
            secondary_color = hex_to_rgb(new_color)
    
    if primary_color == True:
        color = new_color
    else:
        secondary_color = new_color

def lerp_color(cold, hot, t):
    """
    Linearly interpolates between two colors

    Arguments:
    color1 - RGB tuple representing a color
    color2 - RGB tuple representing a color
    t - float between 0 and 1
    """
    r1, g1, b1 = cold
    r2, g2, b2 = hot
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return (r, g, b)

def set_light(state):
    """
    Sets the light on or off

    Argument:
    state - boolean
    """
    global light_on
    light_on = state

def updateLight(sense, color):
    """
    Argument:
    sense - senseHat
    color - RGB tuple representing a color
    """
    for x in range(8):
        for y in range(8):
            sense.set_pixel(x,y, color)

def feed_handler(client, feed_id, payload):
    """
    Prints the new value every time one of the specified feeds has a new value
    """
    if(feed_id == feeds.get("light_toggle")):
        if(payload == 'True'):
            print("Light on")
        else:
            print("Light off")
            
    if(feed_id == feeds.get("light_color")): #handles color change
        print("primary color changed to: " + payload)
        set_color(payload)

    if(feed_id == feeds.get("secondary_color")):
        print("secondary color changed to: " + payload)
        set_color(payload, False)

def calc_color_percent(min, max, temp):
    """
    Calculates the percentage of the color range that the temperature is in

    Arguments:
    min - minimum temperature
    max - maximum temperature
    temp - temperature
    """
    tp = (temp-min)/(max-min)
    if tp > 1:
      tp = 1
    if tp < 0:
      tp = 0
    return tp


if __name__ == "__main__":
    config = load_config(__file__)
    if not config: # exits if no config was found
        sys.exit()

    feeds = config.get("feeds") # feeds dictionary
    feed_list = list() # feeds list
    for(k, value) in feeds.items(): #creates an array of all the feeds for mqtt client
        feed_list.append(value)

    color = (0, 0, 0)
    secondary_color = (0, 0, 0)
    light_on = False
    min_temp = config.get("min_temp")
    max_temp = config.get("max_temp")
    # sense = SenseHat()
    # sense.clear()
    # sense.low_light = config.get('low_light_mode') or False
    
    create_clients(config.get("Adafruit_IO_username"), config.get("Adafruit_IO_key"))
    setup_MQTTClient(feed_handler, feed_list)
    client = get_client()

    client.connect()

    #get last values
    set_light(get_last(feeds.get("light_toggle"))) # load the state of the light
    set_color(get_last(feeds.get("secondary_color")), False) # load the color of the light
    set_color(get_last(feeds.get("light_color"))) # load default color from adafruit_io

    # loops to check for new data
    client.loop_background()


    while True:
        """
        temp = sense.get_temperature()

        upload_data(feeds.get("temp"), temp) # uploads the temperature to adafruit_io
        upload_data(feeds.get("humidity"), sense.get_humidity()) # uploads the humidity to adafruit_io

        if light_on:
            # calc color
            display_color = lerp_color(secondary_color, color, calc_color_percent(min_temp, max_temp, temp))

            sense.clear(display_color)

            # another approach very similar to the first one
            sense_temp = sense.get_temperature()
            color = lerp_color(cold, hot, get_color_percent(min_temp, max_temp, sense_temp))

            #updateLight(sense, lerp_color(cold, hot, get_color_percent(-20, 40, temp)))
            #updateLight(sense, color)
            sense.clear(color)
        """
        sleep(1) # sleep for n seconds
