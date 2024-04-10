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
      old_state = old.getState()
      state_state = state.getState()
      if old_state[0] == state_state[0] and old_state[1] == state_state[1]: return True
    return False

  async def startLinearDepth(self, onIteration, delay=0.2):
    iterations = 0
    stack = []
    saved = []
    init = time.time()
    row_num, col_num = self.getInitialPos()

    current = Node(self.problem, row_num, col_num, None)
    while not current.isGoal():
      iterations+=1
      oldRow, oldCol = current.getState()
      await sleep(delay)
      for choice in current.getChoices():
        new_node = Node(self.problem, choice[0], choice[1], current)
        if not self.isSaved(saved,new_node) :
          saved.append(new_node) 
          stack.append(new_node)
      current = stack.pop()
      new_row, new_col = current.getState()
      path = []
      if(current.isGoal()): path = current.getPathToStart()

      await onIteration(
        json.dumps(
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
          }
        )
      )
  async def startLinearBest(self, onIteration, delay=0.2):
    iterations = 0
    stack = []
    saved = []
    init = time.time()
    row_num, col_num = self.getInitialPos()

    current = Node(self.problem, row_num, col_num, None)
    while not current.isGoal():
      iterations+=1
      oldRow, oldCol = current.getState()
      await sleep(delay)
      for choice in current.getOrderedChoicesByDistanceTo(self.goalRow, self.goalCol):
        new_node = Node(self.problem, choice[0], choice[1], current)
        if not self.isSaved(saved,new_node) :
          saved.append(new_node) 
          stack.append(new_node)
      current = stack.pop()
      new_row, new_col = current.getState()
      path = []
      if(current.isGoal()): path = current.getPathToStart()
      await onIteration(
        json.dumps(
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
          }
        )
      )



    ### BREADTH FIRST SEARCH
  async def startLinearBreadth(self, onIteration, delay=0.2):
    iterations = 0
    queue = []
    saved = []
    init = time.time()
    row_num, col_num = self.getInitialPos()

    current = Node(self.problem, row_num, col_num, None)
    while not current.isGoal():
      iterations+=1
      oldRow, oldCol = current.getState()
      await sleep(delay)
      for choice in current.getChoices():
        new_node = Node(self.problem, choice[0], choice[1], current)
        if not self.isSaved(saved,new_node): 
          saved.append(new_node) 
          queue.append(new_node)

      current = queue.pop(0)
      new_row, new_col = current.getState()
      path = []
      if(current.isGoal()): path = current.getPathToStart()

      await onIteration(
        json.dumps(
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
          }
        )
      )

  async def startDepth(self, onIteration, delay,):
    return await self.startLinearDepth( onIteration, delay)
  
  async def startBest(self, onIteration, delay,):
    return await self.startLinearBest( onIteration, delay)
  
  async def startBreadth(self, onIteration, delay,):
    return await self.startLinearBreadth( onIteration, delay)
