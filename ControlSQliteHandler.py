#!/bin/usr/env python
# -*- coding: utf-8 -*-


"""
TODO:
   Add Menu
   Enhance TableView
   Writer Handler
   Update Option
"""
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QHeaderView
from ViewSQLiteHandler import Ui_MainWindow
from SQLiteConnector import SQLiteConnector

import sys

class SQLiteHandler(QMainWindow):

   def __init__(self):
      super(SQLiteHandler, self).__init__()
      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)
      self.show()

      self.openDataBase("cocktails")
      #self.getDataBase()




   def getDataBase(self):
      filePath = QFileDialog.getOpenFileName(filter = u'SQLite File (*.db)')
      if filePath:
         self.openDataBase(filePath)

   def openDataBase(self, filename = None):
      self.currFilename = filename
      self.sqliteConnector = SQLiteConnector(self.currFilename)
      if not self.sqliteConnector.connection:
         QMessageBox.critical(self,
               "Error",
               u'The file cannot be opened')

      else:
         self.showTableNames()

   def showTableNames(self):
      tables_names = self.sqliteConnector.getTableNames()
      if len(tables_names) > 0:
         tempTablesDialog, output = QInputDialog.getItem(self,
               "Tables available in " + self.currFilename,
               "",
               tables_names,
               current = 0,
               editable = False) 

         if output:
            self.openTable(tempTablesDialog)

      else:
         QMessageBox.critical(self, "Error", u'There are no tables registered in ' + self.currFilename)

   def openTable(self, tableName):
      #Get Header Names
      self.columnNames = self.sqliteConnector.getColumnNames(tableName)
      if len(self.columnNames) > 0:
         self.setupTableHeaders()
         self.ui.tableWidget.clearContents()

         #Get query data
         searchResult = self.sqliteConnector.getCompleteData(tableName)
         row = 0
         while searchResult.next():
            self.ui.tableWidget.setRowCount(row + 1)
            for column in range(len(self.columnNames)):
               temp = searchResult.value(column).toString()
               item = QTableWidgetItem(temp)
               self.ui.tableWidget.setItem(row, column, item)
            row += 1
         self.ui.tableWidget.setRowCount(row + 1)






   def setupTableHeaders(self):
        self.ui.tableWidget.setColumnCount(len(self.columnNames))
        self.ui.tableWidget.setHorizontalHeaderLabels(self.columnNames)
        currTableHeaders = self.ui.tableWidget.horizontalHeader()
        currTableHeaders.setResizeMode(QHeaderView.Stretch)        









def main():
   app = QApplication(sys.argv)
   sqliteHandler = SQLiteHandler()
   sys.exit(app.exec_())

if __name__ == "__main__":
   main()
