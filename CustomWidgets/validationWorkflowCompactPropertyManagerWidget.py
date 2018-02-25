# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-24
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt4.QtGui import QMessageBox, QApplication, QCursor, QFileDialog

#DsgTools imports
from DsgTools.ServerManagementTools.workspaceManager import WorkspaceManager
from DsgTools.CustomWidgets.genericParameterSetter import GenericParameterSetter
from DsgTools.CustomWidgets.genericManagerWidget import GenericManagerWidget
from DsgTools.CustomWidgets.genericCompactPropertyManagerWidget import GenericCompactPropertyManagerWidget
from DsgTools.ValidationTools.validationWorkflowCreator import ValidationWorkflowCreator
from DsgTools.Utils.utils import Utils
from DsgTools.dsgEnums import DsgEnums

from qgis.core import QgsMessageLog
import json

class ValidationWorkflowCompactPropertyManagerWidget(GenericCompactPropertyManagerWidget):
    def __init__(self, manager = None, parent = None):
        """
        Constructor
        """
        super(ValidationWorkflowCompactPropertyManagerWidget, self).__init__(parent = parent)
    
    def populateConfigInterface(self, validationManager, jsonDict = None):
        '''
        Must be reimplemented in each child
        '''
        dlg = ValidationWorkflowCreator(validationManager, parameterDict = jsonDict)
        if dlg.exec_():
            return dlg.getParameterDict()
        else:
            return None
    
    def instantiateManagerObject(self, abstractDb, dbDict, edgvVersion):
        return ValidationWorkflowManager(abstractDb, dbDict, edgvVersion)