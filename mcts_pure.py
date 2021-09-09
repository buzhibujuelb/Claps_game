import numpy as np
import copy
from config import ACTION_COSTS, LIMIT, NP_ACTION_COSTS, ACT
from operator import itemgetter

def random_policy_fn(table, id):
    x = np.where(NP_ACTION_COSTS <= table.qi[0])[0]
    y = np.where(NP_ACTION_COSTS <= table.qi[1])[0]
    act_ava = []
    for a in x:
        for b in y:
            act_ava.append([a,b])
    act_probs = np.random.rand(len(act_ava))
    return zip(act_ava, act_probs)

def policy_value_fn(table, id):
    x = np.where(NP_ACTION_COSTS <= table.qi[0])[0]
    y = np.where(NP_ACTION_COSTS <= table.qi[1])[0]
    act_ava = []
    for a in x:
        for b in y:
            act_ava.append([a,b])
    
    act_probs = np.ones(len(act_ava))/len(act_ava)
    return zip(act_ava, act_probs), 0

def hash(a):
    return a[0]*len(ACTION_COSTS)+a[1]

def unhash(a):
    x=np.array([a//len(ACTION_COSTS),a%len(ACTION_COSTS)])
    return x

class Node(object):
    def __init__(self, parent, p):
        self._parent = parent
        self._children = {}
        self._vis = 0
        self._Q = 0
        self._u = 0
        self._p = p

    def expand(self, act_v):
        for act, prob in act_v:
            if hash(act) not in self._children:
                #print("hash ",act,ACT[act[0]],ACT[act[1]],"->",hash(act))
                self._children[hash(act)] = Node(self,prob)

    def select(self, c_puct):
        return max(self._children.items(),
                key=lambda son: son[1].get_value(c_puct))

    def update(self, v):
        self._vis +=1
        self._Q += 1.0*(v - self._Q)/self._vis

    def reupdate(self, v):
        if self._parent:
            self._parent.reupdate(v)
        self.update(v)

    def get_value(self, c_puct):
        self._u = (c_puct *self._p * np.sqrt(self._parent._vis)/(1+self._vis))
        return self._Q + self._u

    def is_leaf(self):
        return self._children == {}

    def is_root(self):
        return self._parent is None

class MCTS(object):
    def __init__(self, policy_value_fn, c_puct=5, n_playout=LIMIT):
        self._root = Node(None, 1.0)
        self._policy = policy_value_fn
        self._c_puct = c_puct
        self._n_playout = n_playout
        self.id = -1

    def _playout(self, state):
        node = self._root
        while not node.is_leaf():
            cnode = node
            act, node = node.select(self._c_puct)
            act=unhash(act)
            state.do_act(act)
        act_probs, _ = self._policy(state, self.id)
        end, winner = state.game_end()
        if not end:
            node.expand(act_probs)
        leaf_value = self._evaluate_rollout(state, self.id)
        node.reupdate(leaf_value)

    def _evaluate_rollout(self, state, id, limit=LIMIT):
        for i in range(limit):
            end, winner = state.game_end()
            if end:
                break
            act_probs = random_policy_fn(state, id)
            a=-999999999
            max_act = -1

            for x in act_probs:
                if(x[1]>a):
                    a=x[1]
                    max_act=x[0]
            #max_act = max(act_probs, key=lambda s:s[1][1]) 
            state.do_act(max_act)
        if winner == -1:
            return 0
        else:
            return 1 if winner == self.id else -1

    def get_act(self, state):
        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)

        return unhash(max(self._root._children.items(),
                key= lambda son: son[1]._vis)[0])

    def update_with_act(self, last_choice):
        self._root = Node(None, 1.0)
        
        if last_choice in self._root._children:
            self._root = self._root._children[last_choice]
            self._root._parent = None
        else:
            self._root = Node(None, 1.0)
    def __str__(self):
        return "MCTS"




class MCTSPlayer(object):
    def __init__(self, c_puct=5, n_playout=LIMIT):
        self.mcts = MCTS(policy_value_fn, c_puct, n_playout)

    def set_ind(self, p):
        self.player = p
        self.mcts.id = p
    
    def get_act(self, table):
        act = self.mcts.get_act(table)
        #self.mcts.update_with_act(hash(act))
        self.mcts.update_with_act(-1)
        return  act[self.player]

    def __str__(self):
        return f"MCTS {self.player}"
