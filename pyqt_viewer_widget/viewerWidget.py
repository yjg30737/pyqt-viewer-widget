import os

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QGridLayout, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

from PIL import Image

from pyqt_viewer_widget.viewerGraphicsView import ViewerGraphicsView


class ViewerWidget(QWidget):
    prevSignal = pyqtSignal()
    nextSignal = pyqtSignal()
    closeSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.__initUi()
        self.__lst = []
        self.__cur_idx = 0
        self.setMouseTracking(True)

    def __initUi(self):
        self.__page_text = 'Page: {0}'
        self.__pageLabel = QLabel(self.__page_text.format('1'))
        self.__prevBtn = QPushButton('Prev')
        self.__nextBtn = QPushButton('Next')
        self.__closeBtn = QPushButton('Close')

        lay = QHBoxLayout()
        lay.addWidget(self.__prevBtn)
        lay.addWidget(self.__nextBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        btns = QWidget()
        btns.setLayout(lay)

        lay = QGridLayout()

        lay.addWidget(self.__pageLabel, 0, 0, 1, 1, alignment=Qt.AlignLeft)
        lay.addWidget(btns, 0, 1, 1, 1, alignment=Qt.AlignCenter)
        lay.addWidget(self.__closeBtn, 0, 2, 1, 1, alignment=Qt.AlignRight)
        lay.setContentsMargins(0, 0, 0, 0)

        self.__bottomWidget = QWidget()
        self.__bottomWidget.setLayout(lay)
        lay.setContentsMargins(5, 5, 5, 5)

        self.__prevBtn.clicked.connect(self._prev)
        self.__nextBtn.clicked.connect(self._next)
        self.__closeBtn.clicked.connect(self.__close)

        self._graphicsView = ViewerGraphicsView()

        self.__topWidget = QStackedWidget()
        self.__topWidget.addWidget(self._graphicsView)

        lay = QVBoxLayout()
        lay.addWidget(self.__topWidget)
        lay.addWidget(self.__bottomWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

    def setFilenames(self, filenames: list, idx=0):
        self.__lst = []

        for filename in filenames:
            if os.path.isdir(filename):
                dirname = filename
                image_filenames = [os.path.join(dirname, file_in_dir) for file_in_dir in os.listdir(dirname)
                                   if self.__isImageFile(os.path.join(filename, file_in_dir))]
                self.__lst.extend(image_filenames)
            else:
                if self.__isImageFile(filename):
                    self.__lst.append(filename)

        if len(self.__lst) > 0:
            self.__btnToggled()
            self._graphicsView.setFilenames(self.__lst)
            self._graphicsView.setIndex(idx)

    def getCurrentFilename(self):
        return self.__lst[self.__cur_idx]

    def __isImageFile(self, filename):
        res = ''
        try:
            file = Image.open(filename)
            res = file.format
        except:
            pass
        finally:
            return res

    def __btnToggled(self):
        idx = self.__cur_idx
        self.__prevBtn.setEnabled(idx > 0)
        self.__nextBtn.setEnabled(idx < len(self.__lst) - 1)

    def _prev(self):
        if self.__prevBtn.isEnabled():
            self.__cur_idx -= 1
            self._graphicsView.setIndex(self.__cur_idx)
            self.prevSignal.emit()
            self.__btnToggled()
            self.__pageLabel.setText(self.__page_text.format(self.__cur_idx + 1))
            return 0
        return -1

    def _next(self):
        if self.__nextBtn.isEnabled():
            self.__cur_idx += 1
            self._graphicsView.setIndex(self.__cur_idx)
            self.nextSignal.emit()
            self.__btnToggled()
            self.__pageLabel.setText(self.__page_text.format(self.__cur_idx + 1))
            return 0
        return -1

    def keyPressEvent(self, e):
        if (e.key() == 61 or e.matches(QKeySequence.ZoomIn)) or e.matches(QKeySequence.ZoomOut):
            self._zoom = 1
            zoom_factor = 0.04
            if e.key() == 61 or e.matches(QKeySequence.ZoomIn):
                self._zoom += zoom_factor
            else:
                self._zoom -= zoom_factor
            # self.scale(self._zoom, self._zoom)
        return super().keyPressEvent(e)

    def keyReleaseEvent(self, e):
        # 16777234 is left
        if e.key() == 16777234:
            self._prev()
        # 16777236 is right
        elif e.key() == 16777236:
            self._next()
        return super().keyReleaseEvent(e)

    def wheelEvent(self, e):
        if e.angleDelta().y() < 0:
            self._next()
        else:
            self._prev()
        return super().wheelEvent(e)

    def setBottomWidgetVisible(self, f: bool):
        self.__bottomWidget.setVisible(f)

    def __close(self):
        self.__bottomWidget.setVisible(False)
        self.closeSignal.emit()
