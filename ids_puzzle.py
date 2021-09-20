# Travis Chamness
# IDS Puzzle Solution by Graph Mode
# Sept 20th 2021
GOAL = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
ROW = 0
COL = 1
MIN_DIMENSION = 0
MAX_DIMENSION = 2

class Node:
    def __init__(self, state, start, parent, movement, depth):
        self.parent = parent
        self.location = start
        self.neighbors = [] # Neighbors from this current state of the graph
        self.state = state # Puzzle at this current state
        self.movement = movement # Movement in the puzzle resulting in the state
        self.depth = depth # Current depth of the branch
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
        newNode = Node(self.state, self.location, self.parent, self.movement, self.depth)
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
    maze_name = "puzzle3.txt"
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
    # Optionally return the start location, defaults as off
    if find_start:
        return start
    else:
        return ''

def dfs_successor_func(currentNode):
    copyLocation = currentNode.location.copy()
    copyState = [row[:] for row in currentNode.state]
    #Order reversal of Operation that mimics the stack for U, L, D, R order
    #Right
    if copyLocation[COL] != MAX_DIMENSION:
        temp = copyState[copyLocation[ROW]][copyLocation[COL]+1]
        copyState[copyLocation[ROW]][copyLocation[COL]+1] = copyState[copyLocation[ROW]][copyLocation[COL]]
        copyState[copyLocation[ROW]][copyLocation[COL]] = temp
        copyLocation[COL] += 1
        newNode = Node(copyState, copyLocation, currentNode, 'R', currentNode.depth + 1)
        currentNode.neighbors.append(newNode)
    #Down
    copyLocation = currentNode.location.copy()
    copyState = [row[:] for row in currentNode.state]
    if copyLocation[ROW] != MAX_DIMENSION:
        temp = copyState[copyLocation[ROW] + 1][copyLocation[COL]]
        copyState[copyLocation[ROW]+1][copyLocation[COL]] = copyState[copyLocation[ROW]][copyLocation[COL]]
        copyState[copyLocation[ROW]][copyLocation[COL]] = temp
        copyLocation[ROW] += 1
        newNode = Node(copyState, copyLocation, currentNode, 'D', currentNode.depth + 1)
        currentNode.neighbors.append(newNode)
    #Left
    copyLocation = currentNode.location.copy()
    copyState = [row[:] for row in currentNode.state]
    if copyLocation[COL] != MIN_DIMENSION:
        temp = copyState[copyLocation[ROW]][copyLocation[COL] - 1]
        copyState[copyLocation[ROW]][copyLocation[COL] - 1] = copyState[copyLocation[ROW]][copyLocation[COL]]
        copyState[copyLocation[ROW]][copyLocation[COL]] = temp
        copyLocation[COL]= copyLocation[COL] - 1
        newNode = Node(copyState, copyLocation, currentNode, 'L', currentNode.depth + 1)
        currentNode.neighbors.append(newNode)
    #UP
    copyLocation = currentNode.location.copy()
    copyState = [row[:] for row in currentNode.state]
    if copyLocation[ROW] != MIN_DIMENSION:
        temp = copyState[copyLocation[ROW] - 1][copyLocation[COL]]
        copyState[copyLocation[ROW]-1][copyLocation[COL]] = copyState[copyLocation[ROW]][copyLocation[COL]]
        copyState[copyLocation[ROW]][copyLocation[COL]] = temp
        copyLocation[ROW] = copyLocation[ROW] - 1
        newNode = Node(copyState, copyLocation, currentNode, 'U', currentNode.depth + 1)
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

def dls_solution(puzzle, limit):
    find_start = True
    goalFound = False
    start = print_puzzle_id_start(puzzle, find_start)
    print("\nStart Location:",start)
    path = []
    closed = []
    head = Node(puzzle, start, None, None, 0) #initialized head on Fringe
    currentNode = None
    fringe = [head]
    while not goalFound and fringe:
        in_closed = False
        currentNode = fringe.pop()
        goalFound = currentNode.goal_test()
        print("{} \nNodeDepth: {}".format(print_puzzle_id_start(currentNode.state), currentNode.depth))
        in_closed = not_in_closed(currentNode, closed)
        if not goalFound and currentNode.depth < limit and not in_closed:
            closed.append(currentNode)
            currentNode = dfs_successor_func(currentNode)
            fringe = append_to_fringe(fringe, currentNode)
        elif goalFound:
            path = populate_path(currentNode)
            #append to fringe
    print(path)
    return path

def dls_solution_wrapper(depth):
    path = []
    for i in range(depth):
        if not path:
            iterationDepth = i + 1
            path = dls_solution(create_puzzle(), iterationDepth)
        else: break
    return path, len(path) - 1

dls_solution(create_puzzle(), 3)
