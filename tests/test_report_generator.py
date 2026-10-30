"""Tests for the English, LaTeX-enabled Markdown experiment report."""

import tempfile
import unittest
from pathlib import Path

from robot_lab.core.simulation import RobotSimulation
from robot_lab.experiments.report_generator import generate_experiment_report
from robot_lab.worlds.house import ROOMS


class TestReportGenerator(unittest.TestCase):
    """Verify the generated report against actual simulation history."""

    def make_report(self, actions):
        """Create a report in a temporary folder and return its text and history."""
        simulation = RobotSimulation(start_room="Office")
        for action in actions:
            simulation.step(action)
        history = simulation.get_history()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "test_report.md"
            saved_path = generate_experiment_report(history, path)
            self.assertEqual(saved_path, path)
            self.assertTrue(path.is_file())
            content = path.read_text(encoding="utf-8")
        return content, history

    def test_report_file_created(self):
        """An experiment creates a nonempty Markdown report."""
        content, _ = self.make_report(["RIGHT"])
        self.assertTrue(content.strip())
        self.assertTrue(content.startswith("# Robot Intelligence Lab"))

    def test_report_sections(self):
        """The English report has its required sections and LaTeX equations."""
        content, _ = self.make_report(["RIGHT"])
        sections = [
            "## 1. Experiment Objective",
            "## 2. Initial Conditions",
            "## 3. Action Sequence",
            "## 4. Simulation Results",
            "## 5. Final Belief Distribution",
            "## 6. Experiment Evaluation",
            "## 7. Conclusion",
        ]
        positions = [content.index(section) for section in sections]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("### Markov Motion Prediction", content)
        self.assertIn("### Probability Normalization", content)
        self.assertIn("### Most Probable State", content)
        self.assertIn(r"\mathbf{b}_{t+1} = \mathbf{b}_t\mathbf{T}_{a_t}", content)
        self.assertIn(r"\sum_{x \in \mathcal{X}}", content)
        self.assertIn("$$", content)

    def test_report_movement_records(self):
        """All recorded steps, commands and sampled positions appear in order."""
        content, history = self.make_report(["RIGHT", "RIGHT", "UP"])
        self.assertIn("**Initial ground-truth position:** `Office`", content)
        self.assertIn("`RIGHT` → `RIGHT` → `UP`", content)
        self.assertIn("**Number of actions:** $3$", content)
        self.assertIn("| Step | Action | Ground-Truth Position |", content)

        # Do not assume a fixed sampled trajectory: stochastic moves may differ.
        table_lines = [line for line in content.splitlines()
                       if line.startswith("| ") and line.count("|") == 4]
        for record in history:
            expected = (f"| {record['step']} | {record['action']} | "
                        f"{record['true_position']} |")
            self.assertIn(expected, table_lines)
        self.assertEqual(len([line for line in table_lines
                              if line.split("|")[1].strip().isdigit()]), len(history))
        self.assertIn(
            f"| Final ground-truth position | {history[-1]['true_position']} |",
            content,
        )

    def test_report_final_belief(self):
        """Final belief values, normalization and MAP match the simulation."""
        content, history = self.make_report(["RIGHT", "RIGHT", "UP"])
        belief = history[-1]["belief"]
        final_step = history[-1]["step"]
        for room in ROOMS:
            self.assertIn(f"| {room} | ${belief[room]:.4f}$ |", content)
        total = sum(belief[room] for room in ROOMS)
        self.assertAlmostEqual(total, 1.0)
        self.assertIn(f"| Sum of belief probabilities | ${total:.4f}$ |", content)
        self.assertIn(f"= {total:.4f}", content)
        most_likely_room = max(ROOMS, key=belief.get)
        self.assertIn(f"| Most probable predicted position | {most_likely_room} |", content)
        self.assertIn(
            f"| Maximum belief probability | ${belief[most_likely_room]:.4f}$ |",
            content,
        )
        self.assertIn(f"b_{{{final_step}}}(x)", content)


if __name__ == "__main__":
    unittest.main()
