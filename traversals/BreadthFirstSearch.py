# ----------------------------------------------------------------------------------------------------------------------
#  BreadthFirstSearch.py
#
#  Python class for performing a Depth First Search (DFS) on an adjacency list graph.
# ----------------------------------------------------------------------------------------------------------------------

from collections import deque
from time import sleep
from traversals import runtime

class BreadthFirstSearch:
    def __init__(self, maze, set_color, slow_factor=None):
        self.maze = maze.graph
        self.start = maze.start
        self.end = maze.end
        self.reached = False
        self.set_color = set_color
        self.slow_factor = slow_factor

    @runtime
    def bfs(self):
        # Create a boolean visited dictionary
        visited = {}
        for vertex in self.maze.keys():
            visited[vertex] = False

        # Create a dictionary for storing parent nodes
        parent = {}
        for vertex in self.maze.keys():
            parent[vertex] = None

        # Create a queue for nodes
        queue = deque()

        # Visit the starting node and enqueue
        visited[self.start] = True
        queue.append(self.start)

        current = None

        # Iterate through the queue, visiting nodes and enqueuing neighbors
        while not self.reached:
            current = queue.popleft()

            # Toggle tile color
            x, y = current.get_coordinates()
            if (current != self.start) & (current != self.end):
                self.set_color(x, y, "skyblue")

            if self.slow_factor is not None:
                sleep(self.slow_factor)

            # Check if the node is the goal
            if current == self.end:
                self.reached = True

                break

            # Visit neighboring nodes
            for neighbor in self.maze[current]:
                # If neighbor has not been visited
                if not visited[neighbor]:
                    # Mark parent node for this neighbor
                    parent[neighbor] = current
                    # Visit neighbor and enqueue
                    visited[neighbor] = True
                    queue.append(neighbor)

        # Backtrack along the path
        while parent[current] is not None:
            current = parent[current]

            # Get tile coordinates
            x, y = current.get_coordinates()

            if current != self.start:
                self.set_color(x, y, "green")
            if self.slow_factor is not None:
                sleep(self.slow_factor)
