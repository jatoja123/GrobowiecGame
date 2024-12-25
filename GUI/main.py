import sys

from modules.menu import *
from modules.map import *
from modules.legend import *
from modules.input import *

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QSizePolicy
)

WINDOW_TITLE = "Grobowiec Game"
BG_COLOR = QColor(0, 23, 31)
MIN_H = 600
MIN_W = 1070

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setStyleSheet(f'background-color:{BG_COLOR.name()}')
        self.setMinimumSize(MIN_W, MIN_H)

        self.central = QWidget()
        self.outerLayout = QHBoxLayout()
        self.playerLayout = QVBoxLayout()

        #|---- menu widget ----|
        self.menu = Menu(self)
        self.menu.setBaseSize(int(MIN_W*0.15)-70, MIN_H-70)
        self.menu.setMinimumSize(self.menu.baseSize()) #zmienić, tak aby było zawsze widoczne
        self.menu.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        self.outerLayout.addWidget(self.menu)

        #|---- map widget ----|
        self.map = Map(self)
        self.map.setBaseSize(int(MIN_W*0.65)-70, MIN_H-70)
        self.map.setMinimumSize(self.map.baseSize())
        self.map.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.outerLayout.addWidget(self.map)

        #|---- legend widget ----|
        self.legend = Legend(self)
        self.legend.setBaseSize(int(MIN_W*0.2)-70, int(MIN_H/2)-70)
        self.legend.setMinimumSize(self.legend.baseSize())
        self.legend.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        self.playerLayout.addWidget(self.legend)

        #|---- input widget ----|
        self.input = Input(self)
        self.input.setBaseSize(int(MIN_W*0.2)-70, int(MIN_H/2)-70)
        self.input.setMinimumSize(self.input.baseSize())
        self.input.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.playerLayout.addWidget(self.input)
        self.outerLayout.addLayout(self.playerLayout)

        self.central.setLayout(self.outerLayout)
        self.setCentralWidget(self.central)

if __name__ == "__main__":
    app = QApplication(sys.argv)  
    window = MainWindow()

    window.show()
    sys.exit(app.exec())