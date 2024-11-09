import random
import sys
from time import sleep
from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from interface.userinterface import MazeWidget
from maze import Maze
from traversals import DepthFirstSearch

# Increase recursion limit
sys.setrecursionlimit(10000)

class MainWindow(QMainWindow):
    def __init__(self, size):
        super().__init__()
        self.setWindowTitle("Maze Solver")
        self.setGeometry(1100, 500, 600, 600)

        self.maze = Maze(size)
        self.maze_widget = MazeWidget(size)
        self.setCentralWidget(self.maze_widget)

        # Factor to slow maze traversal algorithms by (in seconds per step)
        self.slow_factor = 0.005

        self.generate_button = QPushButton("Start", self)
        self.generate_button.clicked.connect(self.generate_maze)
        self.maze_widget.layout.addWidget(self.generate_button)

        self.threadpool = QThreadPool()

    def generate_maze(self):
        worker = self.GenerationWorker(self.generate_maze_dfs, self.maze.graph)

        # Start the generation thread
        self.threadpool.start(worker)

    def reset_tile_colors(self):
        for x in range(self.maze.length):
            for y in range(self.maze.length):
                tile = self.maze_widget.get_tile(x, y)
                tile.setBrush(QBrush(QColor("lightgray")))

    def toggle_wall(self, node1, node2):
        # Get tiles from nodes
        node1_x, node1_y = node1.get_coordinates()
        node2_x, node2_y = node2.get_coordinates()
        tile1 = self.maze_widget.get_tile(node1_x, node1_y)
        tile2 = self.maze_widget.get_tile(node2_x, node2_y)

        if not tile1.isAdjacent(tile2):
            return False
        if tile1.x == tile2.x:
            if tile1.y == tile2.y - 1:
                tile1.toggleWallVisible("bottom")
                tile2.toggleWallVisible("top")
            if tile1.y == tile2.y + 1:
                tile1.toggleWallVisible("top")
                tile2.toggleWallVisible("bottom")
        else:
            if tile1.x == tile2.x - 1:
                tile1.toggleWallVisible("right")
                tile2.toggleWallVisible("left")
            if tile1.x == tile2.x + 1:
                tile1.toggleWallVisible("left")
                tile2.toggleWallVisible("right")
        tile1.setBrush(QBrush(QColor("green")))
        tile2.setBrush(QBrush(QColor("green")))
        return True

    def backtrack(self, node1, node2):
        # Get tiles from nodes
        node1_x, node1_y = node1.get_coordinates()
        node2_x, node2_y = node2.get_coordinates()
        tile1 = self.maze_widget.get_tile(node1_x, node1_y)
        tile2 = self.maze_widget.get_tile(node2_x, node2_y)

        # Change tile colors to indicate completed path
        tile1.setBrush(QBrush(QColor("gold")))
        tile2.setBrush(QBrush(QColor("gold")))

    def generate_maze_dfs(self, graph):
        # Create a boolean visited dictionary
        visited = {}
        for vertex in graph.keys():
            visited[vertex] = False

        # Traverse the graph using the recursive function
        self.__traverse(graph, visited, self.maze.start)

        # Reset tile colors
        self.reset_tile_colors()

    def __traverse(self, graph, visited, current):
        # Mark current node as visited
        visited[current] = True

        sleep(0.005)

        # Recursively visit all adjacent unvisited nodes
        for i in range(len(graph[current])):
            unvisited = [neighbor for neighbor in graph[current] if visited[neighbor] == False]
            if len(unvisited) > 0:
                neighbor = random.choice(unvisited)
                # Remove the wall between the two nodes
                self.toggle_wall(current, neighbor)
                # Visit the neighbor node
                self.__traverse(graph, visited, neighbor)
                self.backtrack(current, neighbor)
                sleep(0.005)

    class GenerationWorker(QRunnable):
        """
        Worker thread for running various maze functions.
        """

        def __init__(self, function, *args, **kwargs):
            super().__init__()
            self.function = function
            self.args = args
            self.kwargs = kwargs

        @pyqtSlot()
        def run(self):
            """
            Runs the function passed to the worker thread.
            """
            self.function(*self.args, **self.kwargs)

if __name__ == '__main__':
    maze_size = 25

    app = QApplication([])

    window = MainWindow(maze_size)
    window.show()

    app.exec()
