
"""
Robot state management with deterministic and stochastic motion.

This module defines a robot that operates in a discrete
environment and updates its position using either deterministic
movement rules or a probabilistic motion model.
"""

from robot_lab.worlds.house import ROOMS
from robot_lab.motion.movement_rules import get_target_room
from robot_lab.motion.motion_model import sample_motion


class Robot:
    """
    Represent a robot moving between connected rooms.

    The robot maintains its actual position and supports
    both deterministic and probabilistic movement.
    """

    def __init__(self, start_room="Office"):
        """
        Initialize the robot at a specified starting room.

        Args:
            start_room (str):
                Initial room of the robot. Defaults to "Office".

        Raises:
            ValueError:
                If the starting room is not defined in ROOMS.
        """
        if start_room not in ROOMS:
            raise ValueError("Invalid starting room!")

        self.current_room = start_room

    def get_position(self):
        """
        Return the robot's current position.

        Returns:
            str: Name of the room currently occupied.
        """
        return self.current_room

    def move(self, action):
        """
        Execute a deterministic movement command.

        The next position is determined by the environment's
        movement rules without introducing randomness.

        Args:
            action (str):
                Movement command to execute.

        Returns:
            str: Robot's updated position.
        """
        current_room = self.current_room

        # Determine the destination using the environment rules.
        target_room = get_target_room(current_room, action)

        self.current_room = target_room

        return self.current_room

    def move_probabilistic(self, action):
        """
        Execute a movement command using the stochastic motion model.

        The resulting position is sampled from the probability
        distribution associated with the current room and action.

        Args:
            action (str):
                Movement command to execute.

        Returns:
            str: Robot's sampled position after the action.
        """
        current_room = self.current_room

        # Sample a possible outcome instead of assuming success.
        selected_room = sample_motion(current_room, action)

        # Update the robot's actual position with the sampled result.
        self.current_room = selected_room

        return self.current_room
