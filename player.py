from collections import defaultdict

class Player(object):
    """Class interface for a player.

    Every player needs to implement a chooseAction() method for determining
    an action. This method gets overloaded in child classes.

    """

    def __init__(self):
        pass

    def chooseAction(self):
        raise NotImplementedError()
