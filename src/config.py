from characters import characters


config = {
    "auraRepair": False,
    "Shortcut-ContentList": ['alt', 'a'],
    "Shortcut-Pet": ['alt', 'p'],
    "ScreenshotsPath": "./screenshots/",
    "characters": characters,
    "regions": {
        "minimap": (1655, 170, 260, 200),  # (1700, 200, 125, 120)
        "abilities": (625, 779, 300, 155),
        "leaveMenu": (0, 154, 250, 300),
        "buffs": (625, 780, 300, 60),
        "center": (685, 280, 600, 420),
        "portal": (228, 230, 1370, 570),
    },
    "screenResolutionX": 1920,
    "screenResolutionY": 1080,
    "clickableAreaX": 500,
    "clickableAreaY": 250,
    "screenCenterX": 960,
    "screenCenterY": 540,
    "minimapCenterX": 1772,
    "minimapCenterY": 272,
    "move": "right", 
    "blink": "space",
    "meleeAttack": "left",
    "awakening": "v",
    "interact": "g",
    "Specialty1": "mouse1", # mouse1 or mouse2
    "Specialty2": "mouse2", # mouse1 or mouse2
    "delayedStart": 2500,
    "useHealthPot": True,
    "healthPot": "f1",
    "healthPotAtPercent": 0.6,
    "healthCheckX": 690,
    "healthCheckY": 854,
    "blackScreenTimeLimit": 30000,
}