import random
import sys
import traceback
from time import sleep
from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool, pyqtSignal, QObject
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow
from interface.userinterface import MazeWidget
from maze import Maze
from traversals import runtime, DepthFirstSearch
from traversals import BreadthFirstSearch
from traversals import AStar

# Increase recursion limit
sys.setrecursionlimit(10000)

class MainWindow(QMainWindow):
    def __init__(self, size, slow_factor=None):
        super().__init__()
        self.setWindowTitle("Maze Solver")
        self.setGeometry(600, 200, 824, 618)

        # Initialize maze and view
        self.maze = Maze(size)
        self.maze_widget = MazeWidget(size)
        self.setCentralWidget(self.maze_widget)

        # Factor to slow maze traversal algorithms by (in seconds per step)
        self.slow_factor = slow_factor

        # Assign button functions
        self.maze_widget.assign_generate_button(self.generate_maze)
        self.maze_widget.assign_solve_button(self.solve_maze)

        # Initialize generation flag
        self.maze_generated = False

        # Initialize threadpool
        self.threadpool = QThreadPool()

    def generate_maze(self):
        self.maze_generated = False

        # Get the maze size from slider
        size = self.maze_widget.get_slider_value()

        # Recreate maze if necessary
        if self.maze.length != size:
            # Recreate Maze object
            self.maze = Maze(size)

            # Recreate the view
            self.maze_widget.update_maze_size(size)
            self.maze_widget.reset_view()

            # Set maze endpoint colors
            self.set_endpoint_colors()
        else:
            # Reset the maze
            self.reset_maze_walls()

            # Reset maze colors
            self.reset_tile_colors()

        worker = Worker(self.generate_maze_dfs, self.maze, self.slow_factor)

        # Set thread to re-enabled buttons on completion
        worker.signals.finished.connect(self.enable_buttons)

        # Print runtime once thread completes
        worker.signals.result.connect(self.log_runtime)

        # Disable the buttons
        self.disable_buttons()

        # Start the generation thread
        self.threadpool.start(worker)

    def log_runtime(self, function_output):
        # Unpack function output
        function_name, function_runtime = function_output

        log_process = None

        # Set up log information for the relevant function
        match function_name:
            case "generate_maze_dfs":
                log_process = "Maze Generation:"
            case "dfs":
                log_process = "DFS:"
            case "bfs":
                log_process = "BFS:"
            case "a_star":
                log_process = "A*:"

        # Format log output
        log_output = "{:18}{:8.4f}s".format(log_process, function_runtime)

        if log_process:
            self.maze_widget.print_to_log(log_output)

    def disable_buttons(self):
        self.maze_widget.disable_buttons()

    def enable_buttons(self):
        self.maze_widget.enable_buttons()

    def reset_tile_colors(self):
        for x in range(self.maze.length):
            for y in range(self.maze.length):
                tile = self.maze_widget.get_tile(x, y)
                tile.setBrush(QBrush(QColor("lightgray")))

        self.set_endpoint_colors()

    def set_endpoint_colors(self):
        start_x, start_y = self.maze.start.get_coordinates()
        self.set_tile_color(start_x, start_y, "red")

        end_x, end_y = self.maze.end.get_coordinates()
        self.set_tile_color(end_x, end_y, "blue")

    def reset_maze_walls(self):
        for x in range(self.maze.length):
            for y in range(self.maze.length):
                tile = self.maze_widget.get_tile(x, y)
                tile.enableAllWalls()

        # Reset maze graph
        self.maze.reset_graph()

    def solve_maze(self):
        # Check that the maze has been generated
        if not self.maze_generated:
            return False                                    # !!! ADD ALERT !!! #

        algorithm = self.maze_widget.get_algorithm()

        # Reset maze colors
        self.reset_tile_colors()

        # Disable buttons
        self.disable_buttons()

        worker = None

        match algorithm:
            case "Depth First Search":
                worker = self.solve_maze_dfs()
            case "Breadth First Search":
                worker = self.solve_maze_bfs()
            case "A*":
                worker = self.solve_maze_astar()

        # Set thread to re-enable buttons upon completion
        worker.signals.finished.connect(self.enable_buttons)

        # Print runtime once thread completes
        worker.signals.result.connect(self.log_runtime)

        # Start the DFS thread
        self.threadpool.start(worker)

    def solve_maze_dfs(self):
        # Initialize DFS
        solve_dfs = DepthFirstSearch(self.maze, self.set_tile_color, slow_factor=self.slow_factor)

        # Initialize worker thread to perform DFS
        worker = Worker(solve_dfs.dfs)

        return worker

    def solve_maze_bfs(self):
        # Initialize BFS
        solve_bfs = BreadthFirstSearch(self.maze, self.set_tile_color, slow_factor=self.slow_factor)

        # Initialize worker thread to perform BFS
        worker = Worker(solve_bfs.bfs)

        return worker

    def solve_maze_astar(self):
        # Initialize A*
        a_star = AStar(self.maze, self.set_tile_color, slow_factor=self.slow_factor)

        # Initialize worker thread to perform A* search
        worker = Worker(a_star.a_star)

        return worker

    def set_tile_color(self, x, y, color):
        tile = self.maze_widget.get_tile(x, y)
        tile.setBrush(QBrush(QColor(color)))

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
        if (node1 != self.maze.start) & (node1 != self.maze.end):
            tile1.setBrush(QBrush(QColor("green")))
        if (node2 != self.maze.start) & (node2 != self.maze.end):
            tile2.setBrush(QBrush(QColor("green")))
        return True

    def backtrack(self, node1, node2):
        # Get tiles from nodes
        node1_x, node1_y = node1.get_coordinates()
        node2_x, node2_y = node2.get_coordinates()
        tile1 = self.maze_widget.get_tile(node1_x, node1_y)
        tile2 = self.maze_widget.get_tile(node2_x, node2_y)

        # Change tile colors to indicate completed path
        if (node1 != self.maze.start) & (node1 != self.maze.end):
            tile1.setBrush(QBrush(QColor("gold")))
        if (node2 != self.maze.start) & (node2 != self.maze.end):
            tile2.setBrush(QBrush(QColor("gold")))

    @runtime
    def generate_maze_dfs(self, maze, slow_factor=None):
        # Create a boolean visited dictionary
        visited = {}
        for vertex in maze.graph.keys():
            visited[vertex] = False

        # Traverse the graph using the recursive function
        self.__traverse(maze, visited, self.maze.start, slow_factor)

        # Set maze generated flag
        self.maze_generated = True

        # Reset tile colors
        self.reset_tile_colors()

    def __traverse(self, maze, visited, current, slow_factor):
        # Get graph from maze
        graph = maze.generation_graph

        # Mark current node as visited
        visited[current] = True

        if slow_factor is not None:
            sleep(slow_factor)

        # Recursively visit all adjacent unvisited nodes
        for i in range(len(graph[current])):
            unvisited = [neighbor for neighbor in graph[current] if visited[neighbor] == False]
            if len(unvisited) > 0:
                neighbor = random.choice(unvisited)
                # Remove the wall between the two nodes
                self.toggle_wall(current, neighbor)
                # Add edge between the two nodes
                maze.add_edge(current, neighbor)
                # Visit the neighbor node
                self.__traverse(maze, visited, neighbor, slow_factor)
                self.backtrack(current, neighbor)
                if slow_factor is not None:
                    sleep(slow_factor)

class Worker(QRunnable):
    """
    (Adapted from: https://www.pythonguis.com/tutorials/multithreading-pyqt6-applications-qthreadpool/)
    Worker thread for running various maze functions.
    """

    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialize the runner function with passed args, kwargs.
        """

        try:
            result = self.function(
                *self.args, **self.kwargs
            )
        except Exception as e:
            traceback.print_exc()
            except_type, value = sys.exc_info()[:2]
            self.signals.error.emit((except_type, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()

class WorkerSignals(QObject):
    """
    (Adapted from: https://www.pythonguis.com/tutorials/multithreading-pyqt6-applications-qthreadpool/)
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (except_type, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

if __name__ == '__main__':
    maze_size = 25
    slow_factor = 0.005

    app = QApplication([])

    window = MainWindow(maze_size, slow_factor)
    window.show()

    app.exec()
