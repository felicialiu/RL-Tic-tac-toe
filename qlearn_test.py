from tictactoe import TictactoeGame
from qplayer import QPlayer
import unittest
import random
from collections import defaultdict
from itertools import groupby
import operator

# Create new TTT game
game = TictactoeGame()
agent = QPlayer()

# Unit tests for method snippets
class TestChooseActionSnippets(unittest.TestCase):

    def test_epsilon_generation(self):
        epsilon = 1
        result1 = (random.randrange(0,2) -0.1)< epsilon
        result2 = random.randrange(0,2) < 0
        self.assertTrue(result1)
        self.assertFalse(result2)

    def test_possible_actions(self):
        game.play(1, 0)
        game.play(-1, 1)
        possibleActions = []
        for index, item in enumerate(game.getBoard()):
            if item == 0:
                possibleActions.append(index)
        self.assertEqual(possibleActions, [2, 3, 4, 5, 6, 7, 8])
        game.reset()

    def test_best_actions(self):
        example_dict = {0:1.0, 1: 0.5, 2:1.0}
        bestActions = next([g[0] for g in group]
                        for key, group in groupby(
                            sorted(example_dict.items(),
                            key=operator.itemgetter(1), 
                            reverse=True), operator.itemgetter(1)))
        self.assertEqual(bestActions, [0, 2])
        game.reset()

    def test_reverse_states(self):
        def reverseState(stateList):
            """Returns the opposite of a tuple state.

            """
            flipped = []
            for item in stateList:
                item = item * -1
                flipped.append(item)
            return tuple(flipped)

        old = {(1,1,1,-1,-1,-1,0,0,0):{0:0.1, 1:0.2, 2:0.0, 3:-0.1, 4:0.0, 5:0.0, 6:0.0, 7:0.0, 8:0.0}}
        table = defaultdict(dict)#lambda:{0:0.0, 1:0.0, 2:0.0, 3:0.0, 4:0.0, 5:0.0, 6:0.0, 7:0.0, 8:0.0})
        for state, actionValues in old.iteritems():
            flipped = reverseState(list(state))
            self.assertEqual(flipped, (-1,-1,-1,1,1,1,0,0,0))
            table[flipped] = actionValues
        self.assertEqual(table, {(-1,-1,-1,1,1,1,0,0,0):{0:0.1, 1:0.2, 2:0.0, 3:-0.1, 4:0.0, 5:0.0, 6:0.0, 7:0.0, 8:0.0}})





if __name__ == '__main__':
    unittest.main()