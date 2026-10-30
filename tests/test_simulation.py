
"""
Unit tests for robot simulation and probabilistic movement.

These tests verify initialization, stochastic movement,
Markov belief prediction, and invalid action handling.
"""

import unittest

from robot_lab.core.simulation import RobotSimulation
from robot_lab.worlds.house import ROOMS


class TestRobotSimulation(unittest.TestCase):
    """Test robot simulation behavior and belief state consistency."""

    def test_initial_state(self):
        """Verify the initial robot position and normalized belief state."""

        simulation = RobotSimulation(start_room="Office")

        self.assertEqual(
            simulation.robot.get_position(),
            "Office"
        )

        self.assertEqual(
            simulation.step_count,
            0
        )

        self.assertAlmostEqual(
            simulation.current_belief["Office"],
            1.0
        )

        # The initial belief distribution must be normalized.
        self.assertAlmostEqual(
            sum(simulation.current_belief.values()),
            1.0
        )

    def test_one_right(self):
        """Verify stochastic motion and belief prediction after one RIGHT action."""

        simulation = RobotSimulation(start_room="Office")

        result = simulation.step("RIGHT")

        self.assertEqual(
            result["step"],
            1
        )

        self.assertEqual(
            result["action"],
            "RIGHT"
        )

        # Ground-truth motion is stochastic, so either outcome is valid.
        self.assertIn(
            result["true_position"],
            ["Office", "Hallway"]
        )

        self.assertEqual(
            simulation.robot.get_position(),
            result["true_position"]
        )

        # Expected Markov belief after one RIGHT action.
        self.assertAlmostEqual(
            result["belief"]["Office"],
            0.2
        )

        self.assertAlmostEqual(
            result["belief"]["Hallway"],
            0.8
        )

        self.assertAlmostEqual(
            sum(result["belief"].values()),
            1.0
        )

    def test_two_rights(self):
        """Verify belief propagation after two consecutive RIGHT actions."""

        simulation = RobotSimulation(start_room="Office")

        simulation.step("RIGHT")
        result = simulation.step("RIGHT")

        self.assertEqual(
            result["step"],
            2
        )

        self.assertEqual(
            simulation.step_count,
            2
        )

        # The sampled position must remain within the defined environment.
        self.assertIn(
            result["true_position"],
            ROOMS
        )

        # Expected belief after two RIGHT actions.
        self.assertAlmostEqual(
            result["belief"]["Office"],
            0.04
        )

        self.assertAlmostEqual(
            result["belief"]["Hallway"],
            0.32
        )

        self.assertAlmostEqual(
            result["belief"]["Dining Room"],
            0.64
        )

        self.assertAlmostEqual(
            sum(result["belief"].values()),
            1.0
        )

    def test_invalid_action(self):
        """Verify that invalid actions are rejected without changing simulation state."""

        simulation = RobotSimulation(start_room="Office")

        # Invalid commands must raise an error before updating any state.
        with self.assertRaises(ValueError):
            simulation.step("JUMP")

        self.assertEqual(
            simulation.robot.get_position(),
            "Office"
        )

        self.assertEqual(
            simulation.step_count,
            0
        )

        self.assertAlmostEqual(
            simulation.current_belief["Office"],
            1.0
        )

        self.assertAlmostEqual(
            sum(simulation.current_belief.values()),
            1.0
        )


if __name__ == "__main__":
    unittest.main()
