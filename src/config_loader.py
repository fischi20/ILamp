import json
import pathlib

def load_config(main_file):
    """
    Return the config Dictionary if it is found, otherwhise it returns None
    """
    config = None

    # load config from file
    try:
        with open('config.json', 'r', encoding='utf-8') as configfile:
            config = json.load(configfile)
    except FileNotFoundError:
        readme = pathlib.Path(main_file).parent.joinpath('README.md').resolve()
        print(f"Couldn't find config.json file, please check out the {readme}")
    return config
