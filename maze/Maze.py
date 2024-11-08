# ----------------------------------------------------------------------------------------------------------------------
#  Maze.py
#
#  Python class for a maze represented by a graph. The graph is made up of Node objects.
# ----------------------------------------------------------------------------------------------------------------------

from maze import Node

class Maze:
    def __init__(self, length):
        # Graph for maze
        self.graph = {}

        # Length and width of maze
        self.length = length

        # Initialize maze nodes
        self.__initialize_nodes()

    def __initialize_nodes(self):
        for x in range(self.length):
            for y in range(self.length):
                # Create node
                node = Node(x, y)

                # Initialize adjacency list
                self.graph[node] = []