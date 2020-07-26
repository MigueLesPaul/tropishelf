#!/usr/bin/env python

import sys
from PyQt5 import QtCore, QtWidgets, uic, QtSql
from PyQt5.QtGui import QImage, QPixmap, QKeySequence, QStandardItemModel, QPainter, QPen
from PyQt5.QtWidgets import QShortcut, QScrollArea
from PyQt5.QtCore import QRect, QRectF
from popplerqt5 import Poppler


class TropicalViewer(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('tropical-viewer.ui', self)

        self.current_page = 0
        self.zoomFactor = 2.9
        self.set_size_percent(self.zoomFactor)
        self.open_pdf_file(
            '/home/miguel/Projects/Estadistica/Numerical_Methods_of_Statistics.pdf'
        )

        self.reload_page()

        self.shortcut_next = QShortcut(QKeySequence('N'), self)
        self.shortcut_prev = QShortcut(QKeySequence('B'), self)

        self.shortcut_next.activated.connect(self.next_page)
        self.shortcut_prev.activated.connect(self.prev_page)
        self.scrollArea.reachbottom.connect(self.scroll_bottom)
        self.scrollArea.reachtop.connect(self.scroll_top)
        self.scrollArea.areaSelected.connect(self.extract_text_from_area)
        self.numPageEdit.editingFinished.connect(self.edit_current_page)

    def open_pdf_file(self, pdffile):
        self.pdfdocumentfile = pdffile
        self.document = Poppler.Document.load(self.pdfdocumentfile)
        self.document.setRenderHint(Poppler.Document.TextAntialiasing)
        
        self.numPagesLabel.setText(str(self.document.numPages()))
        

    def reload_page(self):
        self.Poppage = self.document.page(self.current_page)
        # self.imgpage = self.Poppage.renderToImage(self.xres, self.yres, 0, 0,468,648)
        self.imgpage = self.Poppage.renderToImage(self.xres, self.yres)
        image = QPixmap(self.imgpage)
        self.pixpage = image
        self.currentpageLabel.setPixmap(image)
        self.currentpageLabel.resize(self.zoomFactor * image.size())
        self.progressBar.setValue(
            int(self.current_page * 100 / self.document.numPages()))
        
        self.numPageEdit.setText(str(self.current_page))
        self.search_page_text('computer software')  ###  testing search

    def jump_to_page(self, page):
        self.current_page = page
        self.reload_page()


    def set_size_percent(self, perc):
        self.xres = perc * 72
        self.yres = perc * 72

    def next_page(self):
        if self.current_page != (self.document.numPages() - 1):
            self.jump_to_page(self.current_page + 1)
            self.scrollArea.verticalScrollBar().setValue(0)

    def prev_page(self):
        if self.current_page != 0:
            self.jump_to_page(self.current_page - 1)
            self.scrollArea.verticalScrollBar().setValue(
                self.scrollArea.verticalScrollBar().maximum())

    def adjustRect(self, rect):
        rct = rect.getRect()
        new = []
        for p in rct:
            new.append(p * self.zoomFactor)
        return rect.setRect(new[0], new[1], new[2], new[3])

    def search_page_text(self, text):
        result = self.Poppage.search(text)

        # print(result)
        if len(result) > 0:
            for res in result:
                print(res, self.adjustRect(res))

                self.painter = QPainter(self.pixpage)
                self.pen = QPen()
                self.pen.setWidth(1)

                self.painter.setPen(self.pen)
                self.painter.drawRect(res)
                self.currentpageLabel.setPixmap(self.pixpage)
                self.painter.end()

    def search_text(self):
        pass

    def extract_text_from_area(self, rect):
        rect = self.qrect2qrectf(rect)
        print(rect)
        for box in self.Poppage.textList():
            if rect.intersects(box.boundingBox()):
                print(box.text())

    def qrect2qrectf(self, Rect):
        rec = Rect.getRect()
        recf = [float(r) for r in rec]
        result = QRectF()
        result.setRect(recf[0], recf[1], recf[2], recf[3])
        return result
    
    # Widget Response Slots 
    def scroll_bottom(self):
        self.next_page()

    def scroll_top(self):
        self.prev_page()

    def edit_current_page(self):
        self.current_page= int(self.numPageEdit.text())
        self.reload_page()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TropicalViewer()
    window.show()
    sys.exit(app.exec_())