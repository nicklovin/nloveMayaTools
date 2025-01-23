from PySide2 import QtWidgets, QtCore, QtGui

NORMAL, DOWN, DISABLED = 1, 2, 3
INNER, OUTER = 1, 2


class ShelfButton(QtWidgets.QPushButton):

    def __init__(self, icon=None, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)
        self.setFixedHeight(50)
        self.setFixedWidth(50)
        try:
            self.setIcon(icon)
            self.setIconSize(QtCore.QSize(50, 50))
        except TypeError:
            pass