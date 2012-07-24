# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions, Actions
import random, util
import math
from mypy import any_food_find, specific_find, any_capsule_find

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()
    legalMoves.remove('Stop')

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, current, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    distance  = util.manhattanDistance
    successor = current.generatePacmanSuccessor(action)
    pacman    = successor.getPacmanPosition()
    ghosts    = successor.getGhostStates()
    walls     = successor.getWalls()
    score = 0

    if current.getFood().count() > successor.getFood().count():
        score += 2
    else:
        cfood = min(distance(f, pacman) for f in current.getFood().asList())
        sfood = min(distance(f, pacman) for f in successor.getFood().asList())
        if sfood >= cfood: score += 1.0/sfood
        else: score -= 1.0/sfood

    if len(current.getCapsules()) > len(successor.getCapsules()):
        score += 20
    elif len(successor.getCapsules()) > 0:
        ccap = min(distance(c, pacman) for c in current.getCapsules())
        scap = min(distance(c, pacman) for c in successor.getCapsules())
        if scap >= ccap: score += 1.0/scap

    for ghost in ghosts:
        gp = ghost.getPosition()
        gd = distance(gp, pacman)
        gt = ghost.scaredTimer
        ac = Actions.getLegalNeighbors(gp, walls)
        
        if gt != 0 and gd <= gt: score += 200
        elif pacman in ac: score -= 500

    return score

    #if len(capsules) > 0:
    #    mcaps  = min(distance(c, pacman) for c in capsules)
    #    score += 20 if mcaps == 0 else 5 * math.ceil(1.0 / mcaps)
    #   
    #if foods.count() > 0:
    #    dfood  = [distance(f, pacman) for f in foods]
    #    mfood  = min(dfood)
    #    cfood  = sum(1.0 for f in dfood if f == mfood)
    #    score += 10 if mfood == 0 else cfood * math.ceil(1.0 / mfood)
    #    
    #for ghost in ghosts:
    #    gp = ghost.getPosition()
    #    gd = distance(gp, pacman)
    #    gt = ghost.scaredTimer
    #    ac = Actions.getLegalNeighbors(gp, walls)
    #    
    #    if gt != 0 and gd <= gt: score += 200
    #    elif pacman in ac: score -= 500
    #      
    #return score

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    def min_value(state, depth, agent):
        moves = state.getLegalActions(agent)
        if Directions.STOP in moves:
            moves.remove(Directions.STOP)
        if len(moves) == 0 or depth == 0:
            return (self.evaluationFunction(state), 'STOP')
        next_value = max_value if agent == 1 else min_value
        successors = ((state.generateSuccessor(agent, m), m) for m in moves)
        if agent == 1: depth -= 1
        return min((next_value(s, depth, agent - 1)[0], m) for s,m in successors)

    def max_value(state, depth, agent):
        moves = state.getLegalActions(agent)
        if Directions.STOP in moves:
            moves.remove(Directions.STOP)
        if len(moves) == 0 or depth == 0:
            return (self.evaluationFunction(state), 'STOP')
        ghosts = state.getNumAgents() - 1
        successors = ((state.generateSuccessor(agent, m), m) for m in moves)
        return max((min_value(s, depth, ghosts)[0], m) for s,m in successors)

    return max_value(gameState, self.depth, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    def min_value(state, depth, agent, alpha, beta):
        moves = state.getLegalActions(agent)
        if Directions.STOP in moves:
            moves.remove(Directions.STOP)
        if len(moves) == 0 or depth == 0:
            return (self.evaluationFunction(state), 'STOP')
        next_value = max_value if agent == 1 else min_value
        successors = ((state.generateSuccessor(agent, m), m) for m in moves)
        if agent == 1: depth -= 1

        value = (+1000000, 'STOP')
        for s,m in successors:
            value = min(value, (next_value(s, depth, agent - 1, alpha, beta)[0], m))
            if value <= alpha: break
            beta = min(beta, value)
        return value

    def max_value(state, depth, agent, alpha, beta):
        moves = state.getLegalActions(agent)
        if Directions.STOP in moves:
            moves.remove(Directions.STOP)
        if len(moves) == 0 or depth == 0:
            return (self.evaluationFunction(state), 'STOP')
        ghosts = state.getNumAgents() - 1
        successors = ((state.generateSuccessor(agent, m), m) for m in moves)

        value = (-1000000, 'STOP')
        for s,m in successors:
            value = max(value, (min_value(s, depth, ghosts, alpha, beta)[0], m))
            if value >= beta: break
            aplha = max(alpha, value)
        return value

    alpha = (-1000000, 'STOP')
    beta  = (+1000000, 'STOP')
    return max_value(gameState, self.depth, 0, alpha, beta)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    def min_value(state, depth, agent):
        moves = state.getLegalActions(agent)
        if Directions.STOP in moves:
            moves.remove(Directions.STOP)
        if len(moves) == 0 or depth == 0:
            return (self.evaluationFunction(state), 'STOP')
        next_value = max_value if agent == 1 else min_value
        successors = ((state.generateSuccessor(agent, m), m) for m in moves)
        if agent == 1: depth -= 1
        return random.choice([(next_value(s, depth, agent - 1)[0], m) for s,m in successors])

    def max_value(state, depth, agent):
        moves = state.getLegalActions(agent)
        if Directions.STOP in moves:
            moves.remove(Directions.STOP)
        if len(moves) == 0 or depth == 0:
            return (self.evaluationFunction(state), 'STOP')
        ghosts = state.getNumAgents() - 1
        successors = ((state.generateSuccessor(agent, m), m) for m in moves)
        return max((min_value(s, depth, ghosts)[0], m) for s,m in successors)

    return max_value(gameState, self.depth, 0)[1]

def betterEvaluationFunction(current):
    """
    * if there are any capsules left, lets really move towards
      the closest one.
    * If there is food left, try to move to the closest
    * For each ghost
      - if they are scared and nearby, chase them
      - otherwise never be in the same position as them
    """
    pacman    = current.getPacmanPosition()
    foods     = current.getFood()
    walls     = current.getWalls()
    ghosts    = current.getGhostStates()
    distance  = util.manhattanDistance
    capsules  = current.getCapsules()
    score     = current.getScore()

    if len(capsules) > 0:
        mcaps  = min(specific_find(current, pacman, c) for c in capsules)
        score += 20 if mcaps == 0 else 5 * math.ceil(1.0 / mcaps)
       
#    if foods.count() > 0:
#        dfood  = [distance(f, pacman) for f in foods.asList()]
#        mfood  = min(dfood)
#        cfood  = sum(1.0 for f in dfood if f == mfood)
#        score += 1.0 / mfood
    score += 1.0 / any_food_find(current)
        
    for ghost in ghosts:
        gp = ghost.getPosition()
        gd = distance(gp, pacman)
        gt = ghost.scaredTimer
        
        if gt != 0 and gd <= gt: score += 200
        elif pacman == gp: score -= 500
    
    return score

# Abbreviation
better = betterEvaluationFunction

def highScoreEvaluationFunction(current):
    """
    * if there are any capsules left, move towards them
    * if we are out of capsules, gather remaining food
    * Try _really_ hard to get a scared ghost if we can
    * if there is a chance of death, don't risk it
    """
    pacman    = current.getPacmanPosition()
    foods     = current.getFood()
    walls     = current.getWalls()
    ghosts    = current.getGhostStates()
    distance  = util.manhattanDistance
    capsules  = current.getCapsules()
    score     = current.getScore()

    if len(capsules) > 0:
          score += 5 * (1.0 / any_capsule_find(current))
    else: score += 1 * (1.0 / any_food_find(current))
        
    max_scared = 0 
    for ghost in ghosts:
        gp = ghost.getPosition()
        gt = ghost.scaredTimer
         
        if gt > 0:
            distance = specific_find(current, pacman, gp)
            if gt >= distance:
                value = 200 * (1.0 / distance)
                max_scared = max(max_scared, value)
        elif pacman == gp: score = -1000
     
    return score + max_scared

class ContestAgent(AlphaBetaAgent):
  """
    Your agent for the mini-contest
  """

  def __init__(self, evalFn = 'highScoreEvaluationFunction', depth = '3'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)
