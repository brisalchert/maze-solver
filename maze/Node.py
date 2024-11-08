# ----------------------------------------------------------------------------------------------------------------------
#  Node.py
#
#  Python class for a node in a graph representation of a maze.
# ----------------------------------------------------------------------------------------------------------------------

DARKGRAY = (169, 169, 169)
SIZE = 20

class Node:
    def __init__(self, x, y):
        # Coordinates
        self.x = x
        self.y = y

        # Color-modifying properties
        self.visited = False

        # Dimensions
        self.width = SIZE
        self.height = SIZE

        # Initial Color
        self.color = DARKGRAY

        # Walls
        self.top_border = True
        self.bottom_border = True
        self.left_border = True
        self.right_border = True