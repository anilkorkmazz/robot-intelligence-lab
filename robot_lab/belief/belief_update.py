from robot_lab.worlds.house import ROOMS
from robot_lab.motion.motion_model import get_motion_probabilities
from robot_lab.motion.transition_matrix import create_transition_matrix

def predict_belief(current_belief, action):

    # Her odanın yeni olasılığı başlangıçta sıfır
    new_belief = {}

    for room in ROOMS:
        new_belief[room] = 0.0

    # Olası bütün başlangıç odalarını incele
    for current_room in ROOMS:

        current_probability = current_belief[current_room]

        # Bu odadan hareketin olası sonuçlarını bul
        motion_probabilities = get_motion_probabilities(
            current_room, action
        )

        # Her olası hedef odanın katkısını hesapla
        for target_room, transition_probability in motion_probabilities.items():

            contribution = current_probability * transition_probability

            new_belief[target_room] += contribution

    return new_belief



def predict_belief_with_matrix(current_belief, action):

    # 1. Hareketin geçiş matrisini oluştur
    transition_matrix = create_transition_matrix(action)

    # 2. Yeni inanç dağılımını saklayacağımız sözlük
    new_belief = {}

    # 3. Her hedef oda için olasılık hesapla
    for target_index, target_room in enumerate(ROOMS):

        total_probability = 0.0

        # 4. Bütün başlangıç odalarının katkılarını topla
        for current_index, current_room in enumerate(ROOMS):

            current_probability = current_belief[current_room]

            transition_probability = transition_matrix[
                current_index
            ][target_index]

            contribution = (
                current_probability * transition_probability
            )

            total_probability += contribution

        # 5. Hesaplanan değeri hedef odaya kaydet
        new_belief[target_room] = total_probability

    return new_belief
