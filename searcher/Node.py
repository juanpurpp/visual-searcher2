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

  def getDistanceFrom( self, targetRow, targetCol ):
    return (( ( self.row - targetRow)**2 ) + ( (self.col - targetCol)**2 )  )**0.5

  def getDistanceFrom (self, row, col, targetRow, targetCol):
    return (( ( row - targetRow )**2 ) + ( ( col - targetCol )**2 )  )**0.5
  
  def getOrderedChoicesByDistanceTo(self, targetRow, targetCol):
    row, col = self.getState()
    children = []
    up = [row - 1, col]
    right = [row, col +1]
    down = [row + 1, col]
    left = [row, col-1]
    #up
    if self.movementDoesntBreakRules(*up):
      this_choice_distance = self.getDistanceFrom(*up, targetRow, targetCol)
      inserted = False
      for index,listed in enumerate(children):
        if this_choice_distance > listed['distance']:
          children = children[:index] + [{"coords": up,"distance": this_choice_distance}]+ children[index:]
          inserted = True
      if len(children) == 0 or not inserted: children.append({"coords": up,"distance": this_choice_distance})
    #right
    if self.movementDoesntBreakRules(*right):
      inserted = False
      this_choice_distance = self.getDistanceFrom(*right, targetRow, targetCol)
      for index,listed in enumerate(children):
        if this_choice_distance > listed['distance']:
          children = children[:index] + [ {"coords": right,"distance": this_choice_distance}] + children[index:]
          inserted = True
      if len(children) == 0 or not inserted: children.append({"coords": right,"distance": this_choice_distance})
    #down
    if self.movementDoesntBreakRules(*down):
      inserted = False
      this_choice_distance = self.getDistanceFrom(*down, targetRow, targetCol)
      for index,listed in enumerate(children):
        if this_choice_distance > listed['distance']:
          children = children[:index] + [{"coords": down,"distance": this_choice_distance}] + children[index:]
          inserted = True
      if len(children) == 0 or not inserted: children.append({"coords": down,"distance": this_choice_distance})
    #left
    if self.movementDoesntBreakRules(*left):
      inserted = False
      this_choice_distance = self.getDistanceFrom(*left, targetRow, targetCol)
      for index,listed in enumerate(children):
        if this_choice_distance > listed['distance']:
          children = children[:index] + [{"coords": left,"distance": this_choice_distance}] + children[index:]
          inserted = True
      if len(children) == 0 or not inserted: children.append({"coords": left,"distance": this_choice_distance})

    children = list(map(lambda choice: choice['coords'], children))

    return children
    
  
  def getPathToStart(self):

    result = []
    current = self.getFather()
    while current is not None:
      result.append(current.getState())
      current = current.getFather()
    return result