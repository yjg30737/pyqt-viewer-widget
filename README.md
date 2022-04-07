# pyqt-viewer-widget
PyQt viewer widget

## Requirements
PyQt5 >= 5.8

## Overview
This is image viewer widget, not an application itself. But you can make image viewer application out of this.

For example, apps below are using this efficiently.

* <a href="https://github.com/yjg30737/pyqt-comic-viewer.git">pyqt-comic-viewer</a> - Comic reading app 
* <a href="https://github.com/yjg30737/pyqt-html-viewer.git">pyqt-html-viewer</a> - HTML viewer app
* <a href="https://github.com/yjg30737/pyqt-svg-viewer.git">pyqt-svg-viewer</a> - SVG viewer app

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-viewer-widget.git --upgrade```

## Included Package
* <a href="https://github.com/yjg30737/pyqt-toast.git">pyqt-toast</a> - to notify user the very beginning/last page when flip the page
* <a href="https://github.com/yjg30737/pyqt-fitting-graphics-view.git">pyqt-fitting-graphics-view</a> - main view

## Feature
* `setExtensions(extensions: list)` to set file extensions to show on the view (e.g. ['.html'])
* `addFilenames(filenames: list, cur_filename: str)` - Add filenames. ```cur_filename``` is file's name which you want to set as current file.
* `setFilenames(filenames: list, cur_filename: str)`. - Clear file list before adding files.
* `setCurrentIndex(idx: int)`, `getCurrentIndex() -> int`. The latter one can be used for checking at least one file exists or not.
* `setCurrentFilename(filename: str)`, `getCurrentFilename() -> str`.
* `clear()`
* Flip the page back and forth with prev, next button on bottom navigation widget, mouse wheel, left and right pad of keyboards.
* Being able to check the current page
* Being able to toggle the visibility of the bottom widget
* Give the emitting signal when clicked prev, next, close buttons: ```prevSignal(), nextSignal(), closeSignal()```
* When you've got the absoulte beginning/last of the files list, toast(<a href="https://github.com/yjg30737/pyqt-toast.git">pyqt-toast</a>) will show up. You can get either direction of toast with ```getFirstPageToast```, ```getLastPageToast``` to change the toast's style such as font, color.
* `setView(view: QWidget)`, `getView() -> QWidget`
* `setBottomWidgetVisible(f: bool)` to toggle the visibility of bottom navigation bar. 
* `getFirstPageToast() -> Toast`, `getLastPageToast() -> Toast`
* `setWindowTitleBasedOnCurrentFileEnabled(f: bool, prefix: str)` to set the title based on current file like "Prefix - def.png" if current file of viewer is "def.png". You can activate the feature by giving `True` to first argument `f`. You can give the default window title to `prefix`.
* `isWindowTitleBasedOnCurrentFileEnabled() -> bool`
* `removeSomeFilesFromViewer(filenames_to_remove: list)` is used when you want to remove some files in viewer, not all files. If `filenames_to_remove` includes the file name which was not included in list, error will be occured.
* `setHome(widget: QWidget)` to set home page widget, `goHome()`.

## Simple Example
Code Example (Extremely basic image viewer)
```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from pyqt_viewer_widget import ViewerWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__viewerWidget = ViewerWidget()
        self.__viewerWidget.setFilenames(['viewerWidgetExampleImagesDir']) # directory name which contains a bunch of files
        self.__viewerWidget.closeSignal.connect(self.__bottomWidgetClosed)

        self.setCentralWidget(self.__viewerWidget)
        self.__setToolBar()

    def __setToolBar(self):
        self.__bottomWidgetToggleBtn = QPushButton('Show')
        self.__bottomWidgetToggleBtn.setCheckable(True)
        self.__bottomWidgetToggleBtn.setChecked(True)
        self.__bottomWidgetToggleBtn.toggled.connect(self.__viewerWidget.setBottomWidgetVisible)

        fileToolbar = self.addToolBar('File')
        fileToolbar.addWidget(self.__bottomWidgetToggleBtn)
        fileToolbar.setMovable(False)
        
    def __bottomWidgetClosed(self):
        self.__bottomWidgetToggleBtn.setChecked(False)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
```

Result

https://user-images.githubusercontent.com/55078043/145040849-0c7326ed-e043-4a8b-8c55-c9b7e1d1756e.mp4

Note: This is result of very first version.
