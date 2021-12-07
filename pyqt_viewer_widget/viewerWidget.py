import os
import sys

from PyQt5.QtGui import QKeySequence, QPixmap
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, \
    QApplication, QGridLayout, QPushButton, QHBoxLayout, QLabel, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QPoint, pyqtSignal, Qt

from pyqt_viewer_widget.viewerGraphicsView import ViewerGraphicsView


class ViewerWidget(QWidget):
    prevSignal = pyqtSignal()
    nextSignal = pyqtSignal()
    closeSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.__initUi()
        self.__lst = []
        self.__cur_idx = 0
        self.setMouseTracking(True)

    def __initUi(self):
        self.__page_text = 'Page: {0}'
        self.__pageLabel = QLabel(self.__page_text.format(''))
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

        self.__graphicsView = ViewerGraphicsView()

        self.__topWidget = QStackedWidget()
        self.__topWidget.addWidget(self.__graphicsView)

        lay = QVBoxLayout()
        lay.addWidget(self.__topWidget)
        lay.addWidget(self.__bottomWidget)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setLayout(lay)

    def set_lst_to_view(self, lst, idx=0):
        self.__lst = lst
        self.__btn_toggled()
        self.__graphicsView.set_filenames(self.__lst)
        self.__graphicsView.set_index(idx)

    def set_start_page(self, widget):
        self.__start_page = widget

    def get_prev(self):
        return self.__prevBtn

    def get_next(self):
        return self.__nextBtn

    def get_top_widget(self):
        return self.__topWidget

    def get_bottom_widget(self):
        return self.__bottomWidget

    def get_top_widgets_count(self):
        lay = self.layout().itemAt(0).widget().layout()
        if lay:
            return lay.count()
        else:
            return 1
    
    def set_cur_idx(self, idx):
        self.__cur_idx = idx

    def get_cur_idx(self):
        return self.__cur_idx

    def __btn_toggled(self):
        idx = self.get_cur_idx()
        self.__prevBtn.setEnabled(idx > 0)
        self.__nextBtn.setEnabled(idx < len(self.__lst)-2)

    def _prev(self):
        limit = 0
        self.__cur_idx = self.get_cur_idx()
        if self.__cur_idx > limit:
            self.__cur_idx -= 1
            self.__graphicsView.set_index(self.__cur_idx)
            self.__btn_toggled()
            self.prevSignal.emit()
            return 0
        return -1

    def _next(self):
        limit = len(self.__lst)-2
        self.__cur_idx = self.get_cur_idx()
        if self.__cur_idx < limit:
            self.__cur_idx += 1
            self.__graphicsView.set_index(self.__cur_idx)
            self.__btn_toggled()
            self.nextSignal.emit()
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

    def bottomWidgetToggled(self, f: bool):
        self.__bottomWidget.setVisible(f)

    def __close(self):
        self.closeSignal.emit(False)
        
        
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    viewerWidget = ViewerWidget()
    lst = [os.path.join('짱 45', filename) for filename in os.listdir('짱 45')]
    viewerWidget.set_lst_to_view(lst)
    viewerWidget.show()
    app.exec_()