from robot_lab.worlds.house import ROOMS
from robot_lab.motion.motion_model import get_motion_probabilities

def create_transition_matrix(action):

    # 1. Boş bir matris oluştur
    matrix = []

    # 2. Her başlangıç odasını incele
    for current_room in ROOMS:

        # Bu oda için hareket olasılıklarını öğren
        motion_probabilities = get_motion_probabilities(
            current_room, action
        )

        # 3. Matrisin yeni satırını oluştur
        row = []

        for target_room in ROOMS:

            probability = motion_probabilities.get(target_room, 0.0)

            row.append(probability)

        # 4. Oluşturduğumuz satırı matrise ekle
        matrix.append(row)

    # 5. Tamamlanan matrisi döndür
    return matrix
