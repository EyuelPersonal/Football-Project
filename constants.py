import json

LINK = DRIVER_PATH = PROXY = ""

def __init__():
    global LINK, DRIVER_PATH, PROXY
    try:
        with open("/Users/eyuelmelese/FootballSprider/settings.json") as data:
            data = json.load(data)
    except Exception as e:
        print(e)
    LINK = data['link']
    DRIVER_PATH = data['driver_path']
    PROXY = data['proxy']

