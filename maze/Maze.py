# ----------------------------------------------------------------------------------------------------------------------
#  Maze.py
#
#  Python class for a maze represented by a graph. The graph is made up of Node objects.
# ----------------------------------------------------------------------------------------------------------------------

from maze import Node

class Maze:
    def __init__(self, length):
        # Start and End nodes
        self.start = None
        self.end = None

        # Graph for maze
        self.graph = {}

        # Length and width of maze
        self.length = length

        # Initialize maze nodes
        self.__initialize_nodes()

    def __initialize_nodes(self):
        """
        Initializes all graph nodes and populates their neighbor lists.
        """
        grid = {}

        # Create nodes
        for x in range(self.length):
            for y in range(self.length):
                # Create node
                node = Node(x, y)

                # Save start and end nodes
                if x == 0 and y == 0:
                    self.start = node
                if x == self.length - 1 and y == self.length - 1:
                    self.end = node

                # Initialize adjacency list
                self.graph[node] = []

                # Add node to the temporary grid
                grid[(x, y)] = node

        # Initialize neighbors for each node
        self.__initialize_neighbors(grid)

    def __initialize_neighbors(self, grid):
        """
        Initializes neighbor lists for all graph nodes.
        :param grid: a dictionary grid of all graph nodes.
        """
        for x in range(1, self.length):
            col = x
            row = 0

            # Add neighbors downward until diagonal is reached
            while row < col:
                # Bi-directionally connect with left node
                grid[(col, row)].add_neighbor(grid[(col - 1, row)])
                grid[(col - 1, row)].add_neighbor(grid[(col, row)])

                # Bi-directionally connect with upper node
                if row > 0:
                    grid[(col, row)].add_neighbor(grid[(col, row - 1)])
                    grid[(col, row - 1)].add_neighbor(grid[(col, row)])

                row += 1

            # Add diagonal's neighbors
            grid[(col, row)].add_neighbor(grid[(col - 1, row)])
            grid[(col - 1, row)].add_neighbor(grid[(col, row)])
            grid[(col, row)].add_neighbor(grid[(col, row - 1)])
            grid[(col, row - 1)].add_neighbor(grid[(col, row)])

            col -= 1

            # Add neighbors to the left until edge is reached
            while col >= 0:
                # Bi-directionally connect with left node
                if col > 0:
                    grid[(col, row)].add_neighbor(grid[(col - 1, row)])
                    grid[(col - 1, row)].add_neighbor(grid[(col, row)])

                # Bi-directionally connect with upper node
                grid[(col, row)].add_neighbor(grid[(col, row - 1)])
                grid[(col, row - 1)].add_neighbor(grid[(col, row)])

                col -= 1
