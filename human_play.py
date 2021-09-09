from game import Table, Game
from config import ACTION_COSTS, ACT
from mcts_pure import MCTSPlayer as MCTS_Pure

class HumanPlayer(object):
    def __init__(self):
        self.player = None

    def set_ind(self, p):
        self.player = p

    def __str__(self):
        return f"Human {self.player}"

    def get_act(self, table):
        try:
            act = int(input("Choose Your action:(-1: show all action)"))
        except Exception as e:
            act = -1
        if act == -1:
            print("Invalid action.")
            for a,b in enumerate(ACT):
                print(a,b)
            act = self.get_act(table)
        if table.qi[self.player]<ACTION_COSTS[act]:
            print("You don't have enough qi.")
            act = self.get_act(table)
        return act
