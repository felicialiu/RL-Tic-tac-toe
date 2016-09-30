from tictactoe import TictactoeGame
import pickle
import dill
from qplayer import QPlayer
import argparse
from restrictedrandomplayer import RestrictedRandomPlayer

parser = argparse.ArgumentParser()

parser.add_argument('-opp', '--opponentType', type=int, default = 0, help ="0 for RestrictedRandomPlayer, 1 from loaded QPlayer")
parser.add_argument('-savefile', '--opponent_savefile', default='qtable.pkl')

args = parser.parse_args()

print("Welcome to Tic-Tac-Toe: human versus computer.")

# Create game
game = TictactoeGame()

# First player
humanFirst = True

# Settings
user = 1
computer = -1
computer_player = RestrictedRandomPlayer()
if args.opponentType == 1:
    computer_player = pickle.load(open(args.opponent_savefile, "rb"))
    computer_player.reverseTableStates()

toContinue = 'y'

while (toContinue == 'y'):
    game.printBoard()
    
    # Opponent plays if it's the first mover. Opponent's mark is -1
    if not humanFirst:
        computerAction = computer_player.chooseAction(game.getBoard(), 0)
        game.play(-1, computerAction)
        game.printBoard()

    # Loop for a single game
    while (not game.checkWinner()[0]):
        # Instantiate
        user_action = -1
        validated = False

        # If user picks an occupied slot, give chance to choose again
        while not validated:
            user_action = int(raw_input("Place your X marker. "))
            validated = game.validate(user_action)
        
        # Perform action picked by user
        game.play(user, user_action)
        game.printBoard()
        
        if game.checkWinner()[0]:
            break

        # Choose and perform action picked by computer
        computer_action = -1
        validated = False
        while not validated:
            computer_action = computer_player.chooseAction(game.getBoard(), epsilon=0)
            validated = game.validate(computer_action)
        game.play(computer, computer_action)
        game.printBoard()

    print "Game over!"
    game.printBoard()
    toContinue = raw_input("Want to continue? y/n: ")
    game.reset()
    humanFirst = not humanFirst
