from src.python.direction import *
from src.python.pos import Pos
from src.python.grid import Grid
from src.python.cell import Cell

# The function you'll implement for your bot! The default code here
# simply has `MyBot` stupidly chase fruit--not even checking to
# see if the cell it wants to go into is free.
"""
Modes:
 Findfood
  When safe && time < half && fruit exists && inseficent blocking length
 Run
  Not Safe && Exit Avalible
 Trapped
  Not Safe && Exit Unavalible
 Block
  When safe && Seficent Blocking Length
 Hunt
  When safe && time > half && Inseficent blocking length

Variables:
 Blocking length = other length * 1.5
 Safty = bfs length > 8

Functions:
 find area of other
 BFS?
"""

def my_bot_think(grid):
  fruits = grid.find_fruits()
  self_head = grid.find_self_head()
  body = grid.find_self_positions()
  other_head = grid.find_other_head()
  other = grid.find_other_positions()

  time = grid.get_current_tick()
  halfTime = 150

  is_there_fruit = len(fruits) > 0
  Safty = Safty(self_head)
  #safty = greater than a forth of blocks avablile

  BlockingLength = (len(other)*1.5)
  isSeficent = len(body) >= BlockingLength

  BestDir = Direction.UP
  
  if(Safty and time < halfTime and is_there_fruit and not isSeficent):
    BestDir = FindFood(fruits, self_head)
  elif(Safty and isSeficent):
    BestDir = Block(self_head, body, other_head, other)
  elif(Safty and time >= halfTime and isSeficent):
    BestDir = Hunt(other_head, self_head)
  else:
    BestDir = Run(self_head, body, other_head, other)


  return BestDir

def Safty(head):
  SaftyBlocks = bfsSafty(self_head)
  gridSize = (Grid.get_width(), Grid.get_height())
  Safty = SaftyBlocks > (gridSize[0]*gridSize[1]/4)
  return Safty


def bfsSafty(head):
  saftyBlocks = []
  Q = [head]

  while(len(Q) > 0):
    if Q[0] not in saftyBlocks:
      for dire in Direction:
        place = Q[0].with_dir(dire)
        Q.append(place)
        if isSafe(Q[0]):
          saftyBlocks.append(Q[0])

    Q.pop(0)

  return len(saftyBlocks)

def isSafe(place):
  if (grid.get_from_pos(place) == Cell.EMPTY) or (grid.get_from_pos(place) == Cell.FRUIT):
    return True
  return False

def SaftyChase(target, head):
  ClosestDir = chase(head, target)
  safeDirections = []
  for dire in Direction:
    temp = head.with_dir(dire)
    if isSafe(temp):
      if Safty(temp):
        safeDirections.append(dire)

  if(len(safeDirections)>0):
    for dire in ClosestDir:
      if dire in safeDirections:
        return dire
    return saftyDirections[0]
  return Direction.UP

def chase(chaser, thing):
  distX = abs(chaser.x-thing.x)
  distY = abs(chaser.y-thing.y)
  ClosestDir = (Direction.UP,Direction.UP)

  if distX > distY:
    if thing.x < chaser.x:
      ClosestDir[0] = Direction.LEFT
    else:
      ClosestDir[0] = Direction.RIGHT
    
    if thing.y < chaser.y:
      ClosestDir[1] = Direction.DOWN
    else:
      ClosestDir[1] = Direction.UP
  else:
    if thing.y < chaser.y:
      ClosestDir[0] = Direction.DOWN
    else:
      ClosestDir[0] = Direction.UP
    
    if thing.x < chaser.x:
      ClosestDir[1] = Direction.LEFT
    else:
      ClosestDir[1] = Direction.RIGHT
  
  return ClosestDir
    

def FindFood(fruits, head):
  closestFruit = fruits[0]
  closeset = Grid.get_width()
  for fruit in fruits:
      closeness = (abs(head.x-fruit.x)+abs(head.y-fruit.y))
      if closeness < closeset:
        closestFruit = fruit
    
  zoningMax = int((Grid.get_width())/10)
  if (abs(head.x-closestFruit.x)+abs(head.y-closestFruit.y)) > zoningMax:
    fruitRichArea = closestFruit
    MaxAround = 0
    for fruit in fruits:
      counting = 0
      for fruit2 in fruits:
        if (fruit2 is not fruit) and ((abs(fruit2.x-fruit.x)+abs(fruit2.y-fruit.y)) < zoningMax):
          counting =+ 1
      if counting > MaxAround:
        MaxAround = counting
        fruitRichArea = fruit
    closestFruit = fruitRichArea

  return SaftyChase(closestFruit, head)

def Block(self_head, body, other_head, other):
  otherLeft = other_head.x
  otherRight = other_head.x
  otherUp = other_head.y
  otherDown = other_head.y
  for part in other:
    if part.x > otherRight:
      otherRight = part.x
    if part.x < otherLeft:
      otherLeft = part.x
    if part.y > otherUp:
      otherUp = part.y
    if part.y < otherDown:
      otherDown = part.y

  selfLeft = self_head.x
  selfRight = self_head.x
  selfUp = self_head.y
  selfDown = self_head.y
  for part in other:
    if part.x > selfRight:
      selfRight = part.x
    if part.x < selfLeft:
      selfLeft = part.x
    if part.y > selfUp:
      selfUp = part.y
    if part.y < selfDown:
      selfDown = part.y
  
  LeftNeeded = selfLeft - otherLeft
  RightNeeded = otherRight - selfRight
  UpNeeded = otherUp - selfUp
  DownNeeded = selfDown - otherDown

  Target = head
  if (LeftNeeded > RightNeeded) and (LeftNeeded > 0):
    Target.x -= LeftNeeded
  elif (RightNeeded > LeftNeeded) and (RightNeeded > 0):
    Target.x += RightNeeded
  
  if (DownNeeded > UpNeeded) and (DownNeeded > 0):
    Target.x -= DownNeeded
  elif (UpNeeded > DownNeeded) and (UpNeeded > 0):
    Target.x += UpNeeded

  if target == head:
    return Run(self_head, body, other_head, other)
  else:
    return SaftyChase(Target, head)

def Hunt(other_head, self_head):
  return SaftyChase(other_head, self_head)

def Run(self_head, body, other_head, other):
  distdirx = other.x - head.x
  distdiry = other.y - head.y
  if Safty(head):
    target = head
    target.y -= other.y
    target.x -= other.x
    return SaftyChase(target, head)
  
  saftDirections = []
  for dire in Direction:
    if isSafe(head.with_dir(dire)):
      saftDirections.append(dire)
  
  if (len(saftDirections) == 0):
    return Direction.UP

  saferDirections = []
  for dire in saftDirections:
    part = head.with_dir(dire)
    for direc in Direction:
      if isSafe(part.with_dir(dire)):
        saferDirections.append(dire)
  
  if (len(saferDirections)==0):
    return saftDirections[0]
  else:
    bestDir = saferDirections[0]
    totalOp = 4
    for dire in saferDirections:
      count = 0
      for direc in Direction:
        if isSafe(head.with_dir(dire).with_dir(direc)):
          count +=1
      
      if count < totalOp:
        totalOp = count
        bestDir = dire
    return bestDir
  
  return Direction.UP