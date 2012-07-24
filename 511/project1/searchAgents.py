# searchAgents.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
This file contains all of the agents that can be selected to
control Pacman.  To select an agent, use the '-p' option
when running pacman.py.  Arguments can be passed to your agent
using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a searchFunction=depthFirstSearch

Commands to invoke other search strategies can be found in the
project description.
"""
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search

class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search algorithm for a
    supplied search problem, then returns actions to follow that path.

    As a default, this agent runs DFS on a PositionSearchProblem to find location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError, fn + ' is not a search function in search.py.'
        func = getattr(search, fn)
        if 'heuristic' not in func.func_code.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError, heuristic + ' is not a function in searchAgents.py or search.py.'
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError, prob + ' is not a search problem type in SearchAgents.py.'
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game board. Here, we
        choose a path to the goal.  In this phase, the agent should compute the path to the
        goal and store it in a local variable.  All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception, "No search function provided for SearchAgent"
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in registerInitialState).  Return
        Directions.STOP if there is no further action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test,
    successor function and cost function.  This search problem can be
    used to find paths to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print 'Warning: this does not look like a regular search maze'

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, top), (right, 1))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print 'Warning: no food in corner ' + str(corner)
        self._expanded = 0 # Number of search nodes expanded
        food = startingGameState.getFood()
        for cx,cy in self.corners:
            food[cx][cy] = True
        self.start = (startingGameState.getPacmanPosition(), food)

    def getStartState(self):
        ''' Returns the start state (in your state
        space, not the full Pacman state space)
        '''
        return self.start

    def isGoalState(self, state):
        ''' Returns whether this search state is
        a goal state of the problem
        '''
        return state[1].count() == 0

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        successors = []
        self._expanded += 1
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                corners = state[1].copy()
                corners[nextx][nexty] = False
                successors.append((((nextx, nexty), corners), direction, 1))
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem; i.e.
    it should be admissible (as well as consistent).
    """
    current, visited = state
    distance  = util.manhattanDistance
    remaining = [c for c in problem.corners if visited[c[0]][c[1]]]
    mstpath   = [(0, current)]

    while len(remaining) > 0:
        node = min((distance(mstpath[-1][1], c), c) for c in remaining)
        mstpath.append(node)
        remaining.remove(node[1])
    return sum(node[0] for node in mstpath)

class AStarCornersAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem

class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0
        self.heuristicInfo = {}
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class PathRouteProblem:

    @staticmethod
    def solve(start, nodes, weight):
        source  = max((v, k) for k,v in weight[start].items())[1]
        x,y     = source
        nodes[x][y] = False
        problem = PathRouteProblem(source, nodes, weight)
        actions = search.ucs(problem)
        total   = problem.getCostOfActions(actions)
        return (actions, total)

    def __init__(self, start, nodes, weight):
        self.nodes  = nodes
        self.start  = start
        self.weight = weight

    def getStartState(self):
        return (self.start, self.nodes)

    def isGoalState(self, state):
        current, nodes = state
        print current, nodes
        return nodes.count() == 0

    def getSuccessors(self, state):
        current, nodes = state
        x,y = current
        successors = []
        for node in nodes.asList():
            follow = nodes.copy()
            follow[node[0]][node[1]] = False
            successors.append(((node, follow), node, self.weight[current][node]))
        return successors

    def getCostOfActions(self, actions):
        cost = 0
        node = self.start
        for step in actions:
            cost += self.weight[node][step]
            node  = step
        return cost

class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        #self.searchFunction = lambda prob: search.ucs(prob)
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a
    Grid (see game.py) of either True or False. You can call foodGrid.asList()
    to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, problem.walls gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use. For example,
    if you only want to count the walls once and store that value, try:
      problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount']
    """
    current, foodGrid = state
    distance  = util.manhattanDistance
    remaining = foodGrid.asList()

    if len(problem.heuristicInfo) == 0:
    # ------------------------------------------------------------
    # min-cost step penalty
    # ------------------------------------------------------------
    #    import heapq
    #    tree = {}
    #    heap = []
    ## ------------------------------------------------------------
    #    # calculate minimum spanning tree kruskal
    #    # calculate pair to pair weights
    ## ------------------------------------------------------------
    #    remaining.append(current)
    #    for start in remaining:
    #        tree[start] = set([start])
    #        for node in remaining:
    #            if start != node:
    #                cost = mazeDistance(start, node, problem.startingGameState)
    #                #cost = distance(start, node) # faster
    #                heapq.heappush(heap, (cost, start, node))
    #    remaining.remove(current)

    #    # calculate minimum spanning tree kruskal 
    #    path = []
    #    while len(heap) != 0:
    #        cost, u, v = heapq.heappop(heap)
    #        if tree[u] != tree[v]:
    #            path.append((cost, u, v))
    #            union = tree[v].union(tree[u])
    #            for value in union: tree[value] = union
    #    problem.heuristicInfo = path
    # ------------------------------------------------------------
        # calculate single source minimum bellman ford
        # calculate pair to pair weights
    # ------------------------------------------------------------
        # predecessor graph class object
        class SSNode(object):
            def __init__(self, node, dist=99999):
                self.node = node
                self.dist = dist

        # calculate pair edge weights
        tree = {}
        remaining.append(current)
        for start in remaining:
            tree[start] = {start:0}
            for node in remaining:
                if start != node:
                    if node in tree and start in tree[node]:
                        # a -> b == b -> a
                        tree[start][node] = tree[node][start]
                    else:
                        cost = mazeDistance(start, node, problem.startingGameState)
                        tree[start][node] = cost
        remaining.remove(current)

        # bellman ford init
        source = max((v, k) for k,v in tree[current].items())[1]
        vertices = []
        for node in remaining:
            if node == source:
                vertices.append(SSNode(node, 0))
            else: vertices.append(SSNode(node))

        # bellman ford main
        for _ in range(len(vertices) - 1):
            for u in vertices:
                for v in vertices:
                    if u.dist == 99999: continue
                    if u.dist + tree[u.node][v.node] < v.dist:
                        v.dist = u.dist + tree[u.node][v.node]

        path = sorted(((c.dist, c.node) for c in vertices), reverse=True)
        problem.heuristicInfo = path

    # ------------------------------------------------------------
    # remaining cost on single shortest path
    # ------------------------------------------------------------
    if len(remaining) > 0:
        path = problem.heuristicInfo
        initial, start = path[0]

        if start in remaining:
            return distance(current, start) + initial

        for cost, node in path:
            if current == node: return cost
            if node in remaining:
                return cost + distance(current, node)
    return 0

    #if len(problem.heuristicInfo) == 0:
    # ------------------------------------------------------------
    # min-cost step penalty
    # ------------------------------------------------------------
    #    weight = {}
    #    for start in remaining:
    #        weight[start] = {}
    #        for k in remaining:
    #            weight[start][k] = mazeDistance(start, k, problem.startingGameState)
    #    import pdb;pdb.set_trace()
    #    problem.heuristicInfo = weight

    ## ------------------------------------------------------------
    ## mst path attempt
    ## ------------------------------------------------------------
    #if len(remaining) != 0:
    #    node = max((distance(current, c), c) for c in remaining)
    #    path = problem.heuristicInfo[node[1]]
    #    dist = max(path[c] for c in remaining)
    #    cost = dist + node[0]
    #    print cost, len(remaining)
    #    return cost
    #return 0

    # ------------------------------------------------------------
    # all pairs
    # ------------------------------------------------------------
        #weight = {}
        #for start in remaining:
        #    weight[start] = {}
        #    for end in remaining:
        #        weight[start][end] = distance(start, end)

        #total = {}
        #for start in remaining:
        #    test = dict((node,False) for node in remaining)
        #    total[start] = 0
        #    item = start
        #    test[item] = True
        #    while not all(test.values()):
        #        cost, item = min((v, k) for k,v in weight[item].items() if not test[k])
        #        total[start] += cost
        #        test[item] = True
        #problem.heuristicInfo = total

    # ------------------------------------------------------------
    # calculate least amount of repeat east and west steps
    # ------------------------------------------------------------
        #weight = {}
        #for start in remaining:
        #    x,y = start
        #    weight[start] = {'e':0, 'w':0, 'n':0, 's':0}
        #    for rest in remaining:
        #        rx, ry = rest
        #        weight[start]['e'] = max(weight[start]['w'], x - rx)
        #        weight[start]['w'] = max(weight[start]['e'], rx - x)
        #        weight[start]['n'] = max(weight[start]['n'], y - ry)
        #        weight[start]['s'] = max(weight[start]['s'], ry - y)

        #total = {}
        #for start in remaining:
        #    cost = max(distance(c, start) for c in remaining)
        #    total[start] = cost
        #problem.heuristicInfo = total

    # ------------------------------------------------------------
    # calculate least amount of repeat east and west steps
    # ------------------------------------------------------------
    #if len(remaining) != 0:
    #    #possible = sorted((weight[n][e], c) for n in remaining)
    #    east  = sum(weight[n]['e'] for n in remaining)
    #    south = sum(weight[n]['s'] for n in remaining)
    #    cost  = max(distance(c, current) for c in remaining)
    #    cost  =  east + cost + south
    #    return cost
    #return 0

    # ------------------------------------------------------------
    # max n,s,e,w square
    # ------------------------------------------------------------
    #if len(remaining) > 0:
    #    x,y = current
    #    n,s,e,w = y,y,x,x
    #    for nx,ny in remaining:
    #        if nx > e: e = nx
    #        if nx < w: w = nx
    #        if ny > n: n = ny
    #        if ny < s: s = ny
    #    tx = min((e - x) * 2 + (x - w), (x - w) * 2 + (e - x))
    #    ty = min((n - y) * 2 + (y - s), (y - s) * 2 + (n - y))
    #    total = tx + ty
    #    return total
    #return 0

    # ------------------------------------------------------------
    # static corners extrema spiral from start
    # a b
    # c d
    # ------------------------------------------------------------
    #if len(problem.heuristicInfo) == 0:
    #    x,y = current
    #    a,b,c,d = current, current, current, current
    #    for nx,ny in remaining:
    #        if (nx <= a[0] and ny >= a[1]): a = (nx,ny)
    #        if (nx >= b[0] and ny >= b[1]): b = (nx,ny)
    #        if (nx <= c[0] and ny <= c[1]): c = (nx,ny)
    #        if (nx >= d[0] and ny <= d[1]): d = (nx,ny)
    #    problem.heuristicInfo = [a,b,c,d]

    #corners = [c for c in problem.heuristicInfo if c in remaining]
    #mstpath = [(0, current)]

    #while len(corners) > 0:
    #    node = min((distance(mstpath[-1][1], c), c) for c in corners)
    #    mstpath.append(node)
    #    corners.remove(node[1])
    #return sum(node[0] for node in mstpath)

    # ------------------------------------------------------------
    # dynamic corner extrema spiral
    # a b
    # c d
    # ------------------------------------------------------------
    #if len(remaining) > 0:
    #    x,y = current
    #    a,b,c,d = current, current, current, current
    #    for nx,ny in remaining:
    #        if (nx <= a[0] and ny >= a[1]): a = (nx,ny)
    #        if (nx >= b[0] and ny >= b[1]): b = (nx,ny)
    #        if (nx <= c[0] and ny <= c[1]): c = (nx,ny)
    #        if (nx >= d[0] and ny <= d[1]): d = (nx,ny)

    #    corners = set([a,b,c,d])
    #    cost, corn = min((distance(n, current), n) for n in corners)
    #    corners.remove(corn)
    #    while len(corners) > 0:
    #        plus, node = min((distance(n, corn), n) for n in corners)
    #        cost += plus
    #        corn  = node
    #        corners.remove(corn)
    #    print cost, len(remaining)
    #    return cost
    #return 0

    # ------------------------------------------------------------
    # max (1,1)(n.w), (-1,1)(n,e), (-1,-1)(s,e), (1,-1)(s,w)
    # ------------------------------------------------------------
    #if len(remaining) > 0:
    #    x,y = current
    #    # {1:(1,1), 2:(-1,1), 3:(-1,-1), 4:(1,-1)
    #    r = dict((i,(x,y)) for i in [1,2,3,4])
    #    for nx,ny in remaining:
    #        if  nx >= x and ny >= y:
    #            rw, rn = r[1]
    #            r[1] =(max(nx, rw), max(rn, ny))
    #        elif nx >= x and ny <= y:
    #            rw, rs = r[4]
    #            r[4] =(max(nx, rw), min(rs, ny))
    #        elif nx <= x and ny >= y:
    #            re, rn = r[2]
    #            r[2] =(min(nx, re), max(rn, ny))
    #        elif nx <= x and ny <= y:
    #            re, rs = r[3]
    #            r[3] =(min(nx, re), min(rs, ny))

    #    xn = min((r[1][0] - x) * 2 + x - r[2][0], r[1][0] - x + (x - r[2][0]) * 2)
    #    xs = (r[4][0] - x) + (x - r[3][0])
    #    #xs = min((r[4][0] - x) * 2 + x - r[3][0], r[4][0] - x + (x - r[3][0]) * 2)
    #    yw = min((r[1][1] - y) * 2 + y - r[4][1], r[1][1] - y + (y - r[4][1]) * 2)
    #    ye = min((r[2][1] - y) * 2 + y - r[3][1], r[2][1] - y + (y - r[3][1]) * 2)
    #    total = xn + xs + yw + ye
    #    return total
    #return 0

    # ------------------------------------------------------------
    # mst of food to food
    # ------------------------------------------------------------
    #if len(remainhristofides
    #    farthest  = max((distance(current, c), c) for c in remaining)
    #    return sum(distance(farthest[1], c) for c in remaining)
    #return 0

    # ------------------------------------------------------------
    # max of remaining food 
    # ------------------------------------------------------------
    #if len(remaining) != 0:
    #    weights = sorted((distance(current, c), c) for c in remaining)
    #    cost, root = weights.pop()
    #    while len(weights) > 0:
    #        weights = sorted(((distance(root, c[1]), c[1]) for c in weights), reverse=True)
    #        weight, _ = weights.pop()
    #        cost += weight
    #    return cost
    #return 0

    # ------------------------------------------------------------
    # max distance to food
    # ------------------------------------------------------------
    #if len(remaining) != 0:
    #    #large  = max((distance(current, c) for c in remaining))
    #    #large += len(remaining)
    #    #large  = large / 2
    #    large = sum(problem.heuristicInfo[c] for c in remaining)
    #    print large, len(remaining)
    #    return large
    #return 0

    # ------------------------------------------------------------
    # mst of me to food    
    # ------------------------------------------------------------
    #mstpath = [(0, current)]
    #while len(remaining) > 0:
    #    node = max((distance(mstpath[-1][1], c), c) for c in remaining)
    #    mstpath.append(node)
    #    remaining.remove(node[1])
    #return sum(node[0] for node in mstpath) - distance(current, mstpath[0][1])

class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception, 'findPathToClosestDot returned an illegal move: %s!\n%s' % t
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print 'Path found with cost %d.' % len(self.actions)

    def findPathToClosestDot(self, gameState):
        "Returns a path (a list of actions) to the closest dot, starting from gameState"
        # Here are some useful elements of the startState
        x,y = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)
        return search.bfs(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    """
      A search problem for finding a path to any food.

      This search problem is just like the PositionSearchProblem, but
      has a different goal test, which you need to fill in below.  The
      state space and successor function do not need to be changed.

      The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
      inherits the methods of the PositionSearchProblem.

      You can use this search problem to help you fill in
      the findPathToClosestDot method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test
        that will complete the problem definition.
        """
        x,y = state
        return self.food[x][y]

##################
# Mini-contest 1 #
##################

#class AStarFoodSearchAgent(SearchAgent):
class ApproximateSearchAgent(SearchAgent):
    "Implement your contest entry here.  Change anything but the class name."

    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception, 'findPathToClosestDot returned an illegal move: %s!\n%s' % t
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print 'Path found with cost %d.' % len(self.actions)

    def findPathToClosestDot(self, gameState):
        "Returns a path (a list of actions) to the closest dot, starting from gameState"
        x,y = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)
            
        return search.ucs(problem)

def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built.  The gameState can be any game state -- Pacman's position
    in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + point1
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False)
    return len(search.bfs(prob))
