#!/usr/bin/env python

from PyQt5.QtWidgets import QScrollArea, QWidget
from PyQt5.QtCore import pyqtSignal


class PageScrollArea(QScrollArea):
    reachbottom = pyqtSignal()
    reachtop = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

    def wheelEvent(self, event):
        super().wheelEvent(event)
        if self.verticalScrollBar().value() == self.verticalScrollBar(
        ).maximum() and event.angleDelta().y() == -120:
            self.reachbottom.emit()
        # print(self.verticalScrollBar().value())
        print(event.angleDelta().y())
        if self.verticalScrollBar().value() == 0 and event.angleDelta().y(
        ) == 120:
            self.reachtop.emit()

    def mousePressEvent(self, event):

        print(event)

    def mouseReleaseEvent(self, event):
        print(event)