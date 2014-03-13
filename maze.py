from random import randint, sample
import matplotlib.pyplot as plt


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
        self.maze = [[True for j in range(self.actual_num_cols)]
                     for i in range(self.actual_num_rows)]
        self.solved_path = [[False for j in range(self.actual_num_cols)]
                            for i in range(self.actual_num_rows)]

    def generate(self):
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
            self.maze[mazeRow][mazeCol] = False
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
                self.maze[temp_row][temp_col] = False
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

    def display(self):
        """(Maze) -> None
        plots the maze """
        plt.gca().yaxis.set_visible(False)
        plt.gca().xaxis.set_visible(False)
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if self.solved_path[row][col] or self.maze[row][col]:
                    if self.solved_path[row][col]:
                        color = [0, 1, 0]
                    elif self.maze[row][col]:
                        color = 'b'
                    plt.axvspan(col / self.actual_num_cols,
                                (col + 1) / self.actual_num_cols,
                                1 - row / self.actual_num_rows,
                                1 - (row + 1) / self.actual_num_rows,
                                facecolor=color)

    def solve(self, start=None, finish=None, visited=None):
        """(Maze, tuple, tuple, set) -> None
        solves a given maze"""
        if start is None:
            start = (0, 0)
        if finish is None:
            finish = (self.rows-1, self.cols-1)
        if visited is None:
            visited = set()
        self.solved_path[2 * start[0] + 1][2 * start[1] + 1] = True
        visited.add(start)
        if start == finish:
            return True
        for neighbor in self.get_neighbors(*start):
                wall_row = start[0] + 1 + neighbor[0]
                wall_col = start[1] + 1 + neighbor[1]
                if not self.maze[wall_row][wall_col] and \
                   not neighbor in visited and \
                   self.solve(neighbor, finish, visited):

                    self.solved_path[wall_row][wall_col] = True
                    return True

        self.solved_path[2 * start[0] + 1][2 * start[1] + 1] = False
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Display a random maze")
    parser.add_argument('--rows', dest='rows', metavar='N',
                        type=int, required=False, default=[11],
                        nargs=1, help="number of rows of maze")
    parser.add_argument('--cols', dest='cols', metavar='M',
                        type=int, required=False, default=[11],
                        nargs=1, help="number of columns of maze")
    parser.add_argument('--output', dest='file', metavar='file',
                        required=False, default=None, nargs='+',
                        help="prints the maze to a png file")
    parser.add_argument('--solve', dest='solve', action='store_const',
                        const=True, default=False,
                        help="display the solution to the maze")
    args = parser.parse_args()
    m = Maze(args.rows[0], args.cols[0])
    m.generate()
    m.display()
    if args.file is None:
        plt.show()
    else:
        plt.savefig(args.file[0])
    if args.solve:
        m.solve()
        m.display()
        if args.file is None:
            plt.show()
        else:
            if len(args.file) == 1:
                split = args.file[0].split(".")
                filename = "".join(split[:-1])
                extension = split[-1]
                plt.savefig(filename + "_solved." + extension)
            elif len(args.file) == 2:
                plt.savefig(args.file[1])
