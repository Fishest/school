import sys, heapq

class Path(object):

    def __init__(self, word, path):
        self.word = word
        self.path = list(path)
        self.used = set(self.path)

    @staticmethod
    def extend(path, word):
        path = [] if not path else path.path
        return Path(word, path + [word])

class Queue(object): # priority queue w/ levenstein dist

    def __init__(self, goal):
        self.goal = goal
        self.data = []

    def enqueue(self, value):
        cost = ldistance(self.goal, value.word)
        heapq.heappush(self.data, (cost, value))

    def dequeue(self):
        return heapq.heappop(self.data)

    def empty(self):
        return len(self.data) == 0

def get_word_list(path='/usr/share/dict/american-english'):
    with open(path, 'r') as file:
        for line in file:
            yield line.strip()

def ldistance(a, b, cache=dict()):
    if (a,b) in cache: return cache[(a,b)]
    size = len(a) + 1
    d = [[0] * size for _ in range(size)]

    for i in range(0, size):
        d[i][0] = d[0][i] = i

    for i in range(1, size):
        for j in range(1, size):
            ad,de,ch = d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + 1
            if a[i - 1] == b[j - 1]: ch -= 1
            d[i][j] = min(ad, de, ch)
    cache[(a,b)] = d[size - 1][size - 1]
    return d[size - 1][size - 1]

def generate_next(word, words, used):
    for poss in words:
        if poss not in used and ldistance(word, poss) == 1:
            yield poss

def bfs_search(start, goal, words, choke=7):
    path = Queue(goal)
    path.enqueue(Path.extend(None, start))
    while not path.empty():
        cost, curr = path.dequeue()
        print curr.path
        if len(curr.path) + 1 > choke: continue
        for word in generate_next(curr.word, words, curr.used):
            step = Path.extend(curr, word)
            if step.word == goal: return step
            else: path.enqueue(step)
    return None

def find_transition(start, goal):
    if len(start) != len(goal):
        print "word lengths are not equal"
        return -1

    words = set([w.lower() for w in get_word_list() if len(w) == len(goal)])
    solve = bfs_search(start, goal, words)
    if solve: print solve.path
    else: print "no solution could be found"
       
if __name__ == "__main__":
    if len(sys.argv) > 2:
        find_transition(sys.argv[1], sys.argv[2])
    else: print "%s <start> <goal>" % sys.argv[0]
