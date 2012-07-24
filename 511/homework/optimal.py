from collections import defaultdict

# ------------------------------------------------------------ 
# problem variables
# ------------------------------------------------------------ 

# ------------------------------------------------------------ 
# processor
# ------------------------------------------------------------ 
class ValueIteration(object):

    actions = ['slow','fast']
    states  = ['cold', 'warm', 'over']
    transit = {
        'cold': {
            'slow':{'cold':1.0, 'warm':0.0, 'over':0.0 },
            'fast':{'cold':1.0/4, 'warm':3.0/4, 'over':0.0 }
        },
        'warm': {
            'slow':{'cold':1.0/4, 'warm':3.0/4, 'over':0 },
            'fast':{'cold':0, 'warm':7.0/8, 'over':1.0/8 }
        },
        'over': {
            'slow':{'cold':0, 'warm':0, 'over':1 },
            'fast':{'cold':0, 'warm':0, 'over':1 }
        },
    }
    reward = {
        'cold': {
            'slow':{'cold':4,   'warm':4, 'over':0 },
            'fast':{'cold':10, 'warm':10, 'over':0 }
        },
        'warm': {
            'slow':{'cold':4,  'warm':4,  'over':0 },
            'fast':{'cold':10, 'warm':10, 'over':0 }
        },
        'over': {
            'slow':{'cold':0, 'warm':0, 'over':0 },
            'fast':{'cold':0, 'warm':0, 'over':0 }
        },
    }

    def __init__(self, **kwargs):
        '''
        '''
        self.rounds   = kwargs.get('rounds', 1000)
        self.discount = kwargs.get('discount', 0.9)
        self.online   = kwargs.get('online', False)
        self.state_vs = defaultdict(int)
        for _ in range(self.rounds): self.get_next_vs()

    def get_q_value(self, state, action):
        '''
        '''
        total = 0
        for nstate in self.states:
            t = self.transit[state][action][nstate]
            r = self.reward[state][action][nstate]
            v = self.get_value(nstate)
            d = self.discount
            total += t * (r + d*v)
        return total

    def get_next_policy(self, state):
        '''
        '''
        return max((self.get_q_value(state, a), a) for a in self.actions)

    def get_next_vs(self):
        '''
        '''
        values = self.state_vs if self.online else self.state_vs.copy()
        for state in self.states:
            action = self.get_next_policy(state)
            values[state] = action[0]
        self.state_vs = values

    def get_value(self, state):
        '''
        '''
        return self.state_vs[state]

    def get_best_policies(self):
        '''
        '''
        for nstate in self.states:
            action = self.get_next_policy(nstate)
            print "%s -> %s" % (nstate, action[1])

    def __str__(self):
        '''
        '''
        return str(self.state_vs.items())

value = ValueIteration(rounds=5000, discount=0.5)
print value
value.get_best_policies()
