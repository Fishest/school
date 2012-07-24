# eightqueens.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import search
import random

class EightQueensState:
    """
    The Eight Puzzle is described in the course textbook on
    page 64.

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__(self, size):
        """
          Constructs a new eight puzzle from an ordering of numbers.
        """
        self.size  = size
        self.cells = [[0] * self.size] * self.size

    def isGoal(self):
        """
          Checks to see if the puzzle is in its goal state.
        """
        valid, queens = True, 0
        for row in self.cells:
            for cell in row:
                if cell == 'Q': queens += 1
        return queens == self.size

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.
        """
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.cells[row][col] == 0:
                    moves.append((row, col))
            if len(moves) > 1: break
        return moves

    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row,col = move
        state = EightQueensState(self.size)
        state.cells = [values[:] for values in self.cells]
        state.cells[row][col] = 'Q'
        for r in range(self.size):
            if r != row: state.cells[r][col] += 1
        for c in range(self.size):
            if c != col: state.cells[row][c] += 1

        dr,dc = row,col
        while dr > 0 and dc > 0:
            dr -= 1
            dc -= 1
        while dr < self.size and dc < self.size:
            if dr != row and dc != col:
                state.cells[dr][dc] += 1
            dr += 1
            dc += 1

        dr,dc = row,col
        while (dr < self.size - 1) and dc > 0:
            dr += 1
            dc -= 1
        while dr >= 0 and dc < self.size:
            if dr != row and dc != col:
                state.cells[dr][dc] += 1
            dr -= 1
            dc += 1

        return state

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.cells[row][col] != other.cells[row][col]:
                    return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        dashes = (self.size * 5) - self.size + 1
        horizontalLine = '-' * dashes
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if   col == 'Q': col = 'Q'
                elif col == 0: col = ' '
                else: col = 'x'
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

class EightQueensSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self, size=8):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.puzzle = EightQueensState(size)

    def getStartState(self):
        return self.puzzle

    def isGoalState(self,state):
        return state.isGoal()

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

if __name__ == '__main__':
    problem = EightQueensSearchProblem(8)
    path = search.breadthFirstSearch(problem)
    print('BFS found a path of %d moves: %s' % (len(path), str(path)))
    curr = problem.puzzle
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(curr)

        #raw_input("Press return for the next state...")   # wait for key stroke
        i += 1
