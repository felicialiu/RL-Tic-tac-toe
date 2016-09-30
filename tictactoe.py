class TictactoeGame(object):
    """Class representation of a Tic-tac-toe game.

    Represents the Tic-tac-toe game as an array of 9 values. The following
    diagram shows the corresponding index in the array for each location:

    0 1 2
    3 4 5
    6 7 8

    Class methods include play(...) for putting X and O markers on the board,
    methods that check whether the game is finished and/or won, printing 
    options, helper methods, and getters and setters.


    Attributes:
        board (list): Flat array representation of the game's board state

    """
    def __init__(self):
        self.board = [0,0,0,0,0,0,0,0,0]

    def play(self, marker, location):
        """Allows placement of markers on the board on free spaces.

        Note:
            Catches IndexErrors

        Args:
            marker (int): Marker, 1 or -1. Conventionally 1 is used for the 
            (learning) agent and -1 for the opponent.
            location (int): An index of a position in the board.

        Returns:
            True if successful, False otherwise.

        """
        try:
            if marker == 1:
                if self.board[location] == 0:
                    self.board[location] = 1
                    return True
                else:
                    print("There is already a marker in this position.")
                    return False
            elif marker == -1:
                if self.board[location] == 0:
                    self.board[location] = -1
                    return True
                else:
                    print("There is already a marker in this position.")
                    return False
        except IndexError:
            print("Illegal marker location.")
        return False

    def isFinished(self):
        """Returns whether the board still has empty spaces.

        Returns:
            True if the board is full, False otherwise.
       
        """
        if 0 in self.board:
            return False
        return True

    def checkWinner(self):
        """Inspects the board and reports whether game has been won, by whom,
        or whether there is a draw.

        Returns:
            Two values: True if the game has been won, False otherwise, and 1   
            denoting agent has won, -1 if opponent has won, and 0 if either
            there is a draw, or the game is not finished yet.

        """
        # Rows from top to down
        for i in range(0,8,3):
            win, winner = self.checkRow(self.board[i:i+3])
            if win:
                return win, winner
        
        # Columns from left to right
        for i in range(3):
            win, winner = self.checkColumn(i)
            if win:
                return win, winner

        # Two diagonals (0, 4, 8; 2, 4, 6)
        win, winner = self.checkDiagonals()
        # If won by one of the two players return here True, and the marker
        # of the winner
        if win:
            return win, winner
        # No one won, check if board is full/there is a draw
        elif self.isFinished():
            return True, 0
        # No winner
        return False, 0


    # Checks three rows for a winner
    def checkRows(self):
        """Checks all three rows for a winner.

        Returns:
            True if there is a winner, otherwise False
            1, -1 depending on winner, 0 if none.
        
        """
        for i in range(0,8,3):
            win, winner = self.checkRow(self.board[i:i+3])
            if win:
                return win, winner
        return False, 0

    def checkRow(self, row):
        """Given a row (list), checks if there is a winner.

        Returns:
            True if there is a winner, otherwise False
            1, -1 depending on winner, 0 if none.  

        """  
        return self.hasWinner(row)

    # Given a column number (col), extracts the column and determines 
    # whether this columns has been won by X or O
    #@staticmethod 
    def checkColumn(self, col):
        """Given a column (list), checks if there is a winner.

        Returns:
            True if there is a winner, otherwise False
            1, -1 depending on winner, 0 if none.

        """
        column = []
        # Extract the column from the board
        for index, item in enumerate(self.board):
            if (index - col) % 3 == 0:
                column.append(item)
        return self.hasWinner(column)

    @staticmethod
    def hasWinner(subboard):
        """Given a subboard (a list of 3) of the 9-space board, determines
        a winner/draw and which player won.

        Args:
            subboard (list): list of length 3 that represents a row, column
            or diagonal.

        Returns:
            True if there is a winner, otherwise False
            1, -1 depending on winner, 0 if none.

        """
        win = False
        winner = 0
        if 0 not in subboard:
            if subboard.count(subboard[0]) == len(subboard):
                win = True
                if 1 in subboard:
                    winner = 1
                elif -1 in subboard:
                    winner = -1
        return win, winner

    def checkDiagonals(self):
        """Checks if there is a winner in either of both diagonals.

        Returns:
            True if there is a winner, otherwise False
            1, -1 depending on winner, 0 if none.

        """
        diag1, diag2 = [], []
        
        # Top left to bottom right diagonal
        for i in range(0,9,4):
            diag1.append(self.board[i])

        # Top right to bottom left diagonal
        for i in range(2,8,2):
            diag2.append(self.board[i])

        win1 = self.hasWinner(diag1)
        win2 = self.hasWinner(diag2)
        if win1[0]:
            return win1
        elif win2[0]:
            return win2
        else:
            return False, 0

    @staticmethod
    def printNum(item):
        """Prints empty space as - and the markers 1 and -1 as X and O.

        Args:
            item (str): A number (1, -1, 0) representing the placement of a
            marker.

        Returns:
            The string 'X' for 1, 'O' for -1, and '-' for no marker.

        """
        if item == 1:
            return 'X'
        elif item == -1:
            return 'O'
        elif item == 0:
            return '-'

    def printSimple(self):
        """Prints the board as a simple list."""
        print self.board

    def printBoard(self):
        """Prints the board in tic-tac-toe layout."""

        for index, item in enumerate(self.board):
            if (index % 3) == 0:
                print "|-",
                print self.printNum(item),
                print "-|",
            elif ((index - 1) % 3) == 0:
                print "-",
                print self.printNum(item),
                print "-",
            elif ((index - 2) % 3) == 0:
                print "|-",
                print self.printNum(item),
                print "-|"
        print "\n"
  
    def validate(self, location):
        """Validates whether a location is free or occupied. Used for
        human versus computer play.

        """
        if self.board[location] == 0:
            return True
        else:
            return False

    def getBoard(self):
        """Returns the board representation."""
        return self.board

    def reset(self):
        """Resets the board to starting state."""
        self.board = [0,0,0,0,0,0,0,0,0]

    def state2key(self):
        """Returns a inmutable representation of the board."""
        return tuple(self.board)
