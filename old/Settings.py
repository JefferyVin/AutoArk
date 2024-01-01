from config import config

def init():
    global states 
    global DEBUG
    DEBUG = False
    states = {
    "currentCharacter": 0,
    "status": "inCity",
    "floor3Mode": "true",
    "deathCount": 0,
    "moveToX": config["screenCenterX"],
    "moveToY": config["screenCenterY"],
    "healthPotCount": 0,
    "abilities": [],
    "abilityScreenshots": [],
    "moveTime": 0,
    }