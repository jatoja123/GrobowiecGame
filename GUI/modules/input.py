from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)

DEFAULT_COLOR = QColor(0, 126, 167)

class Button():
    def __init__(self, text, color=DEFAULT_COLOR, icon=None, uses=-1, size=57):
        super().__init__()
        self.uses = uses
        self.button = QPushButton()
        self.button.setFixedSize(size, size)
        self.button.setStyleSheet(f'background-color:{color.name()}')

        if icon: 
            self.button.setIcon(QIcon(f'C:\Dev\GrobowiecGame\GUI\icons\{icon}'))
            self.button.setIconSize(QSize(int(size-30), int(size-30)))
        else:
            self.button.setText(text)
        if self.uses == 0: self.setDisabled(True)
        if text:
            self.button.setToolTip(text)
            self.button.setToolTipDuration(2000)

    def getUses(self):
        return self.uses
    
    def setDisabled(self, state=True):
        self.button.setDisabled(True)
    
    def onPress(self):
        if self.uses > 0: self.uses -= 1
        if self.uses == 0: self.setDisabled(True)

class Input(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.outerLayout = QGridLayout()
        self.forwardLayout = QVBoxLayout()
        self.backwardsLayout = QVBoxLayout()
        self.rightLayout = QHBoxLayout()
        self.leftLayout = QHBoxLayout()

        self.outerLayout.setContentsMargins(0, 0, 0, 0)

        self.btnUP = Button(text="Up")
        self.btnUP2 = Button(text="Up x2")
        self.btnL = Button(text="Left")
        self.btnL2 = Button(text="Left x2")
        self.btnR = Button(text="Right")
        self.btnR2 = Button(text="Right x2")
        self.btnD = Button(text="Down")
        self.btnD2 = Button(text="Down x2")
        self.btnMap = Button(text="Map", uses=2, size=120)
        self.btnCps = Button(text="Compass", uses=1, size=120)
        self.btnHmr = Button(text="Hammer", uses=1, size=120, icon="hammer.png")
        self.btnOK = Button(text="OK", icon="hammer.png", color=QColor(50, 200, 50))
        
        self.buttons = [
            self.btnUP,
            self.btnUP2,
            self.btnL,
            self.btnL2,
            self.btnR,
            self.btnR2,
            self.btnD,
            self.btnD2,
            self.btnMap,
            self.btnCps,
            self.btnHmr,
            self.btnOK,
        ]

        self.forwardLayout.addWidget(self.btnUP2.button)
        self.forwardLayout.addWidget(self.btnUP.button)

        self.leftLayout.addWidget(self.btnL2.button)
        self.leftLayout.addWidget(self.btnL.button)

        self.backwardsLayout.addWidget(self.btnD.button)
        self.backwardsLayout.addWidget(self.btnD2.button)

        self.rightLayout.addWidget(self.btnR.button)
        self.rightLayout.addWidget(self.btnR2.button)

        self.outerLayout.addWidget(self.btnOK.button, 1, 1)
        self.outerLayout.addWidget(self.btnCps.button, 0, 0)
        self.outerLayout.addWidget(self.btnMap.button, 0, 2)
        self.outerLayout.addWidget(self.btnHmr.button, 2, 2)

        self.outerLayout.addLayout(self.forwardLayout, 0, 1)
        self.outerLayout.addLayout(self.backwardsLayout, 2, 1)
        self.outerLayout.addLayout(self.leftLayout, 1, 0)
        self.outerLayout.addLayout(self.rightLayout, 1, 2)

        self.setLayout(self.outerLayout)
        self.setStyleSheet(f'background-color:{DEFAULT_COLOR.name()}')

    def sizeHint(self):
        return QSize(320, 320)