# Robotun hareket edebileceği odalar
ROOMS = [
    "Living Room",
    "Kitchen",
    "Office",
    "Hallway",
    "Dining Room"
]
# Odalar arasındaki doğrudan bağlantılar
ROOM_CONNECTIONS = {
    "Living Room": ["Kitchen", "Hallway"],
    "Kitchen": ["Living Room", "Dining Room"],
    "Office": ["Hallway"],
    "Hallway": ["Living Room", "Office", "Dining Room"],
    "Dining Room": ["Kitchen", "Hallway"]
}

