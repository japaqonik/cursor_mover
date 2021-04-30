import sys
from threadControl import MouseCoordinatorThread
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import *
from PySide6.QtCore import *

APP_NAME = "Cursor mover"
APP_ICON_PATH = "mouse.png"

TIME_LOWER_BOUND = 1
TIME_UPPER_BOUND = 60

class TimeSlider(QSlider):
    def __init__(self, parent):
        super(TimeSlider, self).__init__(Qt.Horizontal, parent)
        self.setRange(TIME_LOWER_BOUND, TIME_UPPER_BOUND)
        self.setFixedSize(200, 20)
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)
        self.setValue((TIME_UPPER_BOUND - TIME_LOWER_BOUND)/2)


class MainAppDialog(QDialog):
    def __init__(self, parent=None):
        super(MainAppDialog, self).__init__(parent)
        self.setWindowTitle(APP_NAME)
        self.setFixedSize(250, 100)
        self.setWindowIcon(QtGui.QIcon(APP_ICON_PATH))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint |
                            Qt.WindowCloseButtonHint)

        layout = QBoxLayout(QBoxLayout.TopToBottom, self)

        checkBox = QCheckBox("Enabled")
        checkBox.setCheckState(Qt.Checked)
        checkBox.stateChanged[int].connect(self._onEnabledStateChange)

        self.slider = TimeSlider(self)
        self.slider.valueChanged[int].connect(self._onSliderValueChange)

        self.sliderLabel = QLabel()
        self._updateSliderLabel(self.slider.value())

        layout.setContentsMargins(5, 5, 5, 5)

        layout.addWidget(checkBox, 0, Qt.AlignCenter)
        layout.addWidget(self.slider, 0, Qt.AlignCenter)
        layout.addWidget(self.sliderLabel, 0, Qt.AlignCenter)

        self.slider.show()
        self._startMouseCoordinatorThread()

    def _startMouseCoordinatorThread(self):
        self.mouseCoordinatorThread = MouseCoordinatorThread(
            self.slider.value())
        self.mouseCoordinatorThread.start()

    def _stopMouseCoordinatorThread(self):
        self.mouseCoordinatorThread.stop()
        self.mouseCoordinatorThread.join()

    def _isMouseCoordinatorThreadActive(self):
        return self.mouseCoordinatorThread.is_alive()

    def _updateMouseCoordinatorTime(self, newValue):
        if self._isMouseCoordinatorThreadActive():
            self.mouseCoordinatorThread.updateTime(newValue)

    def _updateSliderLabel(self, time):
        self.sliderLabel.setText(str(time) + "s")

    def _onSliderValueChange(self, value):
        self._updateSliderLabel(value)
        self._updateMouseCoordinatorTime(value)

    def _onEnabledStateChange(self, state):
        if state == Qt.Checked:
            if not self._isMouseCoordinatorThreadActive():
                self._startMouseCoordinatorThread()
        elif state == Qt.Unchecked:
            self._stopMouseCoordinatorThread()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def stopApp(self):
        self._stopMouseCoordinatorThread()


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, QtGui.QIcon(APP_ICON_PATH), parent)
        self.setToolTip(APP_NAME)
        self.mainDialog = MainAppDialog()
        menu = QtWidgets.QMenu(parent)
        open_app = menu.addAction("Open")
        open_app.triggered.connect(self.mainDialog.show)

        menu.addSeparator()

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(self._onExit)

        self.setContextMenu(menu)
        self.activated.connect(self._onTrayIconActivated)

    def _onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
            self.mainDialog.show()

    def _onExit(self, args):
        self.mainDialog.stopApp()
        sys.exit()

    def spawn(self):
        self.show()
        self.mainDialog.show()