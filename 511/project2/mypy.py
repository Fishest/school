import util
from game import Directions, Agent, Actions
from collections import defaultdict

# ------------------------------------------------------------------ #
# Classes
# ------------------------------------------------------------------ #
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

class Node(object):
    ''' Represents a node path state chain that 
    is used to make the generic search function
    generic.
    '''
    __slots__ = ['position', 'parent', 'action', 'cost', 'problem', 'depth']

    @staticmethod
    def create(problem):
        ''' Given an initial position, create a node

        :param problem: The initial problem to solve
        :returns: The initial starting node
        '''
        initial = problem.getStartState()
        return Node(problem, initial, None, "Stop", 0, 0)

    def __init__(self, problem, position, parent, action, cost, depth):
        ''' Initialize a new node instance

        :param problem: The problem state for the heuristic
        :param position: The position of this node
        :param parent: The previous parent node
        :param action: The action taken to get here
        :param cost: The total cost of the path to here
        :param depth: The total depth of the path to here
        '''
        self.position = position
        self.parent   = parent
        self.action   = action
        self.cost     = cost
        self.problem  = problem
        self.depth    = depth

    def append(self, state):    
        ''' Given a new state, create a new path node

        :param state: The new state to append
        :returns: A new state node
        '''
        state, action, cost = state
        cost  = self.cost  + cost
        depth = self.depth + 1
        return Node(self.problem, state, self, action, cost, depth)

    def getPath(self):
        ''' Given a goal, return the path to that goal

        :returns: A path to the given goal
        '''
        path, node = [], self
        while node.parent != None:
            path.insert(0, node.action)
            node = node.parent
        return path

    def getPositions(self):
        ''' Given a goal, return the path of positions
        to that goal.

        :returns: A path of the positions to the given goal
        '''
        states, node = [], self
        while node.parent != None:
            states.insert(0, node.position)
            node = node.parent
        return states

    def contains(self, node):
        ''' Checks if the given state is already in this path

        :param state: The state to check for existence
        :returns: True if in this path, False otherwise
        '''
        # TODO make this O(1) with an instance singleton
        return node.position in self.getPositions()

    def __hash__(self):
        ''' An overload of the hash function

        :returns: A hash of the current state
        '''
        return hash(self.position)

    def __len__(self):
        ''' An overload of the len function

        :returns: The current length of the path
        '''
        return self.depth

    def __str__(self):
        ''' Returns a string representation of this node

        :returns: The representation of this node
        '''
        parent = str(self.parent.position) if self.parent else "(start)"
        params = (parent, self.action, self.cost, str(self.position), self.depth)
        return "node(%s %s(%d) %s) len(%d)" % params

# ------------------------------------------------------------------ #
# Search Implementations
# ------------------------------------------------------------------ #
def genericSearch(problem, frontier):
    ''' a generic framework for searching

    :param problem: The problem to be solved
    :param frontier: The frontier structure to use
    :returns: A path to solve the specified problem
    '''
    start   = Node.create(problem)
    visited = defaultdict(lambda:0)
    frontier.push(start)

    while not frontier.isEmpty():
        state = frontier.pop()
        if problem.isGoalState(state.position):
            return state.getPath()

        visited[state.position] += 1
        if visited[state.position] > 1: continue
        for action in problem.getSuccessors(state.position):
            child = state.append(action)
            if child.position not in visited:
                frontier.push(child)

def depthLimitedSearch(problem, limit):
    ''' Search the deepest nodes in the search tree first
    up to a given limit.
    [2nd Edition: p 75, 3rd Edition: p 87]

    :param problem: The problem to solve
    :returns: A path that solves the specified problem
    '''
    return genericSearch(problem, util.LimitedStack(limit))

def depthFirstSearch(problem):
    ''' Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    :param problem: The problem to solve
    :returns: A path that solves the specified problem
    '''
    return genericSearch(problem, util.Stack())

def breadthFirstSearch(problem):
    ''' Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]

    :param problem: The problem to solve
    :returns: A path that solves the specified problem
    '''
    return genericSearch(problem, util.Queue())

def uniformCostSearch(problem):
    ''' Search the node that has the lowest combined cost first.

    :param problem: The problem to solve
    :returns: A path that solves the specified problem
    '''
    cost = lambda node: node.cost
    return genericSearch(problem, util.PriorityQueueWithFunction(cost))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def pointHeuristic(goal):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    def heuristic(state, problem):
        xy1 = state
        xy2 = goal
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
    return heuristic

def aStarSearch(problem, heuristic=nullHeuristic):
    ''' Search the node that has the lowest combined cost and heuristic first.

    :param problem: The problem to solve
    :param heuristic: The heuristic to choose the next node with
    :returns: A path that solves the specified problem
    '''
    cost = lambda node: node.cost + heuristic(node.position, node.problem)
    return genericSearch(problem, util.PriorityQueueWithFunction(cost))

# ------------------------------------------------------------------ #
# Aliases
# ------------------------------------------------------------------ #
bfs = breadthFirstSearch
dfs = depthFirstSearch
dls = depthLimitedSearch
ass = aStarSearch
ucs = uniformCostSearch

# ------------------------------------------------------------------ #
# Some Search Agents
# ------------------------------------------------------------------ #
class SearchAgent(object):
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
        func = globals()[fn]
        heur = globals()[heuristic]
        self.searchFunction = lambda x: func(x, heuristic=heur)
        self.searchType = globals()[prob]

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
        return bfs(problem)

class PositionSearchProblem(SearchProblem):
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
        return state == self.goal

    def getSuccessors(self, state):

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

class AnyFoodSearchProblem(PositionSearchProblem):

    def __init__(self, gameState):
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

class AnyCapsuleSearchProblem(PositionSearchProblem):

    def __init__(self, gameState):
        self.capsules = gameState.getCapsules()

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
        return state in self.capsules

# ------------------------------------------------------------ 
# helper search methods
# ------------------------------------------------------------ 
def any_food_find(state):
    problem = AnyFoodSearchProblem(state)
    result = bfs(problem)
    return 1 if result == None else len(result)

def any_capsule_find(state):
    problem = AnyCapsuleSearchProblem(state)
    result = bfs(problem)
    return 1 if result == None else len(result)

def specific_find(state, start, goal):
    problem = PositionSearchProblem(state, start=start, goal=goal, warn=False)
    result  = ass(problem, pointHeuristic(goal))
    return 1 if result == None else len(result)

