from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel
)

class Legend(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.Layout = QGridLayout()
        self.Layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("test")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.Layout.addWidget(self.label)

        self.setLayout(self.Layout)
        self.setStyleSheet("background-color:green;")

    def sizeHint(self):
        return QSize(320, 200)