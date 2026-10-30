
"""
Unit tests for robot belief visualization and PNG export.

These tests verify plotted room probabilities, figure structure,
and the creation of valid PNG image files.
"""

import unittest
import tempfile

from pathlib import Path

import matplotlib

# Use a non-interactive backend to prevent plot windows during tests.
# This must be configured before importing matplotlib.pyplot.
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from robot_lab.core.simulation import RobotSimulation
from robot_lab.visualization.belief_plot import (
    plot_belief_history,
    save_belief_plot
)


class TestVisualization(unittest.TestCase):
    """Test belief history plotting and image export functionality."""

    def test_five_room_lines(self):
        """Verify that the belief plot contains one line for each room."""

        simulation = RobotSimulation(start_room="Office")
        simulation.step("RIGHT")

        history = simulation.get_history()
        fig = plot_belief_history(history)

        try:
            ax = fig.axes[0]

            # Each of the five rooms must have a separate plot line.
            self.assertEqual(len(ax.lines), 5)

        finally:
            # Close the figure even if an assertion fails.
            plt.close(fig)

    def test_office_line_values(self):
        """Verify the Office belief probabilities across three time steps."""

        simulation = RobotSimulation(start_room="Office")

        simulation.step("RIGHT")
        simulation.step("RIGHT")

        history = simulation.get_history()
        fig = plot_belief_history(history)

        try:
            ax = fig.axes[0]

            # Locate the plot line corresponding to the Office room.
            office_line = None

            for line in ax.lines:
                if line.get_label() == "Office":
                    office_line = line
                    break

            self.assertIsNotNone(office_line)

            # Expected Office belief after zero, one, and two RIGHT actions.
            expected = [1.0, 0.2, 0.04]
            actual = office_line.get_ydata()

            self.assertEqual(len(actual), len(expected))

            for index in range(len(expected)):
                self.assertAlmostEqual(
                    actual[index],
                    expected[index]
                )

        finally:
            plt.close(fig)

    def test_save_belief_plot(self):
        """Verify that saving a belief figure creates a valid PNG file."""

        simulation = RobotSimulation(start_room="Office")

        simulation.step("RIGHT")
        simulation.step("RIGHT")

        history = simulation.get_history()
        fig = plot_belief_history(history)

        try:
            # Use a temporary directory to avoid persistent test files.
            with tempfile.TemporaryDirectory() as temp_dir:

                file_path = Path(temp_dir) / "test_belief.png"

                saved_path = save_belief_plot(
                    fig,
                    file_path
                )

                self.assertTrue(saved_path.is_file())
                self.assertGreater(saved_path.stat().st_size, 0)

                # Verify the standard eight-byte PNG file signature.
                with saved_path.open("rb") as file:
                    signature = file.read(8)

                expected_signature = b"\x89PNG\r\n\x1a\n"

                self.assertEqual(
                    signature,
                    expected_signature
                )

        finally:
            plt.close(fig)


if __name__ == "__main__":
    unittest.main()
