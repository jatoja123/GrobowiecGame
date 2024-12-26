import sys

from modules.menu import *
from modules.map import *
from modules.legend import *
from modules.input import *

from PyQt6.QtGui import QColor, QAction
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QSizePolicy,
)

WINDOW_TITLE = "Grobowiec Game"
BG_COLOR = QColor(0, 23, 31)
TEXT_COLOR = QColor(197, 202, 212)
MIN_H = 600
MIN_W = 1070

class NewGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New game settings")

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

class UnsavedGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Game NOT saved")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("All progress will be lost.\nDo you want to proceed?"))
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setStyleSheet(f'background-color:{BG_COLOR.name()}; color:{TEXT_COLOR.name()}; font-weight: bold;')
        self.setMinimumSize(MIN_W, MIN_H)

        self.central = QWidget()

        self.btn_newGame = QAction("New Game", self)
        self.btn_newGame.setCheckable(False)
        self.btn_newGame.triggered.connect(self.openNewGameDialog)

        self.btn_loadGame = QAction("Load Game", self)
        self.btn_loadGame.setCheckable(False)
        #self.btn_loadGame.triggered.connect()  #odpalić okienko eklspoloratora do odczytania pliku gry

        self.btn_saveGame = QAction("Save", self)
        self.btn_saveGame.setCheckable(False)
        #self.btn_loadGame.triggered.connect()  #odpalić okienko eklspoloratora do zapisania jezeli nie ma pliku

        self.menu = self.menuBar()

        self.game_menu = self.menu.addMenu("Game")
        self.game_menu.addAction(self.btn_saveGame)
        self.game_menu.addSeparator()
        self.game_menu.addAction(self.btn_newGame)
        self.game_menu.addAction(self.btn_loadGame)
        self.menu.setStyleSheet('''
            QMenu { 
                background-color: '''+BG_COLOR.name()+''';
                color: '''+TEXT_COLOR.name()+''';
                border-color: '''+TEXT_COLOR.name()+''';
                border: 2px;
                border-style: solid;
                font-weight: bold;
                }
        ''')
        
    def openNewGameDialog(self):
        self.dialog = UnsavedGameDialog(self)

        if hasattr(self, 'game'):
            if self.game != None and (not self.dialog.exec()): return
        return print("Succes!") #open settings dialog


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(self.central)

class GameWindow(Window):
    def __init__(self):
        super().__init__()
        self.game = 1 #GameEngine() class here
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
    window = GameWindow()

    window.show()
    sys.exit(app.exec())