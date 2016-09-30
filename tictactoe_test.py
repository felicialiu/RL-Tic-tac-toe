from tictactoe import TictactoeGame
from randomplayer import RandomPlayer
import unittest

# Create new TTT game
game = TictactoeGame()

# Print board to test out
game.printBoard()

# Unit tests for play() method
class TestPlayMethod(unittest.TestCase):

    def test_new_x_marker(self):
        self.assertTrue(game.play(1, 7))
        self.assertEqual(game.getBoard()[7], 1)
        game.reset()

    def test_new_o_marker(self):
        self.assertTrue(game.play(-1, 3))
        self.assertEqual(game.getBoard()[3], -1)
        game.reset()

    def test_doubly_placing_same_marker(self):
        self.assertTrue(game.play(1, 7))
        self.assertFalse(game.play(1, 7))
        game.reset()

    def test_doubly_placing_different_marker(self):
        self.assertTrue(game.play(1, 7))
        self.assertFalse(game.play(-1, 7))
        game.reset()

    def test_out_of_bounds_marker(self):
        self.assertFalse(game.play(1, 10))
        self.assertEqual(game.getBoard(), [0,0,0,0,0,0,0,0,0])
        game.reset()

# Unit tests for checkRow/checkRows
class TestCheckRowMethods(unittest.TestCase):

    def test_marker_first_row_win(self):
        game.play(-1, 0)
        game.play(-1, 1)
        game.play(-1, 2)
        self.assertTrue(game.checkRow(game.getBoard()[0:3])[0])
        self.assertFalse(game.checkRow(game.getBoard()[3:6])[0])
        self.assertFalse(game.checkRow(game.getBoard()[6:9])[0])
        game.reset()

    def test_marker_second_row_win(self):
        game.play(-1, 3)
        game.play(-1, 4)
        game.play(-1, 5)
        self.assertFalse(game.checkRow(game.getBoard()[0:3])[0])
        self.assertTrue(game.checkRow(game.getBoard()[3:6])[0])
        self.assertFalse(game.checkRow(game.getBoard()[6:9])[0])
        game.reset()

    def test_marker_third_row_win(self):
        game.play(-1, 6)
        game.play(-1, 7)
        game.play(-1, 8)
        self.assertFalse(game.checkRow(game.getBoard()[0:3])[0])
        self.assertFalse(game.checkRow(game.getBoard()[3:6])[0])
        self.assertTrue(game.checkRow(game.getBoard()[6:9])[0])
        game.reset()

    def test_detect_row_o_winner(self):
        game.play(-1, 0)
        game.play(-1, 1)
        game.play(-1, 2)
        self.assertTrue(game.checkRows()[0])
        self.assertEqual(game.checkRows()[1], -1)
        game.reset()

# Unit tests for checkColumn
class TestCheckColumnMethod(unittest.TestCase):

    def test_marker_first_column_win(self):
        game.play(1, 0)
        game.play(1, 3)
        game.play(1, 6)
        self.assertTrue(game.checkColumn(0)[0])
        self.assertFalse(game.checkColumn(1)[0])
        self.assertFalse(game.checkColumn(2)[0])
        self.assertEqual(game.checkColumn(0)[1], 1)
        game.reset()

    def test_marker_second_column_win(self):
        game.play(1, 1)
        game.play(1, 4)
        game.play(1, 7)
        self.assertFalse(game.checkColumn(0)[0])
        self.assertTrue(game.checkColumn(1)[0])
        self.assertFalse(game.checkColumn(2)[0])
        self.assertEqual(game.checkColumn(1)[1], 1)
        game.reset()

    def test_marker_third_column_win(self):
        game.play(1, 2)
        game.play(1, 5)
        game.play(1, 8)
        self.assertFalse(game.checkColumn(0)[0])
        self.assertFalse(game.checkColumn(1)[0])
        self.assertTrue(game.checkColumn(2)[0])
        self.assertEqual(game.checkColumn(2)[1], 1)
        game.reset()

# Unit tests for checkDiagonals
class TestCheckDiagonalsMethod(unittest.TestCase):

    def test_marker_first_diagonal_win(self):
        game.play(1, 0)
        game.play(1, 4)
        game.play(1, 8)
        self.assertTrue(game.checkDiagonals())
        game.reset()

    def test_marker_second_diagonal_win(self):
        game.play(1, 2)
        game.play(1, 4)
        game.play(1, 6)
        self.assertTrue(game.checkDiagonals())
        game.reset()

    def test_marker_no_diagonal(self):
        self.assertFalse(game.checkDiagonals()[0])
        game.reset()

# Unit tests for hasWinner
class TestHasWinnerMethod(unittest.TestCase):

    def test_no_winner_result(self):
        subboard = [0, 0, 0]
        self.assertFalse(game.hasWinner(subboard)[0])
        self.assertEqual(game.hasWinner(subboard)[1], 0)

    def test_x_marker_winner(self):
        subboard = [1, 1, 1]
        self.assertTrue(game.hasWinner(subboard)[0])
        self.assertEqual(game.hasWinner(subboard)[1], 1)

    def test_o_marker_winner(self):
        subboard = [-1, -1, -1]
        self.assertTrue(game.hasWinner(subboard)[0])
        self.assertEqual(game.hasWinner(subboard)[1], -1)

    def test_filled_but_no_winner(self):
        subboard = [-1, 1, 1]
        self.assertFalse(game.hasWinner(subboard)[0])
        self.assertEqual(game.hasWinner(subboard)[1], 0)

    def test_not_filled_no_winner(self):
        subboard = [0, 1, -1]
        self.assertFalse(game.hasWinner(subboard)[0])
        self.assertEqual(game.hasWinner(subboard)[1], 0)

# Unit tests for checkWinner
class TestCheckWinner(unittest.TestCase):

    def test_draw_result(self):
        """
        x o o
        o x x
        x x o
        """
        game.play(1, 0)
        game.play(-1, 1)
        game.play(-1, 2)
        game.play(-1, 3)
        game.play(1, 4)
        game.play(1, 5)
        game.play(1, 6)
        game.play(1, 7)
        game.play(-1, 8)
        self.assertTrue(game.checkWinner()[0])
        self.assertEqual(game.checkWinner()[1], 0)
        game.reset()


    def test_win_result(self):
        """
        x o o
        x x x
        o x o
        """
        game.play(1, 0)
        game.play(-1, 1)
        game.play(-1, 2)
        game.play(1, 3)
        game.play(1, 4)
        game.play(1, 5)
        game.play(-1, 6)
        game.play(1, 7)
        game.play(-1, 8)
        self.assertTrue(game.checkWinner()[0])
        self.assertEqual(game.checkWinner()[1], 1)
        game.reset()

    def test_not_finished_rowofzeros_result(self):
        """
        - - -
        x x o
        x o o
        """
        game.play(1, 3)
        game.play(1, 4)
        game.play(-1, 5)
        game.play(1, 6)
        game.play(1, 7)
        game.play(-1, 8)
        self.assertFalse(game.checkWinner()[0])
        self.assertEqual(game.checkWinner()[1], 0)
        game.reset()

if __name__ == '__main__':
    unittest.main()