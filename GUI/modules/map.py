from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton
)

class Map(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.Layout = QGridLayout()
        self.Layout.setContentsMargins(0, 0, 0, 0)


        self.label = QLabel("Mapa")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.Layout.addWidget(self.label)

        self.setStyleSheet("background-color:gray;")
        self.setLayout(self.Layout)

    def calculateBlobs(self, map):
        pass
    # returns:
    # [{
    #   cornerField - {x, y} #coordinates of upper-left corner field
    #   height: num
    #   width: num
    # }]
    
    def calculatePositions(self, blobs):
        pass
    # returns:
    # [{
    #   blob: blob
    #   gridPos: (num, num)
    # }]

    def drawMap(self, map):
        blobs = self.calculatePositions(self.calculateBlobs(map))

        for blob in blobs:
            innerGrid = QGridLayout()

            cornerX = blob.blob.cornerField.x
            cornerY = blob.blob.cornerField.y

            for x in range(cornerX, cornerX+blob.blob.width-1):
                for y in range(cornerY, cornerY+blob.blob.height-1):
                    if map[x][y].isDiscovered(): innerGrid.addWidget(QPushButton().setIcon(QIcon(f'C:\Dev\GrobowiecGame\GUI\icons\{map[x][y].getIcon()}')), x-cornerX, y-cornerY)
            
            self.Layout.addLayout(innerGrid, blob.gridPos)
    
    #Potrzebne funckje: getIcon() w 'map', isDiscovered() w 'map' calculateBlobs(map) -> calculatePositions(blobs), 

    def sizeHint(self):
        return QSize(300, 600)