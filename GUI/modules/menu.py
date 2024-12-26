from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel
)

class Menu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.Layout = QGridLayout()
        self.Layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("lewo")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.Layout.addWidget(self.label)

        self.setStyleSheet("background-color:red;")
        self.setLayout(self.Layout)
    
    def sizeHint(self):
        return QSize(50, 400)
    
    def setLabel(self, text):
        print("SETLABEL")
        self.label = QLabel(text)
        self.Layout.addWidget(self.label)