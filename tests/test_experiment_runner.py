
"""
Integration tests for the robot experiment runner.

These tests verify experiment output files, simulation history,
consistency between CSV and Markdown reports, and final belief states.
"""

import csv
import tempfile
import unittest

from robot_lab.experiments.experiment_runner import run_experiment


class TestExperimentRunner(unittest.TestCase):
    """Test the integrated experiment execution and generated outputs."""

    def test_output_files_created(self):
        """Verify that the experiment generates three non-empty output files."""

        with tempfile.TemporaryDirectory() as temp_dir:

            result = run_experiment(
                ["RIGHT", "RIGHT", "UP"],
                temp_dir
            )

            # Verify the PNG, CSV, and Markdown outputs.
            for key in ["png_path", "csv_path", "report_path"]:

                path = result[key]

                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 0)

    def test_history_length(self):
        """Verify the initial state and three movement records."""

        with tempfile.TemporaryDirectory() as temp_dir:

            result = run_experiment(
                ["RIGHT", "RIGHT", "UP"],
                temp_dir
            )

            history = result["history"]

            # One initial state and three movements produce four records.
            self.assertEqual(len(history), 4)

            self.assertEqual(history[0]["step"], 0)
            self.assertEqual(history[0]["action"], "START")
            self.assertEqual(history[0]["true_position"], "Office")

            self.assertEqual(history[-1]["step"], 3)

            actual_actions = [
                record["action"]
                for record in history
            ]

            expected_actions = [
                "START",
                "RIGHT",
                "RIGHT",
                "UP"
            ]

            self.assertEqual(actual_actions, expected_actions)

    def test_csv_report_consistency(self):
        """Verify that CSV and Markdown contain matching simulation records."""

        with tempfile.TemporaryDirectory() as temp_dir:

            result = run_experiment(
                ["RIGHT", "RIGHT", "UP"],
                temp_dir
            )

            # Read the exported CSV records.
            with result["csv_path"].open(
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                csv_rows = list(csv.DictReader(file))

            # Read the generated Markdown report.
            report_text = result["report_path"].read_text(
                encoding="utf-8"
            )

            self.assertEqual(
                len(csv_rows),
                len(result["history"])
            )

            # Compare recorded movement results across both output formats.
            # Actual positions are stochastic, so fixed positions are not expected.
            for row in csv_rows:

                expected_line = (
                    f"| {row['Step']} | "
                    f"{row['Action']} | "
                    f"{row['True Position']} |"
                )

                self.assertIn(
                    expected_line,
                    report_text
                )

    def test_final_belief(self):
        """Verify the expected Markov belief after RIGHT, RIGHT, UP."""

        with tempfile.TemporaryDirectory() as temp_dir:

            result = run_experiment(
                ["RIGHT", "RIGHT", "UP"],
                temp_dir
            )

            final_belief = result["history"][-1]["belief"]

            # Expected distribution from the stochastic motion model.
            expected = {
                "Living Room": 0.256,
                "Kitchen": 0.512,
                "Office": 0.04,
                "Hallway": 0.064,
                "Dining Room": 0.128
            }

            # Compare probabilities with floating-point tolerance.
            for room, probability in expected.items():

                self.assertAlmostEqual(
                    final_belief[room],
                    probability
                )

            # A valid belief distribution must remain normalized.
            self.assertAlmostEqual(
                sum(final_belief.values()),
                1.0
            )


if __name__ == "__main__":
    unittest.main()
