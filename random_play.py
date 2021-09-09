from config import ACTION_COSTS, LIMIT, NP_ACTION_COSTS
import numpy as np
import random

class RandomPlayer(object):
    def __init(self):
        pass

    def set_ind(self, p):
        self.player = p

    def get_act(self, table):
        x = np.where(NP_ACTION_COSTS <= table.qi[self.player])[0]
        return random.choice(x)

    def __str__(self):
        return f"Random {self.player}"
