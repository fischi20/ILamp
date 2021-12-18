import sys
from src.config_loader import load_config

config = load_config(__file__)

if not config:
    sys.exit()
