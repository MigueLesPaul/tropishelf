#!/usr/bin/env python

import sys
from PyQt5 import QtCore, QtWidgets, uic, QtSql
from PyQt5.QtGui import QImage, QPixmap,QKeySequence,QStandardItemModel
from PyQt5.QtWidgets import QShortcut
from popplerqt5 import Poppler


class TropicalViewer(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('tropical-viewer.ui', self)

        self.current_page = 0
        self.set_size_percent(200)
        self.zoomFactor=1
        self.open_pdf_file(
            '/home/miguel/Documents/1996 - Fundamentals of Atmospheric Physics - SALBY.pdf'
        )

        self.reload_page()

        self.shortcut_next=QShortcut(QKeySequence('N'),self)
        self.shortcut_prev=QShortcut(QKeySequence('B'),self)
                                     
        self.shortcut_next.activated.connect(self.next_page)
        self.shortcut_prev.activated.connect(self.prev_page)




    def open_pdf_file(self, pdffile):
        self.pdfdocumentfile = pdffile
        self.document = Poppler.Document.load(self.pdfdocumentfile)
        self.document.setRenderHint(Poppler.Document.TextAntialiasing)

    def reload_page(self):
        page = Poppler.Page.renderToImage(
            self.document.page(self.current_page), self.xsize, self.ysize, 0, 0)
        image = QPixmap(page)
        self.currentpageLabel.setPixmap(image)
        self.currentpageLabel.resize(self.zoomFactor*image.size())
        self.progressBar.setValue(int(self.current_page*100/self.document.numPages()))

    def jump_to_page(self, page):
        self.current_page = page
        self.reload_page()
    
    def set_size_percent(self,perc):
        self.xsize=perc
        self.ysize=perc

    def next_page(self):
        if self.current_page != (self.document.numPages() - 1):
            self.jump_to_page(self.current_page + 1)
            self.scrollArea.verticalScrollBar().setValue(0)

    def prev_page(self):
        if self.current_page != 0:
            self.jump_to_page(self.current_page - 1)
            self.scrollArea.verticalScrollBar().setValue(5000)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TropicalViewer()
    window.show()
    sys.exit(app.exec_())