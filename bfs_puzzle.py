# Travis Chamness
# BFS Puzzle Solution by Graph Mode
# Sept 20th 2021
#TODO - implement to allow user to add their own Goal.
GOAL = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
ROW = 0
COL = 1
MIN_DIMENSION = 0
MAX_DIMENSION = 2

#Taken from Lab 3
class Node:
    def __init__(self, state, start, parent, movement):
        self.parent = parent
        self.location = start
        self.neighbors = [] # Neighbors from this current state of the graph
        self.state = state # Puzzle at this current state
        self.movement = movement
    #utility for comparing nodes
    def compare_state(self, state):
        same = True
        for i, row in enumerate(self.state):
            if same:
                for j,val in enumerate(row):
                    if val != state[i][j]:
                        same = False
                        break
            else:
                break
        return same

    #Tests current state against the GOAL state
    def goal_test(self):
        return self.compare_state(GOAL)

    def copy(self):
        newNode = Node(self.state, self.location, self.parent, self.movement)
        return newNode
    # Compares two nodes for whether or not they are the same
    #   Does not consider the movement, because a movement may not have happened yet, and certainly should not happen again.'
    #   Also will not consider parent because the parent is irrelevant to the same state being found
    def compare(self, o):
        if o == None:
            return False
        elif o is self:
            return True
        else:
            return self.location == o.location and self.compare_state(o.state)

def not_in_closed(currentNode, closed):
    in_closed = False
    for node in closed:
        if in_closed:
            break
        else:
            in_closed = currentNode.compare(node)
    return in_closed
#Reads puzzle from file or user
def create_puzzle():
    #For user specified puzzle
    # maze_name = input("Enter puzzle name(Example - puzzle.txt): ")
    #For Hardcoded puzzle use
    # maze_name = "puzzle1.txt"
    # maze_name = "puzzle2.txt"
    # maze_name = "puzzle3.txt"
    maze_name = "puzzle4BFS.txt"

    file = open(maze_name, "r")
    lines = file.readlines()
    puzzle = []
    for line in lines:
        arr = []
        for character in line:
            if character != '\n':
                arr.append(int(character))
            else:
                break
        puzzle.append(arr)
    return puzzle

#prints the puzzle and identifies the starting position.
def print_puzzle_id_start(puzzle, find_start = False):
    for i, row in enumerate(puzzle): # Technical Row of the puzzle which is enumerated with identifier i
        print()
        for j, val in enumerate(row): # Technical Col of the puzzle which is enumerated with identifier j
            if val != '\n':
                if val  == 0:
                    print(" ", end=' ') #IDE says branch never entered?
                    start = [i,j] # Utilize the Row Column shape of the puzzle to describe the starting location with i,j
                else:
                    print(str(val), end=' ')
    print('\n')
    # Optionally return the start location, defaults as off
    if find_start:
        return start
    else:
        return ''

def bfs_successor_func(currentNode):
    #UP
    copyLocation = currentNode.location.copy()
    copyState = [row[:] for row in currentNode.state]
    if copyLocation[ROW] != MIN_DIMENSION:
        temp = copyState[copyLocation[ROW] - 1][copyLocation[COL]]
        copyState[copyLocation[ROW]-1][copyLocation[COL]] = copyState[copyLocation[ROW]][copyLocation[COL]]
        copyState[copyLocation[ROW]][copyLocation[COL]] = temp
        copyLocation[ROW] = copyLocation[ROW] - 1
        newNode = Node(copyState, copyLocation, currentNode, 'U')
        currentNode.neighbors.append(newNode)
    #Left
    copyLocation = currentNode.location.copy()
    copyState = [row[:] for row in currentNode.state]
    if copyLocation[COL] != MIN_DIMENSION:
        temp = copyState[copyLocation[ROW]][copyLocation[COL] - 1]
        copyState[copyLocation[ROW]][copyLocation[COL] - 1] = copyState[copyLocation[ROW]][copyLocation[COL]]
        copyState[copyLocation[ROW]][copyLocation[COL]] = temp
        copyLocation[COL]= copyLocation[COL] - 1
        newNode = Node(copyState, copyLocation, currentNode, 'L')
        currentNode.neighbors.append(newNode)
     #Down
    copyLocation = currentNode.location.copy()
    copyState = [row[:] for row in currentNode.state]
    if copyLocation[ROW] != MAX_DIMENSION:
        temp = copyState[copyLocation[ROW] + 1][copyLocation[COL]]
        copyState[copyLocation[ROW]+1][copyLocation[COL]] = copyState[copyLocation[ROW]][copyLocation[COL]]
        copyState[copyLocation[ROW]][copyLocation[COL]] = temp
        copyLocation[ROW] += 1
        newNode = Node(copyState, copyLocation, currentNode, 'D')
        currentNode.neighbors.append(newNode)
    #Right
    if copyLocation[COL] != MAX_DIMENSION:
        temp = copyState[copyLocation[ROW]][copyLocation[COL]+1]
        copyState[copyLocation[ROW]][copyLocation[COL]+1] = copyState[copyLocation[ROW]][copyLocation[COL]]
        copyState[copyLocation[ROW]][copyLocation[COL]] = temp
        copyLocation[COL] += 1
        newNode = Node(copyState, copyLocation, currentNode, 'R')
        currentNode.neighbors.append(newNode)

    return currentNode

def populate_path(node):
    path = []
    currentNode = node.copy()
    while currentNode != None:
        path.insert(0, currentNode.movement)
        currentNode = currentNode.parent
    return path

def append_to_fringe(fringe, currentNode):
    for node in currentNode.neighbors:
        fringe.append(node.copy())
    return fringe

def bfs_solution(puzzle):
    find_start = True
    goalFound = False
    start = print_puzzle_id_start(puzzle, find_start)
    path = []
    closed = []
    currentNode = None
    head = Node(puzzle, start, None, None)
    fringe = [head]
    iteration = 0
    while not goalFound and fringe:
        iteration += 1
        in_closed = False
        #Dequeue the 0th place node from the fringe
        currentNode = fringe.pop(0)
        #Test the current node state against the goal state
        goalFound = currentNode.goal_test()
        print(print_puzzle_id_start(currentNode.state))
        #Determine if the current node is in the closed set
        in_closed = not_in_closed(currentNode, closed)
        if not goalFound and not in_closed:
            closed.append(currentNode)
            currentNode = bfs_successor_func(currentNode)
            fringe = append_to_fringe(fringe, currentNode)
        elif goalFound:
            path = populate_path(currentNode)
        print(iteration)
    print(path)
    return path

bfs_solution(create_puzzle())



