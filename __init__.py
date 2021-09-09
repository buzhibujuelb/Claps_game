from config import ACTION_COSTS, ACT, MAXROUND
from game import Table, Game 
from human_play import HumanPlayer
from mcts_pure import MCTSPlayer as MCTS_Pure
from random_play import RandomPlayer

score = [0, 0]

def race(player0, player1, round=5, show=0):
    for _ in range(round):
        try:
            score[game.start_play(player0 , player1, show)]+=1
        except KeyboardInterrupt:
            print("\nQuit")
            return -1

if __name__ == '__main__':
    table = Table()
    game = Game(table)
    mcts_player = MCTS_Pure()
    random_player = RandomPlayer()
    human_player = HumanPlayer()

    #race(random_player, human_player, round=5, show=1)
    #race(random_player, random_player, round=100)
    race(random_player, mcts_player, round=100)

    print(f"Total score is {score[0]}:{score[1]}")

