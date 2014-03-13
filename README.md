Mazes
=====

Generates random maze using a backtracking algorithm

Usage
-----
        $ python3 maze.py [-h] [--rows N] [--cols M] [--output file [file ...]] [--solve]

        Display a random maze

        optional arguments:
          -h, --help            show this help message and exit
          --rows N              number of rows of maze
          --cols M              number of columns of maze
          --output file [file ...]
                                prints the maze to a png file
          --solve               display the solution to the maze

Example
-------

        $ python3 maze.py --row 11 --cols 11 --solve --output unsolved.png solved.png

generates a maze of size 11x11, and prints it to two files:

one with a solution, and one without.



Required
--------

matplotlib.pyplot
