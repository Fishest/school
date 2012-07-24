# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter()
    self._initialize_plan()

  def _initialize_plan(self, online=False):
    '''
    This is a helper to perform the offline planning
    of the value iteration.

    :param online: A flag indicating if the online version is used
    '''
    for count in range(self.iterations):
        values = self.values if online else self.values.copy()
        for state in self.mdp.getStates():
            action = self._next_policy(state)
            if action: values[state] = action[0]
        self.values = values

  def _next_policy(self, state):
    '''
    This is a helper that computes the next optimal policy
    value and action.

    :param state: The state to get the best policy for
    :returns: The best action for this state or None if empty
    '''
    actions = self.mdp.getPossibleActions(state)
    if len(actions) == 0:
        return None
    return max((self.getQValue(state, a), a) for a in actions)
    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    total = 0
    for nstate, prob in self.mdp.getTransitionStatesAndProbs(state, action):
        reward = self.mdp.getReward(state, action, nstate)
        value  = self.getValue(nstate) * self.discount
        total += prob * (reward + value)
    return total

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    action = self._next_policy(state)
    return action[1] if action else None

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
