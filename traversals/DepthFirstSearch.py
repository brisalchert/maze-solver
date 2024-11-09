# ----------------------------------------------------------------------------------------------------------------------
#  DepthFirstSearch.py
#
#  Python class for performing a Depth First Search (DFS) on an adjacency list graph.
# ----------------------------------------------------------------------------------------------------------------------

from time import sleep

class DepthFirstSearch:
    def __init__(self, maze, set_color, slow_factor=None):
        self.maze = maze.graph
        self.start = maze.start
        self.end = maze.end
        self.reached = [False]
        self.set_color = set_color
        self.slow_factor = slow_factor

    def dfs(self):
        # Create a boolean visited dictionary
        visited = {}
        for vertex in self.maze.keys():
            visited[vertex] = False

        # Traverse the graph using the recursive function
        self.__traverse(self.maze, visited, self.start)

    def __traverse(self, graph, visited, current):
        # Visit the current node
        visited[current] = True

        # Toggle tile color
        x, y = current.get_coordinates()
        self.set_color(x, y, "skyblue")

        if self.slow_factor is not None:
            sleep(self.slow_factor)

        # Check if the node is the goal
        if current == self.end:
            self.reached[0] = True

            # Change tile color to the path
            self.set_color(x, y, "green")
            return

        # Recursively traverse adjacent nodes until the goal is found
        for neighbor in graph[current]:
            if (not self.reached[0]) & (not visited[neighbor]):
                self.__traverse(graph, visited, neighbor)

                # Upon returning from completing the maze, set path node color
                if self.reached[0]:
                    self.set_color(x, y, "green")
                    sleep(self.slow_factor)
                    return
