#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we select a file with a
QFileDialog and display its contents
in a QTextEdit.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QLabel, QPushButton,
                             QAction, QFileDialog, QApplication)
from PyQt5.QtGui import (QIcon, QFont)
import sys
import Automation


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # self.textEdit = QTextEdit()
        # self.setCentralWidget(self.textEdit)
        self.statusBar()

        self.file_title = QLabel('PDF Location:', self)
        font = QFont()
        font.setBold(True)
        font.setUnderline(True)
        self.file_title.setFont(font)
        self.file_title.move(15, 30)

        self.file_label = QLabel('', self)
        self.file_label.move(15, 40)

        self.destination_title = QLabel('Ending Location:', self)
        self.destination_title.setFont(font)
        self.destination_title.move(15, 80)

        self.destination_label = QLabel('', self)
        self.destination_label.move(15, 90)

        self.filename = None
        self.destinationname = None

        self.button = QPushButton('Make the Roster Sheet', self)
        self.button.setToolTip('Make sure you select the file and destination!')
        self.button.resize(self.button.sizeHint())
        self.button.move(200, 200)
        self.button.clicked.connect(self.runAutomation)

        openFile = QAction(QIcon('open.png'), 'Get Target File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Select PDF File')
        openFile.triggered.connect(self.showFile)

        saveFile = QAction(QIcon('open.png'), 'Set Destination', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Set Export Destination ')
        saveFile.triggered.connect(self.showDestination)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)

        self.setGeometry(500, 300, 350, 300)
        self.setWindowTitle('PDFtoExcel - Kids\' roster')
        self.show()

    def showFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Choose File', '/home')

        if fname[0]:
            self.file_label.setGeometry(15, 60, 300, 15)
            self.file_label.setText(fname[0])
            filename = fname[0]
            self.filename = filename

            return filename

    def showDestination(self):
        dname = str(QFileDialog.getExistingDirectory(self, 'Choose Destination', '/home'))

        if dname:
            self.destination_label.setGeometry(15, 110, 300, 15)
            self.destination_label.setText(dname)
            destinationname = dname
            self.destinationname = destinationname
            return destinationname

    def runAutomation(self):

        if self.filename and self.destinationname:
            Automation.format_pdf_to_excel(fname=self.filename, dname=self.destinationname)
            sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
