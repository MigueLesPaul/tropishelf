#!/usr/bin/env python

from PyQt5.QtWidgets import QScrollArea, QWidget, QRubberBand
from PyQt5.QtCore import pyqtSignal, QRect, QSize


class PageScrollArea(QScrollArea):
    reachbottom = pyqtSignal()
    reachtop = pyqtSignal()
    areaSelected = pyqtSignal(QRect)

    def __init__(self, parent):
        super().__init__(parent)

    def wheelEvent(self, event):
        super().wheelEvent(event)
        if self.verticalScrollBar().value() == self.verticalScrollBar(
        ).maximum() and event.angleDelta().y() == -120:
            self.reachbottom.emit()

        if self.verticalScrollBar().value() == 0 and event.angleDelta().y(
        ) == 120:
            self.reachtop.emit()

    def mousePressEvent(self, event):
        self.rubberorigin = event.pos()

        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        self.rubberband.setGeometry(QRect(self.rubberorigin, QSize()))
        self.rubberband.show()
      

    def mouseReleaseEvent(self, event):
        rect = QRect(self.rubberband.pos(), self.rubberband.size())
        self.areaSelected.emit(rect)
        self.rubberband.hide()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.rubberband.setGeometry(
            QRect(self.rubberorigin, event.pos()).normalized())

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if self.verticalScrollBar().value() == self.verticalScrollBar(
        ).maximum() and (event.key() == 16777237 or event.key() == 16777239):
            self.reachbottom.emit()
        if self.verticalScrollBar().value() == 0 and (
                event.key() == 16777235 or event.key() == 16777238):
            self.reachtop.emit()
