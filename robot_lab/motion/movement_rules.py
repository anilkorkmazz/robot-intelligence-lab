
"""
Define directional movement rules for the five-room environment.

This module maps movement commands to connected rooms and
determines the target location for deterministic robot motion.
"""

from robot_lab.worlds.house import ROOMS
from robot_lab.motion.actions import ACTIONS


# Map each room to its valid directional transitions.
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
    """
    Determine the target room for a directional movement command.

    If no connection exists in the requested direction,
    the robot remains in its current room.

    Args:
        current_room (str): Robot's current location.
        action (str): Directional movement command.

    Returns:
        str: Target room, or the current room if movement is blocked.

    Raises:
        ValueError: If the room or movement command is invalid.
    """

    # Validate the current room and movement command.
    if current_room not in ROOMS:
        raise ValueError("Invalid room!")

    if action not in ACTIONS:
        raise ValueError("Invalid movement command!")

    # Retrieve the valid directional transitions for the current room.
    room_rules = MOVEMENT_RULES[current_room]

    # Remain in the current room if the direction has no connection.
    target_room = room_rules.get(action, current_room)

    return target_room
