import sys
from PySide6 import QtWidgets
from gui import SystemTrayIcon


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(widget)
    tray_icon.spawn()

    sys.exit(app.exec_())