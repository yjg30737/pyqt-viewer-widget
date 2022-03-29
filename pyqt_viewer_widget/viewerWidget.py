import os, re

from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QGridLayout, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

from PIL import Image
from pyqt_toast import Toast

from pyqt_fitting_graphics_view.fittingGraphicsView import FittingGraphicsView


class ViewerWidget(QWidget):
    prevSignal = pyqtSignal()
    nextSignal = pyqtSignal()
    closeSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__filenames = []
        self.__cur_idx = 0

    def __initUi(self):
        self.setMouseTracking(True)

        self.__page_label_prefix = 'Page: '
        self.__page_label_text = self.__page_label_prefix + '{0}/{1}'
        self.__pageLabel = QLabel(self.__page_label_prefix)
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

        self._view = FittingGraphicsView()

        self.__topWidget = QStackedWidget()
        self.__topWidget.addWidget(self._view)

        lay = QVBoxLayout()
        lay.addWidget(self.__topWidget)
        lay.addWidget(self.__bottomWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

        self.__firstPageToast = Toast(text='This is the first page.', close_sec=2, parent=self)
        self.__lastPageToast = Toast(text='This is the last page.', close_sec=2, parent=self)

        self.__firstPageToast.setFont(QFont('Arial', 20))
        self.__lastPageToast.setFont(QFont('Arial', 20))

        self.__btnToggled()

    def __setOrdered(self, filenames: list):
        # temporary measure
        try:
            # sorted by number
            return sorted(filenames, key=lambda f: int(re.sub(r'\D', '', f)))
        except Exception as e:
            # sorted by string
            return sorted(filenames)

    def setView(self, view: QWidget):
        self.__topWidget.removeWidget(self._view)
        self._view = view
        self.__topWidget.addWidget(self._view)

    def getView(self) -> QWidget:
        return self._view

    def setCurrentFilename(self, idx):
        self.__cur_idx = idx
        self._view.setFilename(self.__filenames[idx])

    def getCurrentFilename(self):
        if len(self.__filenames) <= self.__cur_idx:
            return ''
        else:
            return self.__filenames[self.__cur_idx]

    def setFilenames(self, filenames: list, cur_filename: str):
        filenames = self.__setOrdered(filenames)
        if os.path.isdir(cur_filename):
            idx = 0
        else:
            idx = filenames.index(cur_filename)
        self.__initVal()

        for filename in filenames:
            if os.path.isdir(filename):
                dirname = filename
                filenames_in_dir = self.__setOrdered(os.listdir(dirname))
                image_filenames = [os.path.join(dirname, file_in_dir) for file_in_dir in filenames_in_dir
                                   if self.__isImageFile(os.path.join(filename, file_in_dir))]
                self.__filenames.extend(image_filenames)
            else:
                if self.__isImageFile(filename):
                    self.__filenames.append(filename)

        if len(self.__filenames) > 0:
            self.setCurrentFilename(idx)

        self.__execSettingPageWork()

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
        self.__nextBtn.setEnabled(idx < len(self.__filenames) - 1)

    def _prev(self):
        if self.__prevBtn.isEnabled():
            self.setCurrentFilename(self.__cur_idx-1)
            self.__execSettingPageWork()
            self.prevSignal.emit()
            return 0
        else:
            if self.__isAnyToastVisible():
                pass
            else:
                self.__firstPageToast.show()
            return -1

    def _next(self):
        if self.__nextBtn.isEnabled():
            self.setCurrentFilename(self.__cur_idx+1)
            self.__execSettingPageWork()
            self.nextSignal.emit()
            return 0
        else:
            if self.__isAnyToastVisible():
                pass
            else:
                self.__lastPageToast.show()
            return -1

    def __execSettingPageWork(self):
        self.__btnToggled()
        self.__setPageLabel()
        self.__setWindowTitleBasedOnCurrentFileName()

    def __setPageLabel(self):
        self.__pageLabel.setText(self.__page_label_text.format(self.__cur_idx + 1, len(self.__filenames)))

    def __setWindowTitleBasedOnCurrentFileName(self):
        self.window().setWindowTitle(self.getCurrentFilename())

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
        filename = self.getCurrentFilename()
        if filename:
            if e.angleDelta().y() < 0:
                self._next()
            else:
                self._prev()
        return super().wheelEvent(e)

    def setBottomWidgetVisible(self, f: bool):
        self.__bottomWidget.setVisible(f)

    def __isAnyToastVisible(self):
        return self.__firstPageToast.isVisible() or self.__lastPageToast.isVisible()

    def __close(self):
        self.__bottomWidget.setVisible(False)
        self.closeSignal.emit()

    def getFirstPageToast(self):
        return self.__firstPageToast

    def getLastPageToast(self):
        return self.__lastPageToast