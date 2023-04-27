import logging
import json

# Load logger configs
with open('configs.json') as config_file:
    data = json.load(config_file)

logger = logging.getLogger("ScraperLogger")
logging.basicConfig(level = data['LOG_LEVEL'], format = data['LOG_FORMAT'], handlers = [logging.FileHandler(filename = data['LOG_FILE'], encoding='utf-8', mode='a+')])

