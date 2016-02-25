# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
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
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QApplication, QCursor, QMenu, QTableWidgetItem
from PyQt4.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery

# QGIS imports
from qgis.core import QgsMapLayer, QgsField, QgsDataSourceURI

import qgis as qgis
from qgis.core import QgsMessageLog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'validation_toolbox.ui'))

#DsgTools imports
from DsgTools.Factories.LayerFactory.layerFactory import LayerFactory
from DsgTools.ValidationTools.validation_config import ValidationConfig
from DsgTools.ValidationTools.validationManager import ValidationManager
from DsgTools.ValidationTools.validation_history import ValidationHistory

class ValidationToolbox(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface, codeList):
        """Constructor."""
        super(ValidationToolbox, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        #TODO enable tab when db is set
        self.layerFactory = LayerFactory()
        self.edgvLayer = None
        self.flagLyr = None
        self.iface = iface
        self.codeList = codeList
        self.databaseLineEdit.setReadOnly(True)
        self.configWindow = ValidationConfig()
        self.configWindow.widget.connectionChanged.connect(self.updateDbLineEdit)
        self.validationManager = None
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.createMenuEditFlagStatus)


    def createMenuEditFlagStatus(self, position):
        menu = QMenu()
        item = self.tableView.indexAt(position)
        if item:
            menu.addAction(self.tr('Zoom to flag'), self.zoomToFlag)
            menu.addAction(self.tr('Set Visited'), self.setFlagVisited)
            menu.addAction(self.tr('Set Unvisited'), self.setFlagUnvisited)
        menu.exec_(self.tableView.viewport().mapToGlobal(position))

    
    @pyqtSlot()
    def on_theSelectionModel_selectionChanged(self):
        print 'mudou'
    
    def setFlagVisited(self):
        print 'visited'

    def setFlagUnvisited(self):
        print 'unvisited'
    
    def zoomToFlag(self):
        idx =  self.tableView.selectionModel().selection().indexes()[0].data()
        self.loadFlagLyr()
        self.iface.mapCanvas().refresh()
        self.flagLyr.select(idx)
        bbox = self.flagLyr.boundingBoxOfSelected()
        self.flagLyr.removeSelection()
        self.iface.mapCanvas().setExtent(bbox)
        self.iface.mapCanvas().refresh()
    
    def loadFlagLyr(self):
        if self.checkFlagsLoaded() or self.edgvLayer == None:
            dbName = self.configWindow.widget.abstractDb.getDatabaseName()
            self.edgvLayer = self.layerFactory.makeLayer(self.configWindow.widget.abstractDb, self.codeList, 'validation.aux_flags_validacao_p')
            groupList =  qgis.utils.iface.legendInterface().groups()
            if dbName in groupList:
                self.flagLyr =  self.edgvLayer.load(self.configWindow.widget.crs,groupList.index(dbName))
            else:
                parentTreeNode = qgis.utils.iface.legendInterface().addGroup(self.configWindow.widget.abstractDb.getDatabaseName(), -1)
                self.flagLyr =  self.edgvLayer.load(self.configWindow.widget.crs,parentTreeNode)
    
    def checkFlagsLoaded(self):
        loadedLayers = self.iface.mapCanvas().layers()
        candidateLyrs = []
        for lyr in loadedLayers:
            if lyr.name() == 'aux_flags_validacao_p':
                candidateLyrs.append(lyr)
        for lyr in candidateLyrs:
            if self.configWindow.widget.abstractDb.isLyrInDb(lyr):
                return True
        return False

    @pyqtSlot(bool)
    def on_openDbPushButton_clicked(self):
        self.configWindow.show()

    @pyqtSlot(bool)
    def on_historyButton_clicked(self):
        historyWindow = ValidationHistory(self.configWindow.widget.abstractDb)
        historyWindow.exec_()
    
    @pyqtSlot()
    def updateDbLineEdit(self):
        self.databaseLineEdit.setText(self.configWindow.widget.comboBoxPostgis.currentText())
        self.scale = self.configWindow.scaleComboBox.currentText()
        self.tolerance = self.configWindow.toleranceLineEdit.text()
        self.validationManager = ValidationManager(self.configWindow.widget.abstractDb)
        self.populateProcessList()
        pass
    
    def populateProcessList(self):
        self.processTreeWidget.clear()
        self.edgvLayer = None
        self.flagLyr = None
        rootItem = self.processTreeWidget.invisibleRootItem()
        procList = self.validationManager.processList
        for i in range(len(procList)):
            item = QtGui.QTreeWidgetItem(rootItem)
            item.setText(0, str(i+1))
            item.setText(1,procList[i].getName())
            item.setText(2, procList[i].getStatusMessage())
        pass
    
    @pyqtSlot(bool)
    def on_runButton_clicked(self):
        index = int(self.processTreeWidget.selectedItems()[0].text(0))-1
        processName = self.validationManager.processList[index].getName()
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        procReturn = self.validationManager.executeProcess(processName)
        QApplication.restoreOverrideCursor()
        self.populateProcessList()
        if procReturn == 0:
            QgsMessageLog.logMessage(self.validationManager.getLog(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            QtGui.QMessageBox.warning(self, self.tr('Error!'), self.tr('Process %s returned error. Check log for details.'))
            self.validationManager.clearLog()
        else:
            QtGui.QMessageBox.warning(self, self.tr('Success!'), self.tr('Process successfully executed!'))
            #executou! show!
            pass
        pass

    def createItem(self, parent, text):
        
        return item

    @pyqtSlot(int)
    def on_validationTabWidget_currentChanged(self):
        if self.validationTabWidget.currentIndex() == 1 and self.configWindow.widget.abstractDb <> None:
            self.projectModel = QSqlTableModel(None,self.configWindow.widget.abstractDb.db)
            self.projectModel.setTable('validation.aux_flags_validacao_p')
            self.projectModel.select()
            self.tableView.setModel(self.projectModel)
        pass