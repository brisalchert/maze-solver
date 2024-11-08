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

        # Neighboring nodes
        self.neighbors = []

    def add_neighbor(self, neighbor):
        """
        Adds a neighbor node to this node's list of neighbors if it is not already present.
        :param neighbor: the neighbor node
        :return: True if the neighbor node was added, False otherwise
        """
        if not self.neighbors.__contains__(neighbor):
            self.neighbors.append(neighbor)
            return True

        return False

    def get_neighbors(self):
        """
        Accessor for a node's neighbors.
        :return: The list of neighboring nodes
        """
        return self.neighbors