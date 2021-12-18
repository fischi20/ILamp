import json
import pathlib

config = None

# load config from file
try:
    with open('config2.json', 'r') as configfile:
        config = json.load(configfile)
except FileNotFoundError as e:
    readme = pathlib.Path(__file__).parent.joinpath('README.md').resolve()
    print(f"Couldn't find config.json file, please check out the {readme}")

# If the config file doesn't exist the user is required to set it up
if not config:
    quit()

# Do stuff with config here
print(config)