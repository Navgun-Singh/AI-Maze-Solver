# IMPORT AREA
from PIL import Image, ImageDraw



# CLASSES & FUNCTIONS AREA
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action



# DFS
class StackFrontier():
    def __init__(self):
        self.frontier = []  

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier) 
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node



# BFS 
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node



# MAIN MAZE AND IT's PICTURE PRODUCTION      
class Maze():
    def __init__(self, filename):
        
        with open(filename) as f:
            contents = f.read()
        
        if contents.count('2') != 1:
            raise Exception("No Starting Point")
        if contents.count('3') != 1:
            raise Exception("No Ending Point")
        
        # HEIGHT AND WIDTH
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # WALLS
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "2":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "3":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == "0":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None
    
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("|", end="")
                elif (i, j) == self.start:
                    print("2", end="")
                elif (i, j) == self.goal:
                    print("3", end="")
                elif solution is not None and (i, j) in solution:
                    print("#", end="")
                else:
                    print(" ", end="")
            print()
        print()

    
    def neighbors(self, state):
        row, col = state

        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]

        result = []
        for action, (r,c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r,c)))
            except IndexError:
                continue
        return result

    def solve(self):

        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)

        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("No Solution")
            
            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def save_solution_image(self, cell_size=20, output_file="maze_solution.png"):
        img_width = self.width * cell_size
        img_height = self.height * cell_size
        image = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(image)

        for i in range(self.height):
            for j in range(self.width):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if self.walls[i][j]:
                    color = "black"
                elif (i, j) == self.start:
                    color = "green"
                elif (i, j) == self.goal:
                    color = "red"
                elif self.solution and (i, j) in self.solution[1]:
                    color = "blue"
                else:
                    color = "white"
                
                draw.rectangle([x1, y1, x2, y2], fill=color)

        image.save(output_file)
        print(f"Solution image saved to {output_file}")



# COMMANDS
m = Maze(input("Enter the Maze File Path: "))
print("Maze: ")
m.print()
print("Solving")
m.solve()
print("States Explored: ", m.num_explored)
print("Solution:")
m.print()
m.save_solution_image()

