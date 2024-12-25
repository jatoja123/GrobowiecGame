from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel
)

class Map(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.Layout = QGridLayout()
        self.Layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("test")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.Layout.addWidget(self.label)

        self.setStyleSheet("background-color:gray;")
        self.setLayout(self.Layout)
    
    def sizeHint(self):
        return QSize(300, 400)