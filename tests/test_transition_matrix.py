
"""
Unit tests for Markov state transition matrices.

These tests verify matrix dimensions, transition probabilities,
and consistency between direct and matrix-based belief prediction.
"""

import unittest

from robot_lab.worlds.house import ROOMS
from robot_lab.motion.actions import ACTIONS
from robot_lab.motion.transition_matrix import create_transition_matrix
from robot_lab.belief.belief_state import BeliefState
from robot_lab.belief.belief_update import (
    predict_belief,
    predict_belief_with_matrix
)


class TestTransitionMatrix(unittest.TestCase):
    """Test transition matrix properties and belief prediction consistency."""

    def test_matrix_dimensions(self):
        """Verify that the transition matrix has N x N dimensions."""

        matrix = create_transition_matrix("RIGHT")

        self.assertEqual(len(matrix), len(ROOMS))

        for row in matrix:
            self.assertEqual(len(row), len(ROOMS))

    def test_matrix_probabilities(self):
        """Verify that transition matrices are row-stochastic."""

        for action in ACTIONS:

            matrix = create_transition_matrix(action)

            for row in matrix:

                # Each row represents a normalized probability distribution.
                self.assertAlmostEqual(sum(row), 1.0)

                # Transition probabilities must remain within [0, 1].
                for probability in row:

                    self.assertGreaterEqual(probability, 0.0)
                    self.assertLessEqual(probability, 1.0)

    def test_belief_methods_match(self):
        """Verify that direct and matrix-based predictions produce equal beliefs."""

        belief = BeliefState(start_room="Office")
        initial_belief = belief.get_probabilities()

        for action in ACTIONS:

            result_1 = predict_belief(
                initial_belief, action
            )

            result_2 = predict_belief_with_matrix(
                initial_belief, action
            )

            # Both implementations must agree for every room.
            for room in ROOMS:

                self.assertAlmostEqual(
                    result_1[room],
                    result_2[room]
                )


if __name__ == "__main__":
    unittest.main()
