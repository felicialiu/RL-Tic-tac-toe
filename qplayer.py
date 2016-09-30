from player import Player
from collections import defaultdict
import operator
from itertools import groupby
import random
from copy import deepcopy

class QPlayer(Player):
    """Class representation of an agent which learns through
    Q-learning.

    Main two methods include selecting an action and updating Q-values.

    Attributes:
        QTable (defautldict): Look-up table of Q-values. Key are states, where
        values are another dictionary, mapping actions to Q-values.

    """
    def __init__(self):
        super(QPlayer, self).__init__()
        self.QTable = defaultdict(dict)

    # Given the state of the agent (as board), creates a list of possible
    # moves (spaces with no marker) and their values and chooses the best
    # action based on its value
    def chooseAction(self, rawboard, epsilon = 0):
        """Chooses an action based on board state.

        Note:
            If epsilon is given and unequal to zero, agent acts according to
            epsilon-greedy. With a probability of epsilon it will choose
            a random action as to encourage exploration versus exploitation.

        Args:
            rawboard (list): Representation of Tictactoe board state.
            epsilon (float): A value for epsilon-greedy

        Returns:
            Integer representing the chosen action.

        """
        # Make an epsilon-greedy move
        if random.randrange(0,2) < epsilon:
            return self.chooseRandomAction(rawboard)
        # We need to select the best action from a list of possible open spaces
        else:
            stateKey = tuple(rawboard)
            # Get a list of possible actions (open spaces in the board)
            possibleActions = []
            for index, item in enumerate(rawboard):
                if item == 0:
                    possibleActions.append(index)
            # Map the list possible actions to their values
            actionValues = {}
            for action, actionValue in self.QTable[stateKey].iteritems():
                if action in possibleActions:
                    actionValues[action] = actionValue
            # Select the actions with the highest value
            bestActions = next([g[0] for g in group]
                                        for key, group in groupby(
                                            sorted(actionValues.items(),
                                                   key=operator.itemgetter(1), 
                                                   reverse=True),
                                            operator.itemgetter(1)))
            # Return a random choice between them if there are more than one
            return random.choice(bestActions)

    def chooseRandomAction(self, rawboard):
        """Chooses randomly from avialable slots.

        Args:
            rawboard (list): Board representation

        Returns:
            An integer representing a slot in the Tictactoe board.

        """
        possibleActions = []
        for index, item in enumerate(rawboard):
            if item == 0:
                possibleActions.append(index)
        return random.choice(possibleActions)

    def updateQvalues(self, stateKey, action, nextStateKey, reward, 
                      gameover, alpha, gamma):
        """Updates the Q-values according to the Q-learning algorithm.

        Q-value of (stateKey, action) gets updated with the following rule

        Q(s_t, a_t) = Q(s_t, a_t) 
                    + alpha * [reward + gamma * max_a Q(s_t+1,a)] - Q(s_t, a_t)

        Args:
            stateKey (tuple): Representation of state(t)
            action (int): Action taken by the agent
            nextStateKey (tuple): Board after next player plays a move
            reward (int): 1, 0, or -1 depending on outcome
            gameover (bool): If the game has already been won
            alpha (float): learning rate
            gamma (float): discount factor

        """
        expected = 0
        if gameover:
            expected = reward
        else:
            highestQValue = self.highestQValue(nextStateKey)
            expected = reward + (gamma * highestQValue)
        change = alpha * (expected - self.QTable[stateKey][action])
        self.QTable[stateKey][action] += change

    def highestQValue(self, stateKey):
        """Returns highest Q-value

        Args:
            stateKey (tuple): Representation of state(t)

        Returns:
            Q-value for best action in state(t)

        """

        bestAction = max(self.QTable[stateKey].iteritems(), key=operator.itemgetter(1))[0]
        return self.QTable[stateKey][bestAction]

    def addState(self, state, actionDict):
        """Adds a state to the look-up table with given action-value dict.

        Args:
            state (tuple): Representation of a state
            actionDict (dict): Action-value dictionary

        """
        self.QTable[state] = actionDict

    def getQTable(self):
        """Returns QTable

        """
        return self.QTable

    def prettyprintTable(self):
        """Prints the QTable in a slightly better format.

        """
        for state, actionValues in self.QTable.iteritems():
            print "State ", state
            print "Action value pairs", actionValues

    def reverseTableStates(self):
        """Reverses the states to reflect an opposing player' state.

        Normally, a state such as

        X X -
        O - O
        - - -

        is represented with (1, 1, 0, -1, 0, -1, 0, 0, 0) from the eye of
        the main agent. The best action-value pair reflects the best action to
        take in order to make 1 win, which is 3.

        When loading a pre-trained QTable for an opposing player, we swap the
        board states so the best action-value pair is in favour of -1.

        """
        tableCopy = deepcopy(self.QTable)
        self.QTable = defaultdict(dict)#lambda:{0:0.0, 1:0.0, 2:0.0, 3:0.0, 4:0.0, 5:0.0, 6:0.0, 7:0.0, 8:0.0})
        for state, actionValues in tableCopy.iteritems():
            flipped = self.reverseState(list(state))
            self.QTable[flipped] = actionValues

    def reverseState(self, stateList):
        """Returns the opposite of a tuple state.

        """
        flipped = []
        for item in stateList:
            item = item * -1
            flipped.append(item)
        return tuple(flipped)

    def createRandomDict(self):
        """Returns an action-value dictionary with numbers initialised between
        -0.15 and 0.15.

        """
        actionValues = {}
        for i in range(9):
            actionValues[i] = random.uniform(-0.15, 0.15)
        return actionValues


