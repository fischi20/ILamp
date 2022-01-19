from Adafruit_IO import Client, MQTTClient

aio = None
client = None
aio_feeds = dict()


def create_clients(username, key):
    global aio
    global client
    aio = Client(username, key)
    client = MQTTClient(username, key)
    for f in aio.feeds():
        print(f.name)
        aio_feeds[f.name] = f.id

def get_feed_id(feed_name):
    """
    Returns the feed id of the specified feed name
    """
    return aio_feeds.get(feed_name)

def get_last(feed_name):
    """
    Returns the last value of the specified feed
    """
    return aio.receive_previous(get_feed_id(feed_name)).value

def setup_MQTTClient(feed_update, feeds):

    def message(client, feed_id, payload):
        feed_update(client, feed_id, payload)

    def connected(client):
        for feed in feeds:
            client.subscribe(feed)

    def disconnected(client):
        print('Disconnected from Adafruit IO')


    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message

def get_client():
    return client

def get_aio_client():
    return aio
