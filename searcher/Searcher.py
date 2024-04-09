from searcher.Node import Node
from asyncio import sleep
import json
class Searcher:
  def __init__(self, problem):
    self.problem = problem

  def getInitialPos(self):
    print(self.problem)
    for row_num, row in enumerate(self.problem):
      if 'i' in row:
        col_num = row.index('i')
        return [row_num, col_num]
    return 0

  def isSaved(self, saved, state):
    for old in saved:
      if old[0] == state[0] and old[1] == state[1]: return True
    return False

  async def startLinearDepth(self, onIteration, delay=0.2):
    stack = []
    saved = []
    
    row_num, col_num = self.getInitialPos()

    current = Node(self.problem, row_num, col_num, None)
    while not current.isGoal():
      oldRow, oldCol = current.getState()
      saved.append( current.getState()) 
      await sleep(delay)
      for choice in current.getChoices():
        if not self.isSaved(saved,choice) : stack.append(choice)
      new_row, new_col = stack.pop()
      current = Node(self.problem, new_row, new_col, current)
      await onIteration(json.dumps({"row":new_row, "col": new_col, "oldRow": oldRow , "oldCol": oldCol, "finished": current.isGoal()}),)

  async def startDepth(self, onIteration, delay):
    return await self.startLinearDepth( onIteration, delay)