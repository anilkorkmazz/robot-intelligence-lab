from robot_lab.worlds.house import ROOMS

class BeliefState:
    def __init__(self, start_room="Office"):

        if start_room not in ROOMS:
            raise ValueError("Geçersiz başlangıç odası!")

        self.probabilities = {}

        for room in ROOMS:
            if room == start_room:
                self.probabilities[room] = 1.0
            else:
                self.probabilities[room] = 0.0

    def get_probabilities(self):
        return self.probabilities.copy()



