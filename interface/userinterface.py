from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QObject
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView, QWidget, QVBoxLayout, QListWidget, \
    QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLayout


class MazeWidget(QWidget):
    def __init__(self, length):
        super().__init__()
        self.dimension = length
        self.tile_size = 20
        self.view_size = self.tile_size * (self.dimension + 2)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setMaximumSize(self.view_size, self.view_size)
        self.view.setMinimumSize(self.view_size, self.view_size)
        self.view.setBackgroundBrush(QBrush(QColor("gray")))

        self.generate_button = QPushButton("Generate Maze", self)
        self.dfs_button = QPushButton("Solve with DFS", self)

        self.log = QListWidget(self)
        self.log.setMinimumWidth(260)
        self.log.setMaximumWidth(260)

        self.maze_layout = QVBoxLayout()
        self.maze_layout.addWidget(self.view)
        self.maze_layout.addWidget(self.generate_button)
        self.maze_layout.addWidget(self.dfs_button)
        self.maze_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.log_layout = QHBoxLayout()
        self.h_spacer = QSpacerItem(10000, 0, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        self.log_layout.addItem(self.h_spacer)
        self.log_layout.addLayout(self.maze_layout)
        self.log_layout.addWidget(self.log)
        self.log_layout.addItem(self.h_spacer)
        self.log_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.top_level_layout = QVBoxLayout()
        self.v_spacer = QSpacerItem(0, 10000, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.top_level_layout.addItem(self.v_spacer)
        self.top_level_layout.addLayout(self.log_layout)
        self.top_level_layout.addItem(self.v_spacer)
        self.setLayout(self.top_level_layout)

        # Initialize MazeTile dictionary
        self.tiles = {}

        # Initialize the maze tiles
        self.initialize_tiles()

        # Connect tile changes to view updates
        self.connect_tile_updates()

    def assign_generate_button(self, function):
        self.generate_button.clicked.connect(function)

    def assign_dfs_button(self, function):
        self.dfs_button.clicked.connect(function)

    def disable_buttons(self):
        self.generate_button.setEnabled(False)
        self.dfs_button.setEnabled(False)

    def enable_buttons(self):
        self.generate_button.setEnabled(True)
        self.dfs_button.setEnabled(True)

    def connect_tile_updates(self):
        for x in range(self.dimension):
            for y in range(self.dimension):
                tile = self.tiles.get((x, y))

                # Connect tileChanged signal to the update method
                tile.com.tileChanged.connect(self.update_view)

    @QtCore.pyqtSlot()
    def update_view(self):
        self.view.viewport().update()

    def initialize_tiles(self):
        for x in range(self.dimension):
            for y in range(self.dimension):
                x_pos = x * self.tile_size
                y_pos = y * self.tile_size
                tile = MazeTile(x, y, self.tile_size)
                tile.setBrush(QBrush(QColor("lightgray")))
                tile.setPos(x_pos, y_pos)
                self.scene.addItem(tile)

                # Add tile to dictionary with coordinates
                self.tiles[(x, y)] = tile

    def get_tile(self, x, y):
        return self.tiles[(x, y)]

class MazeTile(QGraphicsItem):
    # Define signal as class variable
    class Communicate(QObject):
        tileChanged = pyqtSignal()

    def __init__(self, x, y, tile_size):
        super().__init__()
        self.x = x
        self.y = y
        self.tile = QRectF(0, 0, tile_size, tile_size)

        self.top_wall = QRectF(0, 0, tile_size, 1)
        self.bottom_wall = QRectF(0, tile_size - 1, tile_size, 1)
        self.left_wall = QRectF(0, 0, 1, tile_size)
        self.right_wall = QRectF(tile_size - 1, 0, 1, tile_size)

        self.top_wall_visible = True
        self.bottom_wall_visible = True
        self.left_wall_visible = True
        self.right_wall_visible = True

        self._brush = QBrush(QColor("black"))

        self.com = self.Communicate()

    def setBrush(self, brush):
        self._brush = brush
        self.com.tileChanged.emit()

    def toggleWallVisible(self, wall=None):
        match wall:
            case "top":
                self.top_wall_visible = not self.top_wall_visible
            case "bottom":
                self.bottom_wall_visible = not self.bottom_wall_visible
            case "left":
                self.left_wall_visible = not self.left_wall_visible
            case "right":
                self.right_wall_visible = not self.right_wall_visible
            case _:
                pass
        self.com.tileChanged.emit()

    def enableAllWalls(self):
        self.top_wall_visible = True
        self.bottom_wall_visible = True
        self.left_wall_visible = True
        self.right_wall_visible = True

    def isAdjacent(self, other_tile):
        if self.x == other_tile.x:
            if self.y == other_tile.y - 1 or self.y == other_tile.y + 1:
                return True
        if self.y == other_tile.y:
            if self.x == other_tile.x - 1 or self.x == other_tile.x + 1:
                return True
        return False

    def boundingRect(self):
        return self.tile

    def paint(self, painter=None, style=None, widget=None):
        painter.fillRect(self.tile, self._brush)
        if self.top_wall_visible:
            painter.fillRect(self.top_wall, QBrush(QColor("black")))
        if self.bottom_wall_visible:
            painter.fillRect(self.bottom_wall, QBrush(QColor("black")))
        if self.left_wall_visible:
            painter.fillRect(self.left_wall, QBrush(QColor("black")))
        if self.right_wall_visible:
            painter.fillRect(self.right_wall, QBrush(QColor("black")))
