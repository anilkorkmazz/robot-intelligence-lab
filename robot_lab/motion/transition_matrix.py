
"""
Construct state transition matrices for stochastic robot motion.

Each matrix represents the probabilities of transitioning
between rooms after executing a specific movement command.
"""

from robot_lab.worlds.house import ROOMS
from robot_lab.motion.motion_model import get_motion_probabilities


def create_transition_matrix(action):
    """
    Construct the state transition matrix for a movement action.

    Each matrix element T[i][j] represents the probability
    of transitioning from room i to room j:

        T[i][j] = P(X_next = j | X_current = i, action)

    Rows represent current rooms, while columns represent
    possible destination rooms. Both follow the order in ROOMS.

    Args:
        action (str): Movement command associated with the matrix.

    Returns:
        list[list[float]]: Row-stochastic transition matrix
            with dimensions N x N, where N is the number of rooms.
    """

    matrix = []

    # Construct one transition matrix row for each starting room.
    for current_room in ROOMS:

        # Retrieve possible movement outcomes and their probabilities.
        motion_probabilities = get_motion_probabilities(
            current_room, action
        )

        row = []

        # Include every destination, assigning zero to impossible transitions.
        for target_room in ROOMS:

            probability = motion_probabilities.get(target_room, 0.0)

            row.append(probability)

        matrix.append(row)

    return matrix
