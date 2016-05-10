# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2016-05-07
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4.QtGui import QMessageBox, QCheckBox
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QStyledItemDelegate, QComboBox, QButtonGroup, QItemDelegate, QDialog, QMessageBox, QListWidget, QListWidgetItem
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtSql import QSqlDatabase

# QGIS imports
from qgis.core import QgsMapLayer, QgsGeometry, QgsMapLayerRegistry

#DsgTools imports
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.QmlTools.qmlParser import QmlParser
from PyQt4.Qt import QGroupBox, QButtonGroup

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'field_setup.ui'))

class FieldSetup(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.abstractDb = None
        self.abstractDbFactory = DbFactory()
        self.setupUi(self)
        
    
    def __del__(self):
        if self.abstractDb:
            del self.abstractDb
            self.abstractDb = None
        
    def getDbInfo(self):
        currentPath = os.path.dirname(__file__)
        if self.versionCombo.currentText() == '2.1.3':
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', '213', 'seed_edgv213.sqlite')
        elif self.versionCombo.currentText() == 'FTer_2a_Ed':
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', 'FTer_2a_Ed', 'seed_edgvfter_2a_ed.sqlite')

        self.abstractDb = self.abstractDbFactory.createDbFactory('QSQLITE')
        if not self.abstractDb:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('A problem occurred! Check log for details.'))
            return
        self.abstractDb.connectDatabase(edgvPath)

        try:
            self.abstractDb.checkAndOpenDb()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
        self.qmlDir = self.abstractDb.getQmlDir()
    
    def populateClassList(self):
        self.classListWidget.clear()
        try:
            geomClasses = self.abstractDb.listGeomClassesFromDatabase()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
        self.classListWidget.addItems(geomClasses)
    
    @pyqtSlot(int)
    def on_versionCombo_currentIndexChanged(self):
        if self.versionCombo.currentIndex() <> 0:
            self.getDbInfo()
            self.populateClassList()
        else:
            self.classListWidget.clear()
    
    def clearAttributeTableWidget(self):
        for i in range(self.attributeTableWidget.rowCount(),-1,-1):
            self.attributeTableWidget.removeRow(i)
        pass
    
    @pyqtSlot(int)
    def on_classListWidget_currentRowChanged(self,row):
        self.buttonNameLineEdit.setText('')
        self.clearAttributeTableWidget()
        schemaName, tableName = self.abstractDb.getTableSchema(self.classListWidget.item(row).text())
        qmlPath = os.path.join(self.qmlDir,tableName+'.qml')
        qml = QmlParser(qmlPath)
        qmlDict = qml.getDomainDict()
        count = 0
        for attr in qmlDict.keys():
            self.attributeTableWidget.insertRow(count)
            item = QTableWidgetItem()
            item.setText(attr)
            self.attributeTableWidget.setItem(count,0,item)
            if isinstance(qmlDict[attr],dict):
                comboItem = QComboBox()
                comboItem.addItems(qmlDict[attr].keys())
                self.attributeTableWidget.setCellWidget(count,1,comboItem)
            if isinstance(qmlDict[attr],tuple):
                (table,filterKeys) = qmlDict[attr]
                checkGroup = QButtonGroup()
                for key in filterKeys:
                    check = QCheckBox(key)
                    checkGroup.addButton(check)
                self.attributeTableWidget.setCellWidget(count,1,checkGroup)
                print table
                print filterKeys
                
                
            count+=1
        
    
    @pyqtSlot(bool)
    def on_addUpdatePushButton_clicked(self):
        print self.attributeTableWidget.cellWidget(0,1).currentText()