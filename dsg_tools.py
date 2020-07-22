# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-10-09
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        mod history          : 2015-04-12 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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

import sys
from os import path

currentPath = path.dirname(__file__)
sys.path.append(path.abspath(currentPath))
try:
    import ptvsd
    ptvsd.enable_attach(address = ('localhost', 5679))
except Exception as e:
    pass

from qgis.core import QgsApplication
from qgis.utils import showPluginHelp
from qgis.PyQt.QtCore import (Qt,
                              qVersion,
                              QSettings,
                              QTranslator,
                              QCoreApplication)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QToolButton, QMenu, QAction

from DsgTools import resources_rc
from DsgTools.core.DSGToolsProcessingAlgs.dsgtoolsProcessingAlgorithmProvider import DSGToolsProcessingAlgorithmProvider
from DsgTools.gui.guiManager import GuiManager

class DsgTools(object):
    """QGIS Plugin Implementation."""
    _instance = None
    
    @staticmethod
    def instance():
        """
        Desgined to handle requests for a singleton's instance.
        :return: (DsgTools) the class' instance for this app lifecycle.
        """
        if DsgTools._instance is None:
            from qgis.utils import iface
            DsgTools(iface)
        return DsgTools._instance

    def __init__(self, iface):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        if not DsgTools._instance is None:
            raise Exception(
                self.tr(
                    "This object is a singleton and an instance already "
                    "exists. Please use 'instance' static method to access it."
                )
            )
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = path.join(
            self.plugin_dir,
            'i18n',
            'DsgTools_{}.qm'.format(locale))

        if path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        # Declare instance attributes
        self.actions = []
        self.menu = '&DSGTools'
        self.toolbar = self.iface.addToolBar(u'DsgTools')
        self.toolbar.setObjectName(u'DsgTools')

        self.dsgTools = None
        self.menuBar = self.iface.mainWindow().menuBar()
        self.provider = DSGToolsProcessingAlgorithmProvider()
        DsgTools._instance = self

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.
        We implement this ourselves since we do not inherit QObject.
        :param message: String for translation.
        :type message: str, QString
        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('DsgTools', message)

    def unload(self):
        """
        Removes the plugin menu item and icon from QGIS GUI
        """
        self.guiManager.unload()
        for action in self.actions:
            self.iface.removePluginMenu(
                '&DSGTools',
                action)
            self.iface.removeToolBarIcon(action)
            self.iface.unregisterMainWindowAction(action)

        if self.dsgTools is not None:
            self.menuBar.removeAction(self.dsgTools.menuAction())
        self.iface.mainWindow().removeToolBar(self.toolbar)
        QgsApplication.processingRegistry().removeProvider(self.provider)
        del self.dsgTools
        del self.toolbar

    def initGui(self):
        """
        Create the menu entries and toolbar icons inside the QGIS GUI
        """

        self.dsgTools = QMenu(self.iface.mainWindow())
        self.dsgTools.setObjectName(u'DsgTools')
        self.dsgTools.setTitle(u'DSGTools')
        self.menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.dsgTools)
        #GuiManager
        self.guiManager = GuiManager(self.iface, parentMenu = self.dsgTools, toolbar = self.toolbar)
        self.guiManager.initGui()
        #provider
        QgsApplication.processingRegistry().addProvider(self.provider)