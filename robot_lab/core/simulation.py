
"""
Robot simulation with stochastic motion and Markov belief prediction.

This module coordinates the robot's actual movement, predicted
belief distribution, and simulation history while keeping
ground-truth positions separate from probabilistic estimates.
"""

from robot_lab.core.robot import Robot
from robot_lab.belief.belief_state import BeliefState
from robot_lab.belief.belief_update import predict_belief
from robot_lab.motion.actions import ACTIONS


class RobotSimulation:
    """
    Manage robot movement, belief prediction, and simulation history.

    The robot's ground-truth position is sampled from the stochastic
    motion model, while its belief is updated independently using
    Markov prediction.
    """

    def __init__(self, start_room="Office"):
        """
        Initialize the robot simulation and record its initial state.

        Args:
            start_room (str): Initial robot location. Defaults to "Office".

        Raises:
            ValueError: If the starting room is invalid.
        """

        # Initialize the actual robot position and its initial belief.
        self.robot = Robot(start_room=start_room)

        belief = BeliefState(start_room=start_room)
        self.current_belief = belief.get_probabilities()

        self.step_count = 0
        self.history = []

        # Record the initial state before any movement occurs.
        initial_record = {
            "step": 0,
            "action": "START",
            "true_position": self.robot.get_position(),
            "belief": self.current_belief.copy()
        }

        self.history.append(initial_record)

    def step(self, action):
        """
        Execute one stochastic movement and update the belief state.

        The actual position is sampled from the motion model,
        whereas the belief prediction considers all possible
        transitions without accessing the sampled position.

        Args:
            action (str): Movement command to execute.

        Returns:
            dict: Simulation record containing the step number,
                action, ground-truth position, and belief distribution.

        Raises:
            ValueError: If the movement command is invalid.
        """

        # Validate the action before modifying the simulation state.
        if action not in ACTIONS:
            raise ValueError(
                f"Invalid movement command: {action}"
            )

        # Sample the robot's actual position from the motion model.
        new_position = self.robot.move_probabilistic(
            action
        )

        # Predict the next belief without using the sampled position.
        self.current_belief = predict_belief(
            self.current_belief,
            action
        )

        # Advance the time step even if the robot remains in place.
        self.step_count += 1

        # Store a snapshot of the state after the movement.
        record = {
            "step": self.step_count,
            "action": action,
            "true_position": new_position,
            "belief": self.current_belief.copy()
        }

        self.history.append(record)

        return record

    def get_history(self):
        """
        Return independent copies of all simulation records.

        Each record includes a separate copy of its belief
        distribution to prevent external modifications
        from affecting the stored simulation history.

        Returns:
            list[dict]: Simulation records containing the initial
                state and all subsequent movement results.
        """

        history_copy = []

        for record in self.history:

            # Copy both the record and its nested belief dictionary.
            copied_record = record.copy()
            copied_record["belief"] = (
                record["belief"].copy()
            )

            history_copy.append(copied_record)

        return history_copy
