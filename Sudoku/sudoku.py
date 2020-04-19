import math
import random
import copy

#method print_grid() from https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python
#Basic print of grid
def print_grid(grid):
    #for row in grid:
    #    print(row)

    root = int(math.sqrt(len(grid)))
    square_num = len(grid)

    def expandLine(line):
        return line[0] + line[5:9].join([line[1:5] * (root - 1)] * root) + line[9:13]

    line0  = expandLine("╔═══╤═══╦═══╗")
    line1  = expandLine("║ . │ . ║ . ║")
    line2  = expandLine("╟───┼───╫───╢")
    line3  = expandLine("╠═══╪═══╬═══╣")
    line4  = expandLine("╚═══╧═══╩═══╝")

    symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #symbol = list(" ")
    #symbol = symbol + list(range(1, len(grid) + 1))

    nums   = [ [""] + [str(symbol[n]) for n in row] for row in grid ]
    print(line0)
    for r in range(1, square_num + 1):
        print( "".join(n + s for n, s in zip(nums[r - 1], line1.split("."))) )
        print([line2, line3, line4][(r % square_num == 0) + (r % root == 0)])


#Test whether value is possible
#Test same row and column for duplicate value
#Test same block for duplicate value
def possible(row, col, test_num, grid):
    for j in range(square_num):
        if grid[row][j] == test_num:
            return False
    for i in range(square_num):
        if grid[i][col] == test_num:
            return False
    y = row // root * root
    x = col // root * root
    for i in range(root):
        for j in range(root):
            if grid[y + i][x + j] == test_num:
                return False
    return True


class Grid:
    def __init__(self, difficulty, square_num, root):
        self.grid = [ [0 for i in range(square_num)] for j in range(square_num) ]
        self.square_num = square_num
        self.root = root
        self.difficulty = difficulty
        self.solution_count = 0
        self.missing_nums = 0
        self.multi_sol = False
        self.solve_grid = []
        self.wrong_attemps = 0
        self.grid_store = []
        self.context = "Generate"

    def solve(self):
        for i in range(self.square_num):
            for j in range(self.square_num):        
                possible_nums = list(range(1, self.square_num + 1))
                if self.grid[i][j] == 0:
                    while len(possible_nums) > 0:
                        test_num = random.sample(possible_nums, 1)[0]
                        if possible(i, j, test_num, self.grid):
                            self.grid[i][j] = test_num
                            self.solve()
                            if self.multi_sol:
                                return
                            self.grid[i][j] = 0
                        possible_nums.remove(test_num)
                    return
        self.solution_count = self.solution_count + 1
        if self.solution_count == 1 and self.context == "Generate" or self.solution_count > 1:
            self.multi_sol = True

    def new_puzzle(self):
        self.context = "Puzzle"
        self.grid_store = copy.deepcopy(self.grid)
        enum_grid = list(range(self.square_num ** 2))
        self.solution_count = 0
        self.solved_grid = copy.deepcopy(self.grid)

        if self.difficulty == "Beginner":
            thres = self.square_num * 5
        elif self.difficulty == "Easy":
            thres = self.square_num * 4
        elif self.difficulty == "Medium":
            thres = self.square_num * 3
        elif self.difficulty == "Hard":
            thres = self.square_num * 2
        elif self.difficulty == "Fiendish":
            thres = self.square_num * 1
        
        print("Generating Puzzle...")

        while len(enum_grid) > thres:
            #print(len(enum_grid), thres)
            self.solution_count = 0
            while self.solution_count <= 1:
                self.solution_count = 0
                enum_to_remove = random.sample(enum_grid, 1)[0]
                enum_grid.remove(enum_to_remove)
                row_store = enum_to_remove // self.square_num
                last_store = self.solved_grid[row_store][enum_to_remove - row_store * self.square_num]
                self.solved_grid[row_store][enum_to_remove - row_store * self.square_num] = 0
                self.grid = copy.deepcopy(self.solved_grid)
                self.solve()
                self.multi_sol = False
            self.solved_grid[row_store][enum_to_remove - row_store * self.square_num] = last_store
            self.solution_count = 0
            self.grid[row_store][enum_to_remove - row_store * self.square_num] = last_store

        for row in self.solved_grid:
            for col in row:
                if col == 0:
                    self.missing_nums = self.missing_nums + 1
        print_grid(self.solved_grid)
        self.context = "Generate"

    def add_num(self):
        while self.missing_nums > 0:
            row = int(input("Enter Row (1-9): "))
            col = int(input("Enter Column (1-9): "))
            if self.solved_grid[row - 1][col - 1] != 0:
                print("Entry Already Set.")
                continue
            input_num = int(input("Enter Guess: "))
            if self.grid_store[row - 1][col - 1] == input_num:
                self.solved_grid[row - 1][col - 1] = input_num
                print("Correct Guess!")
                print_grid(self.solved_grid)
                self.missing_nums = self.missing_nums - 1
            else:
                self.wrong_attemps = self.wrong_attemps + 1
                print("Wrong. Attempts:", self.wrong_attemps, "/3")
                if self.wrong_attemps == 3:
                    break
            #cont = input("Continue (Y/N): ")
            #if cont == "N":
            #    break

if __name__ == "__main__":
    #print("Enter Grid Side Length (Square Number): ")
    #square_num = int(input())
    square_num = 9
    root = int(math.sqrt(square_num))
    print("Select Difficulty (Beginner, Easy, Medium, Hard):")
    difficulty = input()
    grid = Grid(difficulty, square_num, root)
    grid.solve()
    #print_grid(grid.grid)
    grid.new_puzzle()
    grid.add_num()
    grid.solve()

    print("Solution:")
    print_grid(grid.grid_store)
