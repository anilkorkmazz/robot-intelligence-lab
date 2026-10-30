
"""
Belief State Representation
===========================

This module initializes the robot's belief distribution
over a discrete set of rooms.

A belief state represents the robot's uncertainty about
its location using a probability distribution.

Initially, the robot's starting position is assumed
to be known with certainty.

Therefore:

    P(X_0 = start_room) = 1.0
    P(X_0 = other_room) = 0.0

The sum of all probabilities must equal 1.0.

Motion-based belief prediction is implemented separately
in the belief_update module.
"""

from robot_lab.worlds.house import ROOMS


class BeliefState:
    """
    Represent the robot's initial belief distribution.

    The belief state is stored as a dictionary that maps
    each room to its corresponding probability.

    Example:
        If the robot starts in "Office":

        {
            "Living Room": 0.0,
            "Kitchen": 0.0,
            "Office": 1.0,
            "Hallway": 0.0,
            "Dining Room": 0.0
        }

    This distribution represents complete certainty
    about the robot's initial location.
    """

    def __init__(self, start_room="Office"):
        """
        Initialize the robot's belief distribution.

        Assign probability 1.0 to the starting room
        and probability 0.0 to every other room.

        Args:
            start_room (str):
                Name of the robot's initial room.
                Defaults to "Office".

        Raises:
            ValueError:
                If the specified starting room does
                not exist in the environment.
        """

        # Validate that the starting room exists
        # in the predefined environment.
        #
        # An invalid room would produce a belief
        # distribution without a valid initial state.
        if start_room not in ROOMS:
            raise ValueError("Invalid starting room!")

        # Initialize the dictionary that stores
        # the probability assigned to each room.
        self.probabilities = {}

        # Iterate through every room in the environment.
        for room in ROOMS:

            # The robot is assumed to be located
            # in the starting room with certainty.
            if room == start_room:
                self.probabilities[room] = 1.0

            # All other rooms have zero probability
            # at the initial time step.
            else:
                self.probabilities[room] = 0.0

    def get_probabilities(self):
        """
        Return a copy of the current belief distribution.

        Returning a copy prevents external modifications
        from directly affecting the internal dictionary.

        Returns:
            dict[str, float]:
                A dictionary mapping room names
                to their belief probabilities.

        Example:
            belief = BeliefState(start_room="Office")

            probabilities = belief.get_probabilities()

            print(probabilities["Office"])
            # Output: 1.0
        """

        # Return a copy to preserve the internal
        # probability dictionary from external changes.
        return self.probabilities.copy()
