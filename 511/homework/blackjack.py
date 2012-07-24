import random
from collections import defaultdict

class Blackjack(object):
    '''
    '''
    Cards = [5,10,11]

    def hit(self, hand, dirty=0):
        '''
        '''
        if dirty > random.random():
            total = sum(hand)
            worst = [(total + c, c) for c in self.Cards]
            for t, c in worst:
                if t > 21: return hand + [c]
            return hand + [min(worst)[1]]
        return hand + [random.choice(self.Cards)]

    def score(self, hand):
        '''
        '''
        total = sum(hand)
        if    0 <= total <= 14: return 0
        elif 15 <= total <= 19: return 3
        elif       total == 20: return 9
        elif       total == 21: return 12
        else:                   return -6

initial   = [11]
blackjack = Blackjack()

print "Clean Game"
results   = defaultdict(int)
for i in range(1000):
    hand = blackjack.hit(initial, dirty=0.0)
    results[blackjack.score(hand)] += 1
print [(k, v/1000.0) for k,v in results.items()]

print "Dirty Game"
results   = defaultdict(int)
for i in range(1000):
    hand = blackjack.hit(initial, dirty=0.5)
    results[blackjack.score(hand)] += 1
print [(k, v/1000.0) for k,v in results.items()]
