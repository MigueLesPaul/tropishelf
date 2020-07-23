#!/usr/bin/env python

import sys
from PyQt5 import QtCore, QtWidgets, uic, QtSql
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QImage,QPixmap
from popplerqt5 import Poppler

class TropicalViewer(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('tropical-viewer.ui', self)

        pdfdocumentfile='/home/miguel/Documents/1996 - Fundamentals of Atmospheric Physics - SALBY.pdf'
        
        document = Poppler.Document.load(pdfdocumentfile)
        print(document)
        page = Poppler.Page.renderToImage(document.page(34),200,200,0,0 )
        
        # image = QImage(page)
        image= QPixmap(page)
        self.label.setPixmap(image)
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window=TropicalViewer()
    window.show()
    sys.exit(app.exec_())