from robot_lab.worlds.house import ROOMS
from robot_lab.motion.movement_rules import get_target_room
from robot_lab.motion.motion_model import sample_motion

class Robot:
    def __init__(self, start_room="Office"):
        if start_room not in ROOMS:
            raise ValueError("Geçersiz başlangıç odası!")

        self.current_room = start_room

    def get_position(self):
        return self.current_room


    def move(self, action):
        current_room = self.current_room
        target_room = get_target_room(current_room, action)
        self.current_room = target_room
        return self.current_room


    def move_probabilistic(self, action):
        # 1. Robotun mevcut konumunu öğren
        current_room = self.current_room

        # 2. Olasılıklara göre bir hareket sonucu seç
        selected_room = sample_motion(current_room, action)

        # 3. Robotun gerçek konumunu güncelle
        self.current_room = selected_room

        # 4. Yeni konumu döndür
        return self.current_room
