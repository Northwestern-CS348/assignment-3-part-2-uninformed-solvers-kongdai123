
from solver import *

#here's the logic
#the first item in the queue is the node being visited nowChild
#the second item is the one expanded later
#new children append to end of queue
#after children explore
#if there is only one element in queue
#end interation
#after each iteration pop first element update

queue = []

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        state = self.currentState.state
        depth = self.currentState.depth
        ##from solver.py the dictionary visited use self.currentState as key
        ## and TF as value
        movables = self.gm.getMovables()

        print(state)
        #print(movables)
        #this step simply populates parent state with children
        #print('start exploring')
        if state == self.victoryCondition:
            print(depth)
            return True

        for m in movables:
            #make the move
            self.gm.makeMove(m)
            newState = self.gm.getGameState()
            #print(newState)
            newChild = GameState(newState, depth + 1, m)
            newChild.parent = self.currentState
            self.currentState.children.append(newChild)
            self.gm.reverseMove(m)
        #print('children explored')

        while (len(self.currentState.children) != 0):
            firstChild = self.currentState.children[0]
            del self.currentState.children[0]
            query = self.visited.get(firstChild, False)
            if not query:
                self.visited[firstChild] = True
                self.currentState = firstChild
                self.gm.makeMove(firstChild.requiredMovable)
                #print('end')
                return False
        #at this time if the function has not terminated
        #there are no elements in the children array
        if self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return False
        else:
            #this means we have depleted all moves
            #leave it to the solver to decide
            return True


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        global queue
        state = self.currentState.state
        if len(queue)!= 0 and queue[0][0].state != state:
            queue = []
        depth = self.currentState.depth
        movables = self.gm.getMovables()
        if len(queue) == 0:
            queue.append([self.currentState, []])
        #print('start exploring')
        print(queue[0][0].state)
        if state == self.victoryCondition:
            queue = []
            print(depth)
            return True
        #populate children
        for m in movables:
            #make the move
            self.gm.makeMove(m)
            newState = self.gm.getGameState()
            newChild = GameState(newState, depth + 1, m)
            query = self.visited.get(newChild, False)
            if not query:
                self.visited[newChild] = True
                if depth == 0:
                    queue.append([newChild, [m]])
                else:
                    trace = queue[0][1][:]
                    #print(trace)
                    trace.insert(0, m)
                    queue.append([newChild, trace])
                #print(newState)
                #print (queue[len(queue) -1][1])
                newChild.parent = self.currentState
                self.currentState.children.append(newChild)
            self.gm.reverseMove(m)
        #print('children explored')

        nowChild = queue[0][0]
        if len(queue) == 1:
            del queue[0]
            return True
        nextChild = queue[1][0]
        self.currentState = nextChild
        i = 0
        #backtracking
        while i < len(queue[0][1]):
            self.gm.reverseMove(queue[0][1][i])
            i = i + 1

        i = len(queue[1][1])
        while i > 0:
            self.gm.makeMove(queue[1][1][i - 1])
            i = i - 1
        del queue[0]
        return False
