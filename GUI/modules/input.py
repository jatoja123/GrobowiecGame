from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)

BG_COLOR = QColor(0, 23, 31) #SAME AS IN main.py!!!
TEXT_COLOR = QColor(197, 202, 212)

DEFAULT_COLOR = QColor(0, 126, 167)
DISABLED_COLOR = QColor(50, 126, 167)
PRESSED_COLOR = QColor(0, 52, 105)
CONFIRM_COLOR = QColor(0, 126, 50)
HOVER_COLOR = QColor(59, 148, 196)
PRESSED_HOVER = QColor(0, 77, 153)
CONFIRM_HOVER = QColor(0, 166, 65)

class ConfirmButton():
    def __init__(self, parent, text, icon=None, size=57):
        super().__init__()
        self.parent = parent
        self.size = size
        self.button = QPushButton()
        self.button.setFixedSize(size, size)

        if icon: 
            self.button.setIcon(QIcon(f'./GUI/icons/{icon}'))
            self.button.setIconSize(QSize(int(self.size), int(self.size)))
        else:
            self.button.setText(text)
        if text:
            self.button.setToolTip(text)
            self.button.setToolTipDuration(2000)

        self.button.setStyleSheet('''
            QPushButton {
                background: '''+CONFIRM_COLOR.name()+''';
                color: '''+TEXT_COLOR.name()+''';
                border-color: '''+TEXT_COLOR.name()+''';
                border: 0px 0px 0px 0px;
                border-style: outset;
                border-radius: 5px;
                font-size: 15px;
                font-weight: bold;
                width: 2px;
            }

            QPushButton:hover {
                background-color: '''+CONFIRM_HOVER.name()+''';
            }

            QPushButton:pressed {
                outline: 2px;
                font-size: 14px;
                border-radius: 7px;
                outline-style: solid;
                outline-color: '''+BG_COLOR.name()+''';
                border-color: '''+CONFIRM_HOVER.name()+''';
                border: 0px 0px 0px 0px;
                border-style: outset;
                font-weight: bold;
                width: 2px;
            }
        ''')

    def onPress(self):
        self.parent.parent.InputMove(self.parent.getPressedOrder())
        print(self.parent.getPressedOrder())
        self.parent.resetOrder()
        for btn in self.parent.buttons:
            btn.resetState()

class Button():
    def __init__(self, parent, Id, text, icon=None, uses=-1, size=57):
        super().__init__()
        self.size = size-27
        self.id = Id
        self.uses = uses
        self.parent = parent
        self.pressed = False
        self.button = QPushButton()
        self.button.setFixedSize(size, size)

        self.pressedStyle = '''
            QPushButton {
                outline: 2px;
                font-size: 14px;
                border-radius: 7px;
                outline-style: solid;
                outline-color: '''+BG_COLOR.name()+''';
                background-color: '''+PRESSED_COLOR.name()+''';
                color: '''+TEXT_COLOR.name()+''';
                border-color: '''+TEXT_COLOR.name()+''';
                border: 0px 0px 0px 0px;
                border-style: outset;
                font-weight: bold;
                width: 2px;
            }

            QPushButton:hover {
                background-color: '''+PRESSED_HOVER.name()+''';
            }

            QPushButton:disabled {
                background-color: '''+DISABLED_COLOR.name()+''';
            }
        '''

        self.notPressedStyle = '''
            QPushButton {
                background: #007EA7;
                color: '''+TEXT_COLOR.name()+''';
                border-color: '''+TEXT_COLOR.name()+''';
                border: 0px 0px 0px 0px;
                border-style: outset;
                border-radius: 5px;
                font-size: 15px;
                font-weight: bold;
                width: 2px;
            }

            QPushButton:hover {
                background-color: '''+HOVER_COLOR.name()+''';
            }

            QPushButton:disabled {
                background-color: '''+DISABLED_COLOR.name()+''';
            }
        '''

        self.button.setStyleSheet(self.notPressedStyle)

        if icon: 
            self.button.setIcon(QIcon(f'./GUI/icons/{icon}'))
            self.button.setIconSize(QSize(int(self.size), int(self.size)))
        else:
            self.button.setText(text)
        if self.uses == 0: self.setDisabled(True)
        if text:
            self.button.setToolTip(text)
            self.button.setToolTipDuration(2000)

    def getId(self):
        return self.id

    def getUses(self):
        return self.uses
    
    def getState(self):
        return self.pressed
    
    def resetState(self):
        self.pressed = False
        self.button.setStyleSheet(self.notPressedStyle)
    
    def setDisabled(self, state=True):
        self.button.setDisabled(True)
    
    def onPress(self):
        if self.pressed:
            self.pressed = False
            self.parent.releaseBtn(self) #remove button from queue
            self.button.setStyleSheet(self.notPressedStyle)
            self.button.setIconSize(QSize(int(self.size), int(self.size)))
        else:
            self.pressed = True
            self.parent.pressBtn(self) #add button to queue
            self.button.setStyleSheet(self.pressedStyle)
            self.button.setIconSize(QSize(int(self.size-2), int(self.size-2)))



class Input(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.outerLayout = QGridLayout()
        self.forwardLayout = QVBoxLayout()
        self.backwardsLayout = QVBoxLayout()
        self.rightLayout = QHBoxLayout()
        self.leftLayout = QHBoxLayout()

        self.outerLayout.setContentsMargins(0, 0, 0, 0)

        btnUP = Button(parent=self, text="Up", Id="W")
        btnUP2 = Button(parent=self, text="Up x2", Id="WW")
        btnL = Button(parent=self, text="Left", Id="A")
        btnL2 = Button(parent=self, text="Left x2", Id="AA")
        btnR = Button(parent=self, text="Right", Id="D")
        btnR2 = Button(parent=self, text="Right x2", Id="DD")
        btnD = Button(parent=self, text="Down", Id="S")
        btnD2 = Button(parent=self, text="Down x2", Id="SS")
        btnMap = Button(parent=self, text="Map", uses=2, size=120, Id="M")
        btnCps = Button(parent=self, text="Compass", uses=1, size=120, Id="R")
        btnHmr = Button(parent=self, text="Hammer", uses=2, size=120, icon="hammer.png", Id="H")
        self.btnOK = ConfirmButton(parent=self, text="OK")
        
        self.pressOrder = []
        self.buttons = [
            btnUP,
            btnUP2,
            btnL,
            btnL2,
            btnR,
            btnR2,
            btnD,
            btnD2,
            btnMap,
            btnCps,
            btnHmr,
        ]

        self.btnOK.button.pressed.connect(self.btnOK.onPress)
        for btn in self.buttons:
            btn.button.pressed.connect(btn.onPress)

        self.forwardLayout.addWidget(btnUP2.button)
        self.forwardLayout.addWidget(btnUP.button)

        self.leftLayout.addWidget(btnL2.button)
        self.leftLayout.addWidget(btnL.button)

        self.backwardsLayout.addWidget(btnD.button)
        self.backwardsLayout.addWidget(btnD2.button)

        self.rightLayout.addWidget(btnR.button)
        self.rightLayout.addWidget(btnR2.button)

        self.outerLayout.addWidget(self.btnOK.button, 1, 1)
        self.outerLayout.addWidget(btnCps.button, 0, 0)
        self.outerLayout.addWidget(btnMap.button, 0, 2)
        self.outerLayout.addWidget(btnHmr.button, 2, 2)

        self.outerLayout.addLayout(self.forwardLayout, 0, 1)
        self.outerLayout.addLayout(self.backwardsLayout, 2, 1)
        self.outerLayout.addLayout(self.leftLayout, 1, 0)
        self.outerLayout.addLayout(self.rightLayout, 1, 2)

        self.setLayout(self.outerLayout)

    def sizeHint(self):
        return QSize(320, 320)
    
    def disableAll(self):
        for btn in self.buttons:
            btn.setDisabled(True)

    def getPressedOrder(self):
        return self.pressOrder
    
    def pressBtn(self, btn):
        self.pressOrder.append(btn.getId())

    def releaseBtn(self, btn):
        self.pressOrder.remove(btn.getId())

    def resetOrder(self):
        self.pressOrder = []