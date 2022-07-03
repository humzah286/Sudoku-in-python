#Sudoku Generator Algorithm - www.101computing.net/sudoku-generator-algorithm/
from random import randint, shuffle
from time import sleep


# global counter
# counter = 0
#initialise empty 9 by 9 grid
# grid = [ [0 for c in range(0,9)] for r in range(0, 9) ]

#A function to check if the grid is full
def checkGrid(grid):
  for row in range(0,9):
      for col in range(0,9):
        if grid[row][col]==0:
          return False

  #We have a complete grid!  
  return True 

#A backtracking/recursive function to check all possible combinations of numbers until a solution is found
def solveGrid(grid, counter):
  # global counter
  #Find next empty cell
  for i in range(0,81):
    row=i//9
    col=i%9
    if grid[row][col]==0:
      for value in range (1,10):
        #Check that this value has not already be used on this row
        if not(value in grid[row]):
          #Check that this value has not already be used on this column
          if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
            #Identify which of the 9 squares we are working on
            square=[]
            if row<3:
              if col<3:
                square=[grid[i][0:3] for i in range(0,3)]
              elif col<6:
                square=[grid[i][3:6] for i in range(0,3)]
              else:  
                square=[grid[i][6:9] for i in range(0,3)]
            elif row<6:
              if col<3:
                square=[grid[i][0:3] for i in range(3,6)]
              elif col<6:
                square=[grid[i][3:6] for i in range(3,6)]
              else:  
                square=[grid[i][6:9] for i in range(3,6)]
            else:
              if col<3:
                square=[grid[i][0:3] for i in range(6,9)]
              elif col<6:
                square=[grid[i][3:6] for i in range(6,9)]
              else:  
                square=[grid[i][6:9] for i in range(6,9)]
            #Check that this value has not already be used on this 3x3 square
            if not value in (square[0] + square[1] + square[2]):
              grid[row][col]=value
              if checkGrid(grid):
                counter[0] += 1
                # print("counter = ", str(counter)) 
                break
              else:
                if solveGrid(grid, counter):
                  return True
      break
  grid[row][col]=0  

numberList=[1,2,3,4,5,6,7,8,9]
#shuffle(numberList)

#A backtracking/recursive function to check all possible combinations of numbers until a solution is found
def fillGrid(grid):
  # global counter
  #Find next empty cell
  for i in range(0,81):
    row=i//9
    col=i%9
    if grid[row][col]==0:
      shuffle(numberList)      
      for value in numberList:
        #Check that this value has not already be used on this row
        if not(value in grid[row]):
          #Check that this value has not already be used on this column
          if not value in (grid[0][col],grid[1][col],grid[2][col],grid[3][col],grid[4][col],grid[5][col],grid[6][col],grid[7][col],grid[8][col]):
            #Identify which of the 9 squares we are working on
            square=[]
            if row<3:
              if col<3:
                square=[grid[i][0:3] for i in range(0,3)]
              elif col<6:
                square=[grid[i][3:6] for i in range(0,3)]
              else:  
                square=[grid[i][6:9] for i in range(0,3)]
            elif row<6:
              if col<3:
                square=[grid[i][0:3] for i in range(3,6)]
              elif col<6:
                square=[grid[i][3:6] for i in range(3,6)]
              else:  
                square=[grid[i][6:9] for i in range(3,6)]
            else:
              if col<3:
                square=[grid[i][0:3] for i in range(6,9)]
              elif col<6:
                square=[grid[i][3:6] for i in range(6,9)]
              else:  
                square=[grid[i][6:9] for i in range(6,9)]
            #Check that this value has not already be used on this 3x3 square
            if not value in (square[0] + square[1] + square[2]):
              grid[row][col]=value
              if checkGrid(grid):
                return True
              else:
                if fillGrid(grid):
                  return True
      break
  grid[row][col]=0             
    
#Generate a Fully Solved Grid

# fillGrid(grid)


# print(" complete grid :: ")
# for line in grid: print(line)



#Start Removing Numbers one by one
#A higher number of attempts will end up removing more numbers from the grid
#Potentially resulting in more difficiult grids to solve!

def generate_puzzle(grid1 ,a):
  counter = [0]
  attempts = a
  counter[0] = 1
  while attempts>0:
    # print("in loop ")
    #Select a random cell that is not already empty
    row = randint(0,8)
    col = randint(0,8)
    while grid1[row][col]==0:
      row = randint(0,8)
      col = randint(0,8)
    #Remember its cell value in case we need to put it back  
    backup = grid1[row][col]
    grid1[row][col]=0
    # print("grid 1 = ")
    # for line in grid1: print(line)
    
    #Take a full copy of the grid1
    copyGrid = []
    for r in range(0,9):
      copyGrid.append([])
      for c in range(0,9):
          copyGrid[r].append(grid1[r][c])
    
    #Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
    counter[0]=0      
    solveGrid(copyGrid, counter)  
    # print("counter = ", str(counter)) 
    #If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
    if counter[0]!=1:
      grid1[row][col]=backup
      #We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
      attempts -= 1
      
  return grid1

# print(" puzzle grid :: ")
# for line in grid: print(line)

# print("Sudoku Grid Ready")

# solution = [ [0 for c in range(0,9)] for r in range(0, 9) ]
# # puzzle = []

# fillGrid(solution)

# print("solution :: ")
# for line in solution: print(line)

# temp = [ [0 for c in range(0,9)] for r in range(0, 9) ]

# for i in range(0,9): 
#   for j in range(0, 9): temp[i][j] = solution[i][j]

# puzzle = generate_puzzle(solution, 5)

# print("solution :: ")
# for line in temp: print(line)

# print("puzzle :: ")
# for line in puzzle: print(line)