import numpy as np

from config import * 

def kill(x, y):
    if (x==y): return False
    if (y==0) and (x in [2,4,6,9]): return True
    if (x==2) and (y in [0, 7, 10]): return True
    if (x==3) and (y==2): return True
    if (x==4) and (y in [0,2,3,7,10]): return True
    if (x==5) and (y in [2,4]): return True
    if (x==6) and (y in [0,1,2,3,4,10]): return True
    if (x==8) and (y in [2,4,6]): return True
    if (x==9) and (y in [0,1,2,3,4,5,6,7]): return True
    return False

class Table(object):
    def __init__(self):
        self.states = {}
        self.players = [0, 1]

    def init_table(self):
        self.qi = [0,0]
        self.states = []
        self.last_choice = [-1, -1]
        self.step = 0

    def do_act(self,cur_act):
        self.states.append(cur_act);
        self.qi[0]-=ACTION_COSTS[cur_act[0]]
        self.qi[1]-=ACTION_COSTS[cur_act[1]]
        
    def has_win(self, show=0):
        if(show):
            print("state=",self.states)
        if not self.states: return False, -1
        cur = self.states[-1]
        if (kill(cur[0],cur[1])): return True, 0 
        if (kill(cur[1],cur[0])): return True, 1 
        return False, -1

    def game_end(self, show=0):
        win, winner = self.has_win(show)
        if win:
            return True, winner
        elif self.step>LIMIT:
            return True, -1
        return False, -1

class Game(object):
    def __init__(self, table):
        self.table = table
    
    def start_play(self, player0, player1, show=1):
        self.table.init_table()
        p0, p1 = self.table.players
        player0.set_ind(p0)
        player1.set_ind(p1)
        players = {p0: player0, p1:player1}
        print(f"Start Play for {player0} vs {player1}",)
        while True:
            cur_act = [player0.get_act(self.table), player1.get_act(self.table)]
            self.table.do_act(cur_act)
            if show:
                print(f"{player0}: {ACT[cur_act[0]]}  {player1}: {ACT[cur_act[1]]}")
                print(f"{player0}: {self.table.qi[0]} {player1}: {self.table.qi[1]}")
                print("===============")
            self.table.step+=1
            end, winner = self.table.game_end()
            if end:
                if show:
                    if winner != -1:
                        print(f"Game end. Winner is {players[winner]}")
                    else:
                        print("Game end. Tie")
                print(f"Winner is {players[winner]}\n\n--------------")
                return winner

"""
    def start_self_play(self, player, show=0, temp=1e-3):
        self.table.init_table()
        p0, p1 = self.table.players
        states, mcts_probs, current_players = [], [], []
        while True:
            act, act_probs = player.get_act(self.table, temp=temp, return_prob=1)
            states.append(self.table.qi)
            mcts.probs.append(act_probs)
"""
