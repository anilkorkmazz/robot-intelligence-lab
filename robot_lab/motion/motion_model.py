import random
from robot_lab.motion.movement_rules import get_target_room


MOVE_SUCCESS_PROBABILITY = 0.8
STAY_PROBABILITY = 0.2


def get_motion_probabilities(current_room, action):

    # 1. Hareketin hedeflediği odayı bul
    target_room = get_target_room(current_room, action)

    # 2. Olasılıkları saklayacağımız sözlüğü oluştur
    probabilities = {}

    # 3. Hedef oda mevcut odayla aynıysa
    if target_room == current_room:

        # Robot kesinlikle bulunduğu odada kalır
        probabilities[current_room] = 1.0

    else:
        # 4. Kapı varsa iki farklı sonuç mümkündür
        # Robot %80 olasılıkla hedef odaya gider
        probabilities[target_room] = MOVE_SUCCESS_PROBABILITY

        # Robot %20 olasılıkla bulunduğu odada kalır
        probabilities[current_room] = STAY_PROBABILITY

    # 5. Hesaplanan olasılıkları döndür
    return probabilities

def sample_motion(current_room, action):
    probabilities = get_motion_probabilities(current_room, action)
    possible_rooms = list(probabilities.keys())
    room_probabilities = list(probabilities.values())

    selected_room = random.choices(
        possible_rooms,
        weights = room_probabilities,
        k=1,
    )[0]

    return selected_room