
"""
Unit tests for robot simulation history management.

These tests verify initial state recording, history growth,
belief preservation, and protection against external modifications.
"""

import unittest

from robot_lab.core.simulation import RobotSimulation


class TestSimulationHistory(unittest.TestCase):
    """Test simulation history recording and data integrity."""

    def test_initial_history(self):
        """Verify that initialization creates a valid starting record."""

        simulation = RobotSimulation(start_room="Office")
        history = simulation.get_history()

        # The initial state is recorded before any movement.
        self.assertEqual(len(history), 1)

        first_record = history[0]

        self.assertEqual(first_record["step"], 0)
        self.assertEqual(first_record["action"], "START")
        self.assertEqual(first_record["true_position"], "Office")
        self.assertAlmostEqual(first_record["belief"]["Office"], 1.0)

    def test_history_grows(self):
        """Verify that each movement appends a new history record."""

        simulation = RobotSimulation(start_room="Office")

        simulation.step("RIGHT")
        simulation.step("RIGHT")
        simulation.step("UP")

        history = simulation.get_history()

        # Three movements produce four records, including the initial state.
        self.assertEqual(len(history), 4)
        self.assertEqual(simulation.step_count, 3)

        self.assertEqual(history[1]["action"], "RIGHT")
        self.assertEqual(history[2]["action"], "RIGHT")
        self.assertEqual(history[3]["action"], "UP")

        self.assertEqual(history[3]["step"], 3)

    def test_belief_history(self):
        """Verify that previous belief distributions remain unchanged."""

        simulation = RobotSimulation(start_room="Office")

        simulation.step("RIGHT")
        simulation.step("RIGHT")

        history = simulation.get_history()

        # Initial belief must remain unchanged after subsequent movements.
        self.assertAlmostEqual(
            history[0]["belief"]["Office"],
            1.0
        )

        # Belief after the first RIGHT action.
        self.assertAlmostEqual(
            history[1]["belief"]["Office"],
            0.2
        )

        self.assertAlmostEqual(
            history[1]["belief"]["Hallway"],
            0.8
        )

        # Belief after the second RIGHT action.
        self.assertAlmostEqual(
            history[2]["belief"]["Office"],
            0.04
        )

        self.assertAlmostEqual(
            history[2]["belief"]["Hallway"],
            0.32
        )

        self.assertAlmostEqual(
            history[2]["belief"]["Dining Room"],
            0.64
        )

        # Each recorded belief distribution must remain normalized.
        for record in history:
            self.assertAlmostEqual(
                sum(record["belief"].values()),
                1.0
            )

    def test_history_copy_protection(self):
        """Verify that modifying returned history does not affect stored data."""

        simulation = RobotSimulation(start_room="Office")
        simulation.step("RIGHT")

        history_copy = simulation.get_history()

        # Modify a nested belief value in the returned copy.
        history_copy[0]["belief"]["Office"] = 0.5

        # The original simulation history must retain its initial value.
        original_history = simulation.get_history()

        self.assertAlmostEqual(
            original_history[0]["belief"]["Office"],
            1.0
        )


if __name__ == "__main__":
    unittest.main()
