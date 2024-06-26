from searcher.Node import Node
from asyncio import sleep
import time
import json
class Searcher:
  def __init__(self, problem):
    self.problem = problem
    self.goalRow, self.goalCol= self.getGoalCoords()

  def getInitialPos(self):
    for row_num, row in enumerate(self.problem):
      if 'i' in row:
        col_num = row.index('i')
        return [row_num, col_num]
    return 0

  def getGoalCoords(self):
    for row_num, row in enumerate(self.problem):
      if 'g' in row:
        col_num = row.index('g')
        return [row_num, col_num]
    return 0
  
  def isSaved(self, saved, state):
    for old in saved:
      if old.getState() == state.getState(): return True
    return False

  async def startLinearDepth(self, onIteration, delay=0):
    iterations = 1

    row_num, col_num = self.getInitialPos()
    current = Node(self.problem, row_num, col_num, None)
    stack = []
    saved = [current]
    init = time.time()

    
    while not current.isGoal():
      iterations+=1
      oldRow, oldCol = current.getState()
      await sleep(delay)
      choices = current.getChoices()
      choices = [Node(self.problem, choice[0], choice[1], current) for choice in choices]
      choices = list(filter(lambda choice: not self.isSaved(saved,choice), choices ))
      for choice in choices:
        saved.append(choice) 
        stack.append(choice)

      current = stack.pop()
      new_row, new_col = current.getState()
      path = []
      if(current.isGoal()): path = current.getPathToStart()

      await onIteration(
        {
          "row":new_row,
          "col": new_col,
          "oldRow": oldRow,
          "oldCol": oldCol,
          "finished": current.isGoal(),
          "path": path,
          "visited": len(saved),
          "left": len(stack),
          "iterations": iterations,
          "time": (time.time() - init),
          "choices": [choice.getState() for choice in choices],
          "current_depth": current.getDepth()
        }
      )
  async def startLinearBest(self, onIteration, delay=0):
    iterations = 1

    row_num, col_num = self.getInitialPos()
    current = Node(self.problem, row_num, col_num, None) #Setting first iteration with node as initial positicion
    stack = []
    saved = [current]
    init = time.time()

    while not current.isGoal():
      iterations+=1
      oldRow, oldCol = current.getState()
      await sleep(delay)
      choices = current.getOrderedChoicesByDistanceTo(self.goalRow, self.goalCol)
      choices = [Node(self.problem, choice[0], choice[1], current) for choice in choices]
      choices = list(filter(lambda choice: not self.isSaved(saved,choice), choices ))
      for choice in choices:
        saved.append(choice) 
        stack.append(choice)
      current = stack.pop()
      new_row, new_col = current.getState()
      path = []
      if(current.isGoal()): path = current.getPathToStart()
      await onIteration(
        {
          "row":new_row,
          "col": new_col,
          "oldRow": oldRow,
          "oldCol": oldCol,
          "finished": current.isGoal(),
          "path": path,
          "visited": len(saved),
          "left": len(stack),
          "iterations": iterations,
          "time": time.time() - init,
          "choices": [choice.getState() for choice in choices],
          "current_depth": current.getDepth()
        }
      )



    ### BREADTH FIRST SEARCH
  async def startLinearBreadth(self, onIteration, delay=0):
    iterations = 1
    row_num, col_num = self.getInitialPos()
    current = Node(self.problem, row_num, col_num, None)
    queue = []
    saved = [current]
    init = time.time()



    while not current.isGoal():
      iterations+=1
      oldRow, oldCol = current.getState()
      await sleep(delay)
      choices = current.getChoices()
      choices = [Node(self.problem, choice[0], choice[1], current) for choice in choices]
      choices = list(filter(lambda choice: not self.isSaved(saved,choice), choices ))
      for choice in choices:
        saved.append(choice) 
        queue.append(choice)

      current = queue.pop(0)
      new_row, new_col = current.getState()
      path = []
      if(current.isGoal()): path = current.getPathToStart()

      await onIteration(
        {
          "row":new_row,
          "col": new_col,
          "oldRow": oldRow,
          "oldCol": oldCol,
          "finished": current.isGoal(),
          "path": path,
          "visited": len(saved),
          "left": len(queue),
          "iterations": iterations,
          "time": time.time() - init,
          "choices": [choice.getState() for choice in choices],
          "current_depth": current.getDepth()
        }
      )

  async def startDepth(self, onIteration, delay,):
    return await self.startLinearDepth( onIteration, delay)
  
  async def startBest(self, onIteration, delay,):
    return await self.startLinearBest( onIteration, delay)
  
  async def startBreadth(self, onIteration, delay,):
    return await self.startLinearBreadth( onIteration, delay)
