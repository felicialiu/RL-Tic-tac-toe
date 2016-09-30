from tictactoe import TictactoeGame
from qplayer import QPlayer
from restrictedrandomplayer import RestrictedRandomPlayer
from sarsaplayer import SarsaPlayer
import argparse
import sys
import random
import pickle
import time
from datetime import timedelta
import dill
parser = argparse.ArgumentParser()
# Parameters
parser.add_argument('-max', '--maxNumberGames', type=int, default=100000)
parser.add_argument('-lr', '--alpha', type=float, default = 0.1)
parser.add_argument('-g', '--gamma', type=float, default = 0.9)
parser.add_argument('-e', '--epsilon', type=float, default = 0.9)

# Agent and opponent settings
parser.add_argument('-agent', '--agentType', type=int, default = 1, help = "1 for SARSA, 2 from loaded SARSA")
parser.add_argument('-opp', '--opponentType', type=int, default = 0, help ="0 for RestrictedRandomPlayer, 1 from loaded SARSA")
parser.add_argument('-save1', '--agent_savefile', default='qtable.pkl')
parser.add_argument('-save2', '--opponent_savefile', default='qtable.pkl')

# Save file names
parser.add_argument('-agent_file', '--agent_filename', default="agent.pkl")
parser.add_argument('-reward', '--rewardsperep', default="rewardep.pkl")
parser.add_argument('-q_file', '--qtable_filename', default="qtable.pkl")

args = parser.parse_args()

# Maximum number of games
maxGames = args.maxNumberGames

# Current game
games = 0

# Game statistics
wins = 0
losses = 0
draw = 0
reward_per_episode = []

# Initialise board
game = TictactoeGame()

eps_start = args.epsilon
eps = eps_start
alpha = args.alpha
gamma = args.gamma

# Initialising agent, opponent
agent = SarsaPlayer()#pickle.load(open("reversebug/agent1.pkl", "rb"))#QPlayer()#pickle.load(open("debugging/agent1.pkl", "rb"))#QPlayer()#pickle.load(open("debugging/agent1.pkl", "rb"))
opponent = RestrictedRandomPlayer()#pickle.load(open("reversebug/agent1.pkl", "rb"))#RestrictedRandomPlayer()#pickle.load(open("debugging/agent1.pkl", "rb"))#QPlayer(opponent=True)#pickle.load(open("debugging/agent1.pkl", "rb"))#QPlayer(learning=False)

# Setting up agents
if args.agentType == 1:
    print "Initialised new SARSA agent"
    agent = SarsaPlayer()
elif args.agentType == 2:
    print "Loaded up SARSA agent from disk"
    agent = pickle.load(open(args.agent_savefile, "rb"))

if args.opponentType == 0:
    print "Initialised RestrictedRandomPlayer opponent"
    opponent = RestrictedRandomPlayer()
elif args.opponentType == 1:
    print "Loaded up SARSA opponent from disk"
    opponent = pickle.load(open(args.opponent_savefile, "rb"))
    opponent.reverseTableStates()

agentFirst = True

# Current state
stateKey = game.state2key()

# Start measuring time
start_time = time.time()

# Loop running different episodes
while games < maxGames:

    # Opponent plays if it's the first mover. Opponent's mark is -1
    if not agentFirst:
        opponentAction = opponent.chooseAction(game.getBoard(), 0)
        game.play(-1, opponentAction)

    # Current state
    stateKey = game.state2key()
    
    # Initialise action-value pairs randomly
    if not stateKey in agent.getQTable():
        initDict = agent.createRandomDict()
        agent.addState(stateKey, initDict)

    # Agent chooses the best action for current state
    action = agent.chooseAction(game.getBoard(), epsilon = eps)


    # Loop through a single game
    # While game unfinished
    while (not game.checkWinner()[0]): 
        win = False
        reward = 0

        ## Agent plays
        # Get the resulting state after playing this action
        game.play(1, action)

        nextStateKey = game.state2key()

        # If the game is done after the agent's action
        # update reward, if not, play the opponents action
        if game.checkWinner()[0]:
            win, reward = game.checkWinner()
        # Opponent can still play
        else:
            opponentAction = opponent.chooseAction(game.getBoard(), epsilon = 0)
            game.play(-1, opponentAction)

            # If we win after the opponents action, update nextStateKey = game.state2key()
            nextStateKey = game.state2key()
            if not nextStateKey in agent.getQTable():
                initDict = agent.createRandomDict()
                agent.addState(nextStateKey, initDict)

            # Win and reward variable accordingly
            if game.checkWinner()[0]:
                win, reward = game.checkWinner()

        # Update Q
        # win and reward variable should not have been adjusted if the 
        # game can still be played
        if win:
            nextAction = None
        else:
            nextAction = agent.chooseAction(game.getBoard(), epsilon=eps)

        # Updating Q-values
        agent.updateQvalues(stateKey, action, nextStateKey, nextAction, reward, win, alpha=alpha, gamma = gamma)

        # Set action and stateKey after updating Q-values
        action = nextAction
        stateKey = nextStateKey

        if win:
            reward_per_episode.append(reward)
            if reward == 1:
                wins += 1
            elif reward == -1:
                losses += 1
            elif reward == 0:
                draw += 1

    games += 1
    if eps <= 0:
        eps = 0
    else:
        eps = (-eps_start/(.5*maxGames))*games + eps_start
    game.reset()
    agentFirst = not agentFirst

print "Game statistics"
elapsed_time_secs = time.time() - start_time
print "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
print "Wins for agent: %s" % wins
print "Wins for opponent %s " % losses
print "Draw plays: %s" % draw
#print agent.prettyprintTable()

output = open(args.agent_filename, 'wb')
output2 = open(args.qtable_filename, 'wb')
output3 = open(args.rewardsperep, 'wb')

# Save to disk
pickle.dump(agent, output)
pickle.dump(agent.getQTable(), output2)
pickle.dump(reward_per_episode, output3)


