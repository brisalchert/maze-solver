from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QObject
from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView, QWidget, QVBoxLayout, QListWidget, \
    QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QComboBox, QSlider, QLabel, QErrorMessage


class MazeWidget(QWidget):
    def __init__(self, size):
        super().__init__()
        self.dimension = size
        self.max_dimension = 50
        self.tile_size = 15
        self.view_size = self.tile_size * (self.max_dimension + 2)
        self.tiles = {}
        self.initial_slow_value = 50

        self.font = QFont("Cascadia Code", 10)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setMaximumSize(self.view_size, self.view_size)
        self.view.setMinimumSize(self.view_size, self.view_size)
        self.view.setBackgroundBrush(QBrush(QColor("gray")))

        self.generate_button = QPushButton("Generate Maze", self)
        self.generate_button.setFont(self.font)
        self.solve_button = QPushButton("Solve Maze", self)
        self.solve_button.setFont(self.font)

        self.size_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.size_slider.setMinimum(15)
        self.size_slider.setMaximum(self.max_dimension)
        self.size_slider.setTickInterval(1)

        self.size_value = QLabel(self)
        self.size_value.setFont(self.font)

        self.size_label = QLabel("Maze Size:", self)
        self.size_label.setFont(self.font)
        self.size_slider.valueChanged.connect(self.update_size_label)

        self.algorithm_selection = QComboBox(self)
        self.algorithm_selection.setFont(self.font)
        self.algorithm_selection.addItems([
            "Depth First Search",
            "Breadth First Search",
            "A*"
        ])

        self.size_slider_layout = QHBoxLayout()
        self.size_slider_layout.addWidget(self.size_label)
        self.size_slider_layout.addWidget(self.size_value)
        self.size_slider_layout.addWidget(self.size_slider)

        self.selection_layout = QHBoxLayout()
        self.selection_layout.addLayout(self.size_slider_layout, stretch=1)
        self.selection_layout.addWidget(self.algorithm_selection, stretch=1)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.generate_button, stretch=1)
        self.button_layout.addWidget(self.solve_button, stretch=1)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setFont(self.font)
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
            }
        """)

        self.slow_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slow_slider.setMinimum(0)
        self.slow_slider.setMaximum(100)
        self.slow_slider.setTickInterval(1)

        self.slow_value = QLabel(self)
        self.slow_value.setFont(self.font)
        self.slow_value.setMinimumWidth(24)
        self.slow_value.setAlignment((Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter))

        self.slow_label = QLabel("Slow Factor:", self)
        self.slow_label.setFont(self.font)
        self.slow_slider.valueChanged.connect(self.update_slow_label)

        self.slow_layout = QHBoxLayout()
        self.slow_layout.addWidget(self.slow_label)
        self.slow_layout.addWidget(self.slow_value)
        self.slow_layout.addWidget(self.slow_slider)

        self.log = QListWidget(self)
        self.log.setFont(self.font)
        self.log.setViewportMargins(10, 10, 10, 10)
        self.log.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.log.setMinimumWidth(260)
        self.log.setMaximumWidth(260)

        self.log_label = QLabel("Runtime Log", self)
        self.log_label.setFont(self.font)
        self.log_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.log_reset_button = QPushButton("Reset Log", self)
        self.log_reset_button.setFont(self.font)
        self.log_reset_button.clicked.connect(self.reset_log)

        self.maze_layout = QVBoxLayout()
        self.maze_layout.addWidget(self.view)
        self.maze_layout.addLayout(self.selection_layout)
        self.maze_layout.addLayout(self.button_layout)
        self.maze_layout.addLayout(self.slow_layout)
        self.maze_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.log_layout = QVBoxLayout()
        self.log_layout.addWidget(self.log_label)
        self.log_layout.addWidget(self.log)
        self.log_layout.addWidget(self.log_reset_button)
        self.log_layout.addWidget(self.exit_button)

        self.interface_layout = QHBoxLayout()
        self.h_spacer = QSpacerItem(10000, 0, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        self.interface_layout.addItem(self.h_spacer)
        self.interface_layout.addLayout(self.maze_layout)
        self.interface_layout.addLayout(self.log_layout)
        self.interface_layout.addItem(self.h_spacer)
        self.interface_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.top_level_layout = QVBoxLayout()
        self.v_spacer = QSpacerItem(0, 10000, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.top_level_layout.addItem(self.v_spacer)
        self.top_level_layout.addLayout(self.interface_layout)
        self.top_level_layout.addItem(self.v_spacer)
        self.setLayout(self.top_level_layout)

        # Initialize the maze tiles
        self.initialize_tiles()

        # Initialize size slider and label
        self.size_slider.setValue(self.dimension)
        self.update_size_label()

        # Initialize slow slider and label
        self.slow_slider.setValue(self.initial_slow_value)
        self.update_slow_label()

        # Connect tile changes to view updates
        self.connect_tile_updates()

    def update_maze_size(self, size):
        self.dimension = size

    def reset_view(self):
        # Create new scene and view
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        # Recreate maze tiles
        self.tiles = {}

        self.initialize_tiles()
        self.connect_tile_updates()

    def get_size_value(self):
        return self.size_slider.value()

    def update_size_label(self):
        self.size_value.setText(str(self.size_slider.value()))

    def get_slow_value(self):
        return self.slow_slider.value() * 0.0001

    def update_slow_label(self):
        self.slow_value.setText(str(self.slow_slider.value()))

    def print_to_log(self, text):
        self.log.addItem(text)

    def reset_log(self):
        self.log.clear()

    def get_algorithm(self):
        return self.algorithm_selection.currentText()

    def assign_generate_button(self, function):
        self.generate_button.clicked.connect(function)

    def assign_solve_button(self, function):
        self.solve_button.clicked.connect(function)

    def assign_exit_button(self, function):
        self.exit_button.clicked.connect(function)

    def disable_buttons(self):
        self.generate_button.setEnabled(False)
        self.solve_button.setEnabled(False)

    def enable_buttons(self):
        self.generate_button.setEnabled(True)
        self.solve_button.setEnabled(True)

    def display_solve_error(self):
        error_dialog = QErrorMessage(self)
        error_dialog.setWindowTitle("Error")
        error_dialog.showMessage("Error: Please generate a maze before solving.")

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
        self.wall_color = QColor("gray")
        self.wall_width = 1

        self.top_wall = QRectF(0, 0, tile_size, self.wall_width)
        self.bottom_wall = QRectF(0, tile_size - self.wall_width, tile_size, self.wall_width)
        self.left_wall = QRectF(0, 0, self.wall_width, tile_size)
        self.right_wall = QRectF(tile_size - self.wall_width, 0, self.wall_width, tile_size)

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
            painter.fillRect(self.top_wall, QBrush(self.wall_color))
        if self.bottom_wall_visible:
            painter.fillRect(self.bottom_wall, QBrush(self.wall_color))
        if self.left_wall_visible:
            painter.fillRect(self.left_wall, QBrush(self.wall_color))
        if self.right_wall_visible:
            painter.fillRect(self.right_wall, QBrush(self.wall_color))
