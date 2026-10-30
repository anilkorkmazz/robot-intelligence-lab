
import unittest

from robot_lab.belief.belief_state import BeliefState
from robot_lab.belief.belief_update import predict_belief


class TestBelief(unittest.TestCase):

    def test_initial_belief(self):
        belief = BeliefState(start_room="Office")
        probabilities = belief.get_probabilities()

        self.assertEqual(probabilities["Office"], 1.0)
        self.assertEqual(probabilities["Hallway"], 0.0)
        self.assertAlmostEqual(sum(probabilities.values()), 1.0)

    def test_one_right(self):
        belief = BeliefState(start_room="Office")
        initial = belief.get_probabilities()

        updated = predict_belief(initial, "RIGHT")

        self.assertAlmostEqual(updated["Office"], 0.2)
        self.assertAlmostEqual(updated["Hallway"], 0.8)
        self.assertAlmostEqual(sum(updated.values()), 1.0)

    def test_two_rights(self):
        belief = BeliefState(start_room="Office")
        current = belief.get_probabilities()

        current = predict_belief(current, "RIGHT")
        current = predict_belief(current, "RIGHT")

        self.assertAlmostEqual(current["Office"], 0.04)
        self.assertAlmostEqual(current["Hallway"], 0.32)
        self.assertAlmostEqual(current["Dining Room"], 0.64)
        self.assertAlmostEqual(sum(current.values()), 1.0)


if __name__ == "__main__":
    unittest.main()
