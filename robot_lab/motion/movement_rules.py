from robot_lab.worlds.house import ROOMS
from robot_lab.motion.actions import ACTIONS



# Her odada hareket komutlarının hedeflediği odalar

MOVEMENT_RULES = {
    "Living Room": {
        "RIGHT": "Kitchen",
        "DOWN": "Hallway"
    },
    "Kitchen": {
        "LEFT": "Living Room",
        "DOWN": "Dining Room"
    },
    "Office": {
        "RIGHT": "Hallway"
    },
    "Hallway": {
        "LEFT": "Office",
        "RIGHT": "Dining Room",
        "UP": "Living Room"
    },
    "Dining Room": {
        "LEFT": "Hallway",
        "UP": "Kitchen"
    }
}


def get_target_room(current_room, action):
    if current_room not in ROOMS:
        raise ValueError("Geçersiz oda!")

    if action not in ACTIONS:
        raise ValueError("Geçersiz hareket komutu!")

    room_rules = MOVEMENT_RULES[current_room]
    target_room = room_rules.get(action, current_room)
    return target_room
