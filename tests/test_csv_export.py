
"""
Unit tests for exporting robot simulation history to CSV.

These tests verify file creation, CSV structure, movement records,
and the accuracy of exported belief probabilities.
"""

import csv
import tempfile
import unittest

from pathlib import Path

from robot_lab.core.simulation import RobotSimulation
from robot_lab.experiments.csv_export import export_history_to_csv
from robot_lab.worlds.house import ROOMS


class TestCSVExport(unittest.TestCase):
    """Test CSV export functionality for robot simulation history."""

    def test_csv_file_created(self):
        """Verify that exporting simulation history creates a non-empty CSV file."""

        simulation = RobotSimulation(start_room="Office")
        simulation.step("RIGHT")

        history = simulation.get_history()

        # Use a temporary directory to avoid leaving test artifacts.
        with tempfile.TemporaryDirectory() as temp_dir:

            file_path = Path(temp_dir) / "test_history.csv"

            saved_path = export_history_to_csv(
                history,
                file_path
            )

            self.assertTrue(saved_path.is_file())
            self.assertGreater(saved_path.stat().st_size, 0)

    def test_csv_headers_and_rows(self):
        """Verify CSV column order, row counts, and movement sequence."""

        simulation = RobotSimulation(start_room="Office")

        simulation.step("RIGHT")
        simulation.step("RIGHT")
        simulation.step("UP")

        history = simulation.get_history()

        with tempfile.TemporaryDirectory() as temp_dir:

            file_path = Path(temp_dir) / "test_history.csv"

            export_history_to_csv(
                history,
                file_path
            )

            # Read CSV with BOM-compatible UTF-8 encoding.
            with file_path.open(
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                reader = csv.reader(file)
                rows = list(reader)

            # Verify column names and their ordering.
            headers = rows[0]

            expected_headers = [
                "Step",
                "Action",
                "True Position"
            ] + list(ROOMS)

            self.assertEqual(headers, expected_headers)
            self.assertEqual(len(headers), 8)

            # One header row and four simulation records are expected.
            self.assertEqual(len(rows), 5)

            data_rows = rows[1:]

            self.assertEqual(len(data_rows), 4)

            self.assertEqual(
                [row[1] for row in data_rows],
                ["START", "RIGHT", "RIGHT", "UP"]
            )

    def test_csv_belief_values(self):
        """Verify exported belief probabilities after two RIGHT movements."""

        simulation = RobotSimulation(start_room="Office")

        simulation.step("RIGHT")
        simulation.step("RIGHT")

        history = simulation.get_history()

        with tempfile.TemporaryDirectory() as temp_dir:

            file_path = Path(temp_dir) / "test_history.csv"

            export_history_to_csv(
                history,
                file_path
            )

            with file_path.open(
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                reader = csv.DictReader(file)
                rows = list(reader)

            # The third data row represents the second RIGHT movement.
            second_right = rows[2]

            self.assertEqual(second_right["Step"], "2")
            self.assertEqual(second_right["Action"], "RIGHT")

            # Verify deterministic belief predictions despite stochastic motion.
            self.assertAlmostEqual(
                float(second_right["Office"]),
                0.04
            )

            self.assertAlmostEqual(
                float(second_right["Hallway"]),
                0.32
            )

            self.assertAlmostEqual(
                float(second_right["Dining Room"]),
                0.64
            )

            # Belief probabilities must remain normalized.
            total_probability = sum(
                float(second_right[room])
                for room in ROOMS
            )

            self.assertAlmostEqual(
                total_probability,
                1.0
            )


if __name__ == "__main__":
    unittest.main()
