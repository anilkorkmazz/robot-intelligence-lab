"""Run demonstrations of robot motion, belief prediction, and experiment reporting.

This module provides examples of deterministic and stochastic movement,
Markov belief updates, visualization, and integrated experiment exports.
"""

import matplotlib.pyplot as plt

from robot_lab.belief.belief_state import BeliefState
from robot_lab.belief.belief_update import (
    predict_belief,
    predict_belief_with_matrix,
)
from robot_lab.core.robot import Robot
from robot_lab.core.simulation import RobotSimulation
from robot_lab.experiments.csv_export import export_history_to_csv
from robot_lab.experiments.experiment_runner import run_experiment
from robot_lab.experiments.report_generator import generate_experiment_report
from robot_lab.motion.actions import ACTIONS
from robot_lab.motion.motion_model import (
    get_motion_probabilities,
    sample_motion,
)
from robot_lab.motion.movement_rules import get_target_room
from robot_lab.motion.transition_matrix import create_transition_matrix
from robot_lab.visualization.belief_plot import (
    plot_belief_history,
    save_belief_plot,
)
from robot_lab.worlds.house import ROOMS, ROOM_CONNECTIONS


def print_section(title):
    """Print a formatted section heading.

    Args:
        title (str): Heading to display.
    """
    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)


def print_probabilities(probabilities):
    """Print room probabilities and their total.

    Args:
        probabilities (dict[str, float]): Room probability distribution.
    """
    for room, probability in probabilities.items():
        print(f"{room}: {probability:.4f}")

    total = sum(probabilities.values())
    print(f"Total probability: {total:.4f}")


def show_world():
    """Display the rooms, connections, and available movement commands."""
    print_section("1. WORLD MODEL")

    print("\nRooms:")
    for room in ROOMS:
        print("-", room)

    print("\nRoom connections:")
    for room, neighbors in ROOM_CONNECTIONS.items():
        print(room, "->", ", ".join(neighbors))

    print("\nMovement commands:")
    for action in ACTIONS:
        print("-", action)


def show_deterministic_motion():
    """Demonstrate movement with a deterministic destination."""
    print_section("2. DETERMINISTIC MOTION")

    robot = Robot(start_room="Office")
    action = "RIGHT"
    current_room = robot.get_position()

    # Look up the destination without changing the robot's position.
    target = get_target_room(current_room, action)

    print("\nMovement rule test:")
    print("Current room:", current_room)
    print("Action:", action)
    print("Target room:", target)
    print("Actual position:", robot.get_position())

    new_room = robot.move(action)

    print("\nAfter movement:")
    print("New position:", new_room)


def show_probabilistic_motion():
    """Display movement probabilities without sampling a robot position."""
    print_section("3. PROBABILISTIC MOTION MODEL")

    current_room = "Office"
    action = "RIGHT"
    probabilities = get_motion_probabilities(current_room, action)

    print("\nStarting room:", current_room)
    print("Action:", action)
    print("\nPossible movement outcomes:")
    print_probabilities(probabilities)


def show_motion_sampling():
    """Demonstrate independent samples and consecutive stochastic moves."""
    print_section("4. MOTION SAMPLING")

    # Each sample starts from Office rather than the previous outcome.
    print("\n10 independent samples:")
    for i in range(10):
        result = sample_motion("Office", "RIGHT")
        print(f"Trial {i + 1}: {result}")

    print("\nRobot's actual movement:")
    robot = Robot(start_room="Office")
    print("Starting room:", robot.get_position())

    new_position = robot.move_probabilistic("RIGHT")
    print("Action: RIGHT")
    print("Actual position:", new_position)

    # Consecutive moves start from the last sampled position.
    print("\n5 consecutive movements:")
    sequence_robot = Robot(start_room="Office")
    print("Starting room:", sequence_robot.get_position())

    for step in range(5):
        new_room = sequence_robot.move_probabilistic("RIGHT")
        print(f"Step {step + 1}: {new_room}")


def show_belief_prediction():
    """Demonstrate direct Markov belief prediction for two RIGHT actions."""
    print_section("5. BELIEF STATE PREDICTION")

    belief = BeliefState(start_room="Office")
    current_belief = belief.get_probabilities()

    print("\nInitial belief distribution:")
    print_probabilities(current_belief)

    # Prediction propagates all possible outcomes, not a sampled position.
    current_belief = predict_belief(current_belief, "RIGHT")
    print("\nAfter the first RIGHT action:")
    print_probabilities(current_belief)

    current_belief = predict_belief(current_belief, "RIGHT")
    print("\nAfter the second RIGHT action:")
    print_probabilities(current_belief)


def show_transition_matrix():
    """Print the state transition matrix for a RIGHT action."""
    print_section("6. TRANSITION MATRIX")

    action = "RIGHT"
    transition_matrix = create_transition_matrix(action)

    print("\nRIGHT transition matrix:")
    for row in transition_matrix:
        print(row)


def compare_belief_methods():
    """Compare direct and matrix-based belief prediction results."""
    print_section("7. BELIEF UPDATE COMPARISON")

    belief = BeliefState(start_room="Office")
    initial_belief = belief.get_probabilities()
    action = "RIGHT"

    result_1 = predict_belief(initial_belief, action)
    result_2 = predict_belief_with_matrix(initial_belief, action)

    print("\nDirect probability propagation:")
    print_probabilities(result_1)

    print("\nMatrix-based prediction:")
    print_probabilities(result_2)

    # Compare the absolute numerical difference for each room.
    print("\nDifference between methods:")
    for room in ROOMS:
        difference = abs(result_1[room] - result_2[room])
        print(f"{room}: {difference:.10f}")


def show_matrix_prediction():
    """Apply two consecutive Markov predictions using transition matrices."""
    print_section("8. MATRIX BELIEF PREDICTION")

    belief = BeliefState(start_room="Office")
    current_belief = belief.get_probabilities()

    print("\nInitial belief:")
    print_probabilities(current_belief)

    for step in range(2):
        current_belief = predict_belief_with_matrix(current_belief, "RIGHT")
        print(f"\nAfter RIGHT action {step + 1}:")
        print_probabilities(current_belief)


def run_robot_simulation():
    """Demonstrate one stochastic move and its independent belief update."""
    print_section("9. INTEGRATED ROBOT SIMULATION")

    simulation = RobotSimulation(start_room="Office")

    print("\nInitial actual position:")
    print(simulation.robot.get_position())

    print("\nInitial belief:")
    print_probabilities(simulation.current_belief)

    result = simulation.step("RIGHT")

    print("\nMovement result:")
    print("Step:", result["step"])
    print("Action:", result["action"])
    print("Actual position:", result["true_position"])

    print("\nUpdated belief distribution:")
    print_probabilities(result["belief"])


def run_consecutive_robot_simulation():
    """Demonstrate actual positions and belief after two RIGHT moves."""
    print_section("10. CONSECUTIVE ROBOT SIMULATION")

    simulation = RobotSimulation(start_room="Office")

    print("\nInitial position:")
    print(simulation.robot.get_position())

    print("\nInitial belief distribution:")
    print_probabilities(simulation.current_belief)

    # Actual positions are sampled; belief updates consider all outcomes.
    result_1 = simulation.step("RIGHT")
    result_2 = simulation.step("RIGHT")

    print("\nTwo consecutive RIGHT movements:")
    print("Actual position after first movement:", result_1["true_position"])
    print("Actual position after second movement:", result_2["true_position"])

    print("\nBelief after the second movement:")
    print_probabilities(result_2["belief"])
    print("\nTotal steps:", result_2["step"])


def show_movement_history():
    """Display the recorded actual positions and beliefs after each step."""
    print_section("11. ROBOT MOVEMENT HISTORY")

    simulation = RobotSimulation(start_room="Office")
    actions = ["RIGHT", "RIGHT"]

    for action in actions:
        simulation.step(action)

    history = simulation.get_history()

    print("\nRobot movement history:")
    for record in history:
        print("\n------------------------------")
        print("Step:", record["step"])
        print("Action:", record["action"])
        print("Actual position:", record["true_position"])
        print("\nBelief distribution:")
        print_probabilities(record["belief"])

    print("\nTotal movements:", simulation.step_count)
    print("Total records:", len(history))


def show_belief_history_plot():
    """Plot and save belief probabilities across three RIGHT actions."""
    print_section("12. BELIEF HISTORY VISUALIZATION")

    simulation = RobotSimulation(start_room="Office")
    actions = ["RIGHT", "RIGHT", "RIGHT"]

    for action in actions:
        simulation.step(action)

    history = simulation.get_history()
    fig = plot_belief_history(history)

    saved_path = save_belief_plot(
        fig,
        "robot_lab/experiments/results/belief_history.png",
    )
    print("\nPlot saved:", saved_path)

    # Displaying the figure depends on the active Matplotlib backend.
    plt.show()


def show_simulation_history_csv_export():
    """Export a three-action simulation history to CSV."""
    print_section("13. SIMULATION HISTORY CSV EXPORT")

    simulation = RobotSimulation(start_room="Office")
    actions = ["RIGHT", "RIGHT", "UP"]

    for action in actions:
        simulation.step(action)

    history = simulation.get_history()
    csv_path = export_history_to_csv(
        history,
        "robot_lab/experiments/results/simulation_history.csv",
    )

    print("\nCSV file saved:", csv_path)
    print("Total movements:", simulation.step_count)
    print("History record count:", len(history))


def show_automatic_experiment_report():
    """Generate a Markdown report from a separate simulation history."""
    print_section("14. AUTOMATIC EXPERIMENT REPORT")

    simulation = RobotSimulation(start_room="Office")
    actions = ["RIGHT", "RIGHT", "UP"]

    for action in actions:
        simulation.step(action)

    history = simulation.get_history()
    report_path = generate_experiment_report(
        history,
        "robot_lab/experiments/results/experiment_001.md",
    )

    print("\nExperiment report saved:", report_path)
    print("Total movements:", simulation.step_count)
    print("Report record count:", len(history))


def show_integrated_experiment():
    """Generate PNG, CSV, and Markdown outputs from one experiment run."""
    print_section("15. INTEGRATED EXPERIMENT")

    actions = ["RIGHT", "RIGHT", "UP"]
    experiment_result = run_experiment(
        actions,
        "robot_lab/experiments/results/integrated_experiment",
    )

    print("\nExperiment output files:")
    print("PNG:", experiment_result["png_path"])
    print("CSV:", experiment_result["csv_path"])
    print("Report:", experiment_result["report_path"])

    history = experiment_result["history"]
    print("\nTotal history records:", len(history))

    # Ground-truth positions may differ across runs due to sampling.
    print("\nExperiment actual position history:")
    for record in history:
        print(
            "Step", record["step"],
            "-", record["action"],
            "-", record["true_position"],
        )

    final_record = history[-1]
    print("\nFinal belief distribution:")
    print_probabilities(final_record["belief"])


def main():
    """Run all Robot Intelligence Lab demonstrations in sequence."""
    print("Robot Intelligence Lab")
    print("Robot simulation system initialized.")

    show_world()
    show_deterministic_motion()
    show_probabilistic_motion()
    show_motion_sampling()
    show_belief_prediction()
    show_transition_matrix()
    compare_belief_methods()
    show_matrix_prediction()
    run_robot_simulation()
    run_consecutive_robot_simulation()
    show_movement_history()
    show_belief_history_plot()
    show_simulation_history_csv_export()
    show_automatic_experiment_report()
    show_integrated_experiment()


if __name__ == "__main__":
    main()
