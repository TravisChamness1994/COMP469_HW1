# Travis Chamness
# DFS Puzzle Solution by Graph Mode
# Sept 20th 2021
#TODO - implement to allow user to add their own Goal
GOAL = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

#Taken from Lab 3
class Node:
    def __init__(self, state, movement, parent):
        self.parent = parent
        self.neighbors = [] # Neighbors from this current state of the graph
        self.state = state # Puzzle at this current state
        self.movement = movement # The movement up, left, down, or right
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
        newNode = Node(self.state, self.movement, self.parent)
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
            if o.state.shape() == self.state.shape():
                return self.compare_state(o.state) and self.neighbors == o.neighbors and self.parent.compare_state(o.parent.state)
            else:
                return False



#Reads puzzle from file or user
def create_puzzle():
    #For user specified puzzle
    # maze_name = input("Enter puzzle name(Example - puzzle.txt): ")
    #For Hardcoded puzzle use
    maze_name = "puzzle1.txt"
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



def dfs_solution(puzzle):
    find_start = True
    start = print_puzzle_id_start(puzzle, find_start)
    print("Start Location: ",start)
    path = []
    closed = []
    head = Node(puzzle, None, None) #initialized head on Fringe
    goalFound = False
    currentNode = None
    fringe = [head]
    while not goalFound and fringe:
        currentNode = fringe.pop()
        goalFound = currentNode.goal_test()
        print(print_puzzle_id_start(currentNode.state))
        if not goalFound:
            #successor function
            #append to fringe
dfs_solution(create_puzzle())
