from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect


class ViewerGraphicsView(QGraphicsView):
    photoClicked = pyqtSignal(QPoint)
    rectChanged = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__p = 0
        self.__scene = 0
        self.__graphicItem = 0

        old_code = '''
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__prepare_menu)

    def __prepare_menu(self, pos):
        menu = QMenu(self)
        self.__fitAction = QAction('화면에 맞게 보기')
        self.__fitAction.triggered.connect(self.__fit)

        menu.addAction(self.__fitAction)
        menu.exec(self.mapToGlobal(pos))
        '''

    def __fit(self):
        # restore default transform
        if isinstance(self.__graphicItem, QGraphicsItem):
            self.fitInView(self.__graphicItem, Qt.KeepAspectRatio)

    def set_filenames(self, filenames):
        self.__filenames = filenames

    def set_index(self, index):
        self.__filenames_idx = index
        self.setFile(self.__filenames[self.__filenames_idx])

    def setPixmap(self, p):
        self.__set_pixmap(p)

    def setFile(self, filename):
        self.__p = QPixmap(filename)
        self.__set_pixmap(self.__p)

    def __set_pixmap(self, p):
        self.__p = p
        self.__scene = QGraphicsScene()
        self.__graphicItem = self.__scene.addPixmap(self.__p)
        self.setScene(self.__scene)
        # fit in view literally
        self.fitInView(self.__graphicItem, Qt.KeepAspectRatio)
        self.show()

    # def showEvent(self, e):
    #     self.fitInView(self.__graphicItem, Qt.KeepAspectRatio)

    def resizeEvent(self, e):
        if isinstance(self.__graphicItem, QGraphicsItem):
            self.fitInView(self.__graphicItem, Qt.KeepAspectRatio)