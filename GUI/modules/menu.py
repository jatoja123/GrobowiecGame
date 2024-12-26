from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit, QPushButton, QWidget
)

class Menu(QWidget):
    def __init__(self, window, parent=None):
        super().__init__(parent=None)
        self.Layout = QGridLayout()
        self.Layout.setContentsMargins(0, 0, 0, 0)

        self.window = window

        self.label = QLabel("lewo")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        

        # Line edit with a parent widget and a default text
        self.bottom_line_edit = QLineEdit(
            "Hello! This is a line edit.", parent=self
        )

        self.button = QPushButton("Click me")
        self.button.clicked.connect(self.btn)

        self.Layout.addWidget(self.label)
        self.Layout.addWidget(self.bottom_line_edit)
        self.Layout.addWidget(self.button)

        self.setStyleSheet("background-color:red;")
        self.setLayout(self.Layout)
    
    def sizeHint(self):
        return QSize(50, 400)
    
    def setLabel(self, text):
        self.label.setText(text)

    def readInput(self, text):
        self.window.ReadInput(text)

    def btn(self):
        self.readInput(self.bottom_line_edit.text)