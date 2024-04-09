class Node:
  def __init__(self, problem, row, col, father):
    self.problem = problem
    self.row = row
    self.col = col
    self.father = father

  def getState(self):
    return [self.row, self.col]
  
  def getFather(self):
    return self.father
  
  def movementDoesntBreakRules(self, newRow, newCol):
    if newRow < 0: return False
    if newCol < 0: return False
    if newRow >= len(self.problem): return False
    if newCol >= len(self.problem[0]): return False
    if self.problem[newRow][newCol] == 0: return False
    return True
  
  def getChoices(self):
    row, col = self.getState()
    children = []
    #up
    if self.movementDoesntBreakRules(row - 1, col):
      children.append(([row -1, col]))
    #right
    if self.movementDoesntBreakRules(row, col+1):
      children.append(([row, col+1]))
    #down
    if self.movementDoesntBreakRules(row + 1, col):
      children.append(([row + 1, col]))
    #left
    if self.movementDoesntBreakRules(row, col-1):
      children.append(([row, col-1]))
    return children
  
  def isGoal(self):
    row, col = self.getState()
    if self.problem[row][col] == 'g': return True
    else: return False

  def getPathToStart(self):

    result = []
    current = self.getFather()
    while current is not None:
      result.append(current.getState())
      current = current.getFather()
    return result