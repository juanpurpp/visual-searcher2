from searcher.Node import Node
from asyncio import sleep
import json
class Searcher:
  def __init__(self, problem):
    self.problem = problem

  def getInitialPos(self):
    for row_num, row in enumerate(self.problem):
      if 'i' in row:
        col_num = row.index('i')
        return [row_num, col_num]
    return 0

  def isSaved(self, saved, state):
    for old in saved:
      if old.getState() == state.getState(): return True
    return False

  async def startLinearDepth(self, onIteration, delay=0.2):
    stack = []
    saved = []
    
    row_num, col_num = self.getInitialPos()

    current = Node(self.problem, row_num, col_num, None)
    while not current.isGoal():
      oldRow, oldCol = current.getState()
      saved.append( current) 
      await sleep(delay)
      for choice in current.getChoices():
        new_node = Node(self.problem, choice[0], choice[1], current)
        if not self.isSaved(saved,new_node) : stack.append(new_node)
      current = stack.pop()
      new_row, new_col = current.getState()
      path = []
      if(current.isGoal()): path = current.getPathToStart()

      await onIteration(json.dumps({"row":new_row, "col": new_col, "oldRow": oldRow , "oldCol": oldCol, "finished": current.isGoal(), "path": path}),)

  async def startDepth(self, onIteration, delay):
    return await self.startLinearDepth( onIteration, delay)