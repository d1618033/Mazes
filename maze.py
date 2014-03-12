from random import randint, sample
import matplotlib.pyplot as plt

USAGE = """
Generates random maze using a backtracking algorithm

Usage: python maze.py N M [filename]
N - number of rows (must be an odd number)
M - number of columns (must be an odd number)
filename - if specified, the maze will be saved to a file
"""


class Maze:

    def __init__(self, rows, cols):
        """(Maze, int, int) -> None
        initializes a maze object
        input: rows, cols - number of rows and columns of the maze
        """
        self.rows = (rows - 1) // 2
        self.cols = (cols - 1) // 2
        self.actual_num_rows = 2 * self.rows + 1
        self.actual_num_cols = 2 * self.cols + 1
        self.maze = [[1 for j in range(self.actual_num_cols)]
                     for i in range(self.actual_num_cols)]

    def generate_maze(self):
        """(Maze) -> None
        generates a random maze"""
        visited = [[False for j in range(self.cols)] for i in range(self.rows)]
        stack = []
        # Make the initial cell the current cell and mark it as visited
        row, col = self.rows - 1, self.cols - 1
        visited[row][col] = True
        numUnvisited = self.cols * self.rows - 1
        # While there are unvisited cells
        while True:
            mazeRow, mazeCol = 2 * row + 1, 2 * col + 1
            self.maze[mazeRow][mazeCol] = 0
            if numUnvisited == 0:
                break
            # If the current cell has any neighbours which have not been
            # visited
            neighbors = self.get_neighbors(row, col)
            unvisitedNeighbors = [x for x in neighbors
                                  if not visited[x[0]][x[1]]]
            if len(unvisitedNeighbors) > 0:
                # Choose randomly one of the unvisited neighbours
                chosen = sample(unvisitedNeighbors, 1)[0]
                # Push the current cell to the stack
                stack.append((row, col))
                # Remove the wall between the current cell and the chosen cell
                temp_row = mazeRow + chosen[0] - row
                temp_col = mazeCol + chosen[1] - col
                self.maze[temp_row][temp_col] = 0
                # Make the chosen cell the current cell and mark it as visited
                row, col = chosen
                visited[row][col] = True
                numUnvisited -= 1
            # Else if stack is not empty
            elif len(stack) > 0:
                # Pop a cell from the stack
                # Make it the current cell
                row, col = stack.pop()
            else:
                # Pick a random unvisited cell, make it the current cell and
                # mark it as visited
                row, col = randint(0, self.rows - 1), randint(0, self.cols - 1)
                visited[row][col] = True
                numUnvisited -= 1

    def get_neighbors(self, row, col):
        """(Maze, int, int) -> list
        returns a list of all the neighbors of the cell row,col"""
        neighbors = []
        if row >= 1:
            neighbors.append((row - 1, col))
        if col >= 1:
            neighbors.append((row, col - 1))
        if row <= self.rows - 2:
            neighbors.append((row + 1, col))
        if col <= self.cols - 2:
            neighbors.append((row, col + 1))
        return neighbors

    def displayMaze(self):
        """(Maze) -> None
        plots the maze """
        plt.gca().yaxis.set_visible(False)
        plt.gca().xaxis.set_visible(False)
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if self.maze[row][col] == 1:
                    plt.axvspan(row / self.actual_num_rows,
                                (row + 1) / self.actual_num_rows,
                                col / self.actual_num_cols,
                                (col + 1) / self.actual_num_cols)

    def get_open_neighbors(self, row, col):
        return [x for x in self.get_neighbors(row, col)
                if self.maze[2*row+1+x[0]-row][2*col+1+x[1]-col] == 0]

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(USAGE)
    else:
        N, M = sys.argv[1:3]
        N, M = int(N), int(M)
        m = Maze(N, M)
        m.generate_maze()
        m.displayMaze()
        if len(sys.argv) == 4:
            plt.savefig(sys.argv[3])
        else:
            plt.show()
