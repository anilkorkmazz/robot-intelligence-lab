
"""
Stochastic motion model for a robot in a discrete environment.

This module calculates movement probabilities and samples
the robot's next position based on the commanded action.
"""

import random

from robot_lab.motion.movement_rules import get_target_room


MOVE_SUCCESS_PROBABILITY = 0.8
STAY_PROBABILITY = 0.2


def get_motion_probabilities(current_room, action):
    """
    Calculate the possible outcomes of a movement command.

    For a valid transition, the robot moves to the target room
    with probability 0.8 or remains in place with probability 0.2.

    If the movement is blocked, the robot remains in its
    current room with probability 1.0.

    Args:
        current_room (str): Robot's current location.
        action (str): Movement command to execute.

    Returns:
        dict[str, float]: Possible destination rooms and
            their corresponding transition probabilities.
    """

    # Determine the destination defined by the movement rules.
    target_room = get_target_room(current_room, action)

    probabilities = {}

    if target_room == current_room:

        # A blocked movement results in staying with certainty.
        probabilities[current_room] = 1.0

    else:

        # Distribute probability between moving and staying.
        probabilities[target_room] = MOVE_SUCCESS_PROBABILITY
        probabilities[current_room] = STAY_PROBABILITY

    return probabilities


def sample_motion(current_room, action):
    """
    Sample the robot's next position from the motion model.

    Uses weighted random sampling to select one destination
    according to the probabilities of possible outcomes.

    Args:
        current_room (str): Robot's current location.
        action (str): Movement command to execute.

    Returns:
        str: Sampled room representing the robot's next position.
    """

    probabilities = get_motion_probabilities(current_room, action)

    possible_rooms = list(probabilities.keys())
    room_probabilities = list(probabilities.values())

    # Select one destination using its transition probability as weight.
    selected_room = random.choices(
        possible_rooms,
        weights=room_probabilities,
        k=1,
    )[0]

    return selected_room
