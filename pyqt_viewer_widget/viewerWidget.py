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
    clearSignal = pyqtSignal()
    closeSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__filenames = []
        self.__cur_idx = 0

        self.__extensions = []
        self.__windowTitlePrefix = ''
        self.__window_title_based_on_current_file_flag = False

    def __resetVal(self):
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

        self.__prevBtn.clicked.connect(self._prev)
        self.__nextBtn.clicked.connect(self._next)
        self.__closeBtn.clicked.connect(self.__close)

        self._home = QWidget()
        self._view = FittingGraphicsView()

        self.__topWidget = QStackedWidget()
        self.__topWidget.addWidget(self._home)
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

        self.setCurrentIndex(0)

    def __setOrdered(self, filenames: list):
        # temporary measure
        try:
            # sorted by number
            return sorted(filenames, key=lambda f: int(re.sub(r'\D', '', f)))
        except Exception as e:
            # sorted by string
            return sorted(filenames)

    def isWindowTitleBasedOnCurrentFileEnabled(self) -> bool:
        return self.__window_title_based_on_current_file_flag

    def setWindowTitleBasedOnCurrentFileEnabled(self, f: bool, prefix: str = ''):
        self.__window_title_based_on_current_file_flag = f
        if self.__window_title_based_on_current_file_flag:
            self.__windowTitlePrefix = prefix

    def setExtensionsExceptForImage(self, extensions: list):
        self.__extensions = extensions

    def setHome(self, home_widget: QWidget):
        self.__topWidget.removeWidget(self._home)
        self._home = home_widget
        self.__topWidget.addWidget(self._home)

    def goHome(self):
        self.__topWidget.setCurrentWidget(self._home)

    def setView(self, view: QWidget):
        self.__topWidget.removeWidget(self._view)
        self._view = view
        self.__topWidget.addWidget(self._view)

    def getView(self) -> QWidget:
        return self._view

    def setCurrentIndex(self, idx):
        self.__cur_idx = idx
        if len(self.__filenames) == 0:
            self.clearSignal.emit()
            self.goHome()
        else:
            self._view.setFilename(self.__filenames[idx])
            self.__topWidget.setCurrentWidget(self._view)
        self.__execSettingPageWork()

    def getCurrentIndex(self) -> int:
        return self.__cur_idx

    def setCurrentFilename(self, filename: str):
        idx = self.__filenames.index(filename)
        self.setCurrentIndex(idx)

    def getCurrentFilename(self):
        if len(self.__filenames) <= self.__cur_idx:
            return ''
        else:
            return self.__filenames[self.__cur_idx]

    def setFilenames(self, filenames: list, cur_filename: str):
        self.__resetVal()
        self.addFilenames(filenames, cur_filename)

    def addFilenames(self, filenames: list, cur_filename: str):
        filenames = self.__setOrdered(filenames)
        if os.path.isdir(cur_filename):
            idx = 0
        else:
            idx = filenames.index(cur_filename)
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
                else:
                    if len(self.__extensions) > 0:
                        if os.path.splitext(filename)[-1] in self.__extensions:
                            self.__filenames.append(filename)

        if len(self.__filenames) > 0:
            self.setCurrentIndex(idx)

    def getFilenames(self) -> list:
        return self.__filenames

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
        self.__prevBtn.setEnabled(self.__cur_idx > 0)
        self.__nextBtn.setEnabled(self.__cur_idx < len(self.__filenames)-1)

    def _prev(self):
        if self.__prevBtn.isEnabled():
            self.setCurrentIndex(self.__cur_idx-1)
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
            self.setCurrentIndex(self.__cur_idx+1)
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
        if self.isWindowTitleBasedOnCurrentFileEnabled():
            self.__setWindowTitleBasedOnCurrentFileName()

    def __setPageLabel(self):
        cur_page = min(len(self.__filenames), self.__cur_idx + 1)
        self.__pageLabel.setText(self.__page_label_text.format(cur_page, len(self.__filenames)))

    def __setWindowTitleBasedOnCurrentFileName(self):
        if self.getCurrentFilename():
            self.window().setWindowTitle(self.__windowTitlePrefix + ' - ' + os.path.basename(self.getCurrentFilename()))
        else:
            self.window().setWindowTitle(self.__windowTitlePrefix)

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

    def removeSomeFilesFromViewer(self, filenames_to_remove: list):
        cur_idx = self.getCurrentIndex()
        filenames = self.getFilenames()
        maintain_cur_idx_if_cur_idx_file_still_remain = filenames[cur_idx] in filenames_to_remove

        self.__cur_idx = max(0, filenames.index(filenames_to_remove[0])-1)
        for filename in filenames_to_remove:
            filenames.remove(filename)
        self.setCurrentIndex(self.__cur_idx)