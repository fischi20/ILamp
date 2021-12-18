import sys
import time
from Adafruit_IO import Client, MQTTClient
from src.config_loader import load_config
from src.adafruit import create_clients, setup_MQTTClient, get_client


config = load_config(__file__)

if not config:
    sys.exit()

def feed_handler(client, feed_id, payload):
    print(f"{feed_id}: {payload}")

create_clients(config["Adafruit_IO_username"], config["Adafruit_IO_key"])
setup_MQTTClient(feed_handler, ['ToggleLight', 'LightColor'])

client = get_client()

client.connect()

# loops to check for new data
client.loop_background()

time.sleep(20)

client.disconnect()