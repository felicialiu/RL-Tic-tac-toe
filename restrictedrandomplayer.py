from player import Player
import random

class RestrictedRandomPlayer(Player):
    """Class for an agent who plays randomly by choosing from the free spaces.

    Note:
        Restricted means it will only choose from available spaces, so it 
        will not return an already occupied slot.

    """

    def __init__(self):
        super(RestrictedRandomPlayer, self).__init__()

    def chooseAction(self, rawboard, epsilon = None):
        """Chooses randomly from avialable slots.

        Args:
            rawboard (list): Board representation
            epsilon (float): Not used

        Returns:
            An integer representing a slot in the Tictactoe board.

        """
        possibleActions = []
        for index, item in enumerate(rawboard):
            if item == 0:
                possibleActions.append(index)
        return random.choice(possibleActions)
