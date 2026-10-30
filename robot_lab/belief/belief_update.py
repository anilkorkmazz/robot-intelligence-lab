
"""
Markov belief prediction using direct probability propagation
and state transition matrices.

Both methods predict the robot's next belief distribution
without accessing its actual position.
"""

from robot_lab.worlds.house import ROOMS
from robot_lab.motion.motion_model import get_motion_probabilities
from robot_lab.motion.transition_matrix import create_transition_matrix


def predict_belief(current_belief, action):
    """
    Predict the next belief distribution using the motion model.

    Implements the Markov prediction equation:

        b_next(x') = sum_x P(x' | x, action) * b(x)

    Args:
        current_belief (dict[str, float]):
            Current probability distribution over rooms.
        action (str):
            Movement command to execute.

    Returns:
        dict[str, float]:
            Predicted probability distribution after the action.
    """

    # Initialize the predicted belief for all rooms.
    new_belief = {}

    for room in ROOMS:
        new_belief[room] = 0.0

    # Propagate probability mass from each possible current room.
    for current_room in ROOMS:

        current_probability = current_belief[current_room]

        # Retrieve possible transitions for the given action.
        motion_probabilities = get_motion_probabilities(
            current_room, action
        )

        for target_room, transition_probability in motion_probabilities.items():

            # Apply the law of total probability.
            contribution = current_probability * transition_probability

            new_belief[target_room] += contribution

    return new_belief


def predict_belief_with_matrix(current_belief, action):
    """
    Predict the next belief distribution using a transition matrix.

    Implements row-vector matrix multiplication:

        b_next = b * T_action

    Args:
        current_belief (dict[str, float]):
            Current probability distribution over rooms.
        action (str):
            Movement command associated with the transition matrix.

    Returns:
        dict[str, float]:
            Predicted probability distribution after the action.
    """

    # Construct the transition matrix for the selected action.
    transition_matrix = create_transition_matrix(action)

    new_belief = {}

    # Compute each target room's probability.
    for target_index, target_room in enumerate(ROOMS):

        total_probability = 0.0

        # Sum contributions from all possible current rooms.
        for current_index, current_room in enumerate(ROOMS):

            current_probability = current_belief[current_room]

            transition_probability = transition_matrix[
                current_index
            ][target_index]

            contribution = (
                current_probability * transition_probability
            )

            total_probability += contribution

        new_belief[target_room] = total_probability

    return new_belief
