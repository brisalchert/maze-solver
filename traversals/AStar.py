# ----------------------------------------------------------------------------------------------------------------------
#  AStar.py
#
#  Python class for performing an A* search on an adjacency list graph.
# ----------------------------------------------------------------------------------------------------------------------

import heapq
from time import sleep
from traversals import runtime

class AStar:
    def __init__(self, maze, set_color, slow_factor=None):
        self.maze = maze.graph
        self.start = maze.start
        self.end = maze.end
        self.set_color = set_color
        self.slow_factor = slow_factor

    def calculate_h_value(self, node):
        # Get coordinates of the node
        x_node, y_node = node.get_coordinates()

        # Get coordinates of the destination node
        x_dest, y_dest = self.end.get_coordinates()

        # Calculate Euclidean distance to destination node
        return ((x_node - x_dest) ** 2 + (y_node - y_dest) ** 2) ** 0.5

    def trace_path(self, node_details):
        # Set current node to the destination node's parent
        current = node_details[self.end].parent

        while node_details[current].parent is not None:
            # Get node coordinates
            x, y = current.get_coordinates()

            if current != self.start:
                self.set_color(x, y, "green")
            if self.slow_factor is not None:
                sleep(self.slow_factor)

            # Set current to next node
            current = node_details[current].parent

    @runtime
    def a_star(self):
        # Initialize closed list (for visited nodes)
        closed_list = {}
        for node in self.maze.keys():
            closed_list[node] = False

        # Initialize node details
        node_details = {}

        for node in self.maze.keys():
            node_details[node] = Node()

        # Initialize details for source node
        node_details[self.start].f = 0
        node_details[self.start].g = 0
        node_details[self.start].h = 0

        # Initialize counter for breaking ties for pushing to heap
        counter = 0

        # Initialize open list (for nodes to be visited)
        open_list = []
        heapq.heappush(open_list, (0.0, counter, self.start))
        counter += 1

        while len(open_list) > 0:
            # Pop the node with the lowest f value
            node = heapq.heappop(open_list)[2]

            # Mark the node as visited
            closed_list[node] = True

            # Toggle tile color
            x, y = node.get_coordinates()
            if (node != self.start) & (node != self.end):
                self.set_color(x, y, "skyblue")

            if self.slow_factor is not None:
                sleep(self.slow_factor)

            # Check neighbor nodes
            for neighbor in self.maze[node]:
                # If the neighbor has not been visited
                if not closed_list[neighbor]:
                    # If the node is the destination
                    if neighbor == self.end:
                        # Set the parent of the destination node
                        node_details[neighbor].parent = node

                        # Trace path from source to destination
                        self.trace_path(node_details)

                        return
                    else:
                        # Calculate new f, g, and h values
                        g_new = node_details[node].g + 1.0
                        h_new = self.calculate_h_value(neighbor)
                        f_new = g_new + h_new

                        # If the node is not in the open list or the new f value is smaller
                        if node_details[neighbor].f == float("inf") or node_details[neighbor].f > f_new:
                            # Add node to the open list
                            heapq.heappush(open_list, (f_new, counter, neighbor))
                            counter += 1

                            # Update node details
                            node_details[neighbor].g = g_new
                            node_details[neighbor].h = h_new
                            node_details[neighbor].f = f_new
                            node_details[neighbor].parent = node

class Node:
    def __init__(self):
        self.parent = None
        self.f = float("inf")
        self.g = float("inf")
        self.h = 0
