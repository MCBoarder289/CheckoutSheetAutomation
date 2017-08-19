#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
UI code tweaked from ZetCode PyQt5 tutorial

Main changes - Used Labels instead of TextEdits,
and added File and Directory selection in the FileDialog

Original Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

from PyQt5.QtWidgets import (QMainWindow, QLabel, QPushButton,
                             QAction, QFileDialog, QApplication)
from PyQt5.QtGui import (QIcon, QFont)
import sys
import Automation


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.statusBar()

        self.file_title = QLabel('PDF Location:', self)  # Title above selected file location
        font = QFont()
        font.setBold(True)  # Setting the font variable to bold
        font.setUnderline(True)  # Underlining the title font variable
        self.file_title.setFont(font)  # Setting the title object font
        self.file_title.move(15, 30)  # Placing the position in the window

        self.file_label = QLabel('', self)  # Placeholder for File Selection
        self.file_label.move(15, 40)

        self.destination_title = QLabel('Ending Location:', self)  # Title above selected destination location
        self.destination_title.setFont(font)  # Copying bold/underline font for title here
        self.destination_title.move(15, 80)

        self.destination_label = QLabel('', self)   # Placeholder for Destination Selection
        self.destination_label.move(15, 90)

        self.filename = None
        self.destinationname = None

        self.button = QPushButton('Make the Roster Sheet', self)  # Creating the push button
        self.button.setToolTip('Make sure you select the file and destination!')
        self.button.resize(self.button.sizeHint())  # Sizing the button appropriately
        self.button.move(200, 200)
        self.button.clicked.connect(self.runAutomation)  # Click action = execute runAutomation function

        # This section establishes the actions when selecting the PDF file
        openFile = QAction(QIcon('open.png'), 'Get Target File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Select PDF File')
        openFile.triggered.connect(self.showFile)  # When selected, it triggers the showFile function

        # This section establishes the actions when selecting the target destination folder
        saveFile = QAction(QIcon('open.png'), 'Set Destination', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Set Export Destination ')
        saveFile.triggered.connect(self.showDestination)  # When selected, it triggers the showDestination function

        menubar = self.menuBar()  # Creates Status Bar at top of Window
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)

        self.setGeometry(500, 300, 450, 300)  # Sets size of the window
        self.setWindowTitle('PDFtoExcel - Kids\' roster')
        self.show()

    def showFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Choose File', '/home')  # Opens explorer and awaits file selection

        if fname[0]:  # Once we have a name, fill it in the appropriate label and return that string
            self.file_label.setGeometry(15, 60, 300, 15)
            self.file_label.setText(fname[0])
            filename = fname[0]
            self.filename = filename  # Need to set up a variable that persists when selected

            return filename  # Need to ensure that the indent is here so that the UI doesn't crash if "canceled"

    def showDestination(self):
        dname = str(QFileDialog.getExistingDirectory(self, 'Choose Destination', '/home'))

        if dname:   # Once we have a destination folder, fill it in the appropriate label and return that string
            self.destination_label.setGeometry(15, 110, 300, 15)
            self.destination_label.setText(dname)
            destinationname = dname
            self.destinationname = destinationname
            return destinationname  # Need to ensure that the indent is here so that the UI doesn't crash if "canceled"

    def runAutomation(self):

        if self.filename and self.destinationname:  # If we have both a file and destination, run the script with those
            Automation.format_pdf_to_excel(fname=self.filename, dname=self.destinationname)
            sys.exit(app.exec_())  # Exit the app after it is run


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()  # Run this whole class, and exit when closed
    sys.exit(app.exec_())
