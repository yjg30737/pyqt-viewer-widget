# pyqt-viewer-widget
PyQt viewer widget(template)

## Requirements
PyQt5 >= 5.8

## Overview
This is image viewer widget, not an application itself. But you can make image viewer application with this. Check the example code below.

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-viewer-widget.git --upgrade```

## Included Package
* Pillow >= 9.0.0 - to check if file extension is image format or not
* <a href="https://github.com/yjg30737/pyqt-toast.git">pyqt-toast</a> - to notify user the very beginning/last page when flip the page
* <a href="https://github.com/yjg30737/pyqt-fitting-graphics-view.git">pyqt-fitting-graphics-view</a> - main view

## Feature
* Being able to show image files in certain directory by giving the directory name and image files' names as arguments to ```setFilenames(filenames: list, cur_filename: str)```. ```cur_filename``` is file's name which you want to set among the ```filenames```. ```setFilenames``` function filters the none-image files with private function using ```Image``` module in ```Pillow``` package. 
* Being able to get current filename with ```getCurrentFilename()```. This can be also used for checking at least one file exists or not.
* Flip the page with prev, next button on bottom navigation widget, mouse wheel, left and right pad of keyboards.
* Being able to check the current page
* Being able to toggle the visibility of the bottom widget
* Give the emitting signal when clicked prev, next, close buttons: ```prevSignal(), nextSignal(), closeSignal()```
* When you've got the absoulte beginning/last of the files list, toast(<a href="https://github.com/yjg30737/pyqt-toast.git">pyqt-toast</a>) will show up. You can get either direction of toast with ```getFirstPageToast```, ```getLastPageToast``` to change the toast's style such as font, color.
* `setView(view: QWidget)`, `getView() -> QWidget`

## Example
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
