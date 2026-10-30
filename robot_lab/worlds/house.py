
"""
Define the discrete environment used by the robot.

The environment consists of five rooms connected through
a predefined adjacency structure.
"""

# List of rooms representing the robot's possible states.
ROOMS = [
    "Living Room",
    "Kitchen",
    "Office",
    "Hallway",
    "Dining Room"
]

# Undirected connections between directly accessible rooms.
ROOM_CONNECTIONS = {
    "Living Room": ["Kitchen", "Hallway"],
    "Kitchen": ["Living Room", "Dining Room"],
    "Office": ["Hallway"],
    "Hallway": ["Living Room", "Office", "Dining Room"],
    "Dining Room": ["Kitchen", "Hallway"]
}
