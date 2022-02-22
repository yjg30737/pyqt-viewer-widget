from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect


class ViewerGraphicsView(QGraphicsView):
    photoClicked = pyqtSignal(QPoint)
    rectChanged = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()
        self.__filenames = []
        self.__initUi()

    def __initUi(self):
        self.__p = 0
        self.__scene = 0
        self.__graphicItem = 0

    def setFilenames(self, filenames):
        self.__filenames = filenames

    def setIndex(self, index):
        self.setFile(self.__filenames[index])

    def setPixmap(self, p):
        self.__setPixmap(p)

    def setFile(self, filename):
        self.__p = QPixmap(filename)
        self.__setPixmap(self.__p)

    def __setPixmap(self, p):
        self.__p = p
        self.__scene = QGraphicsScene()
        self.__graphicItem = self.__scene.addPixmap(self.__p)
        self.setScene(self.__scene)
        # fit in view literally
        self.fitInView(self.__graphicItem, Qt.KeepAspectRatio)
        self.show()

    def resizeEvent(self, e):
        if isinstance(self.__graphicItem, QGraphicsItem):
            self.fitInView(self.__graphicItem, Qt.KeepAspectRatio)