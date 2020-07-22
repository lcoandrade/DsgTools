# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-07-15
        git sha              : $Format:%H$
        copyright            : (C) 2020 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

from qgis.core import QgsProject, QgsExpressionContextUtils

class ManagerEnumerator:
    """
    Enumerates all DSGTools interface component managers.
    This class is desgined to support stateManager module, hence it's not a
    DsgToolsEnum.
    """
    GuiManager, ProductionToolsGuiManager, ToolBoxesGuiManager, \
        ToolbarsGuiManager, MapToolsGuiManager = range(5)
        

printer = lambda x: print("Tool initiate {0}.".format(x))

def app():
    """
    Gets the plugin's base class instance.
    :return: (DsgTools) current instance for DsgTools main class.
    """
    # importing DsgTools class outside method scope will cause a conflict
    # upon plugin booting
    from DsgTools.dsg_tools import DsgTools
    return DsgTools.instance()

def guiManager():
    """
    Gets the current instance of GUI manager class.
    :return: (GuiManager) instance of manager that is responsible for all
             loaded components to QGIS GUI.
    """
    return app().guiManager

def productionToolsGuiManager():
    """
    Gets the current instance of GUI manager class.
    :return: (ProductionToolsGuiManager) instance of manager that is
             responsible for all loaded production tools components to QGIS
             GUI.
    """
    return guiManager().productionToolsGuiManager

def toolBoxesGuiManager():
    """
    Gets the current instance of GUI manager class.
    :return: (ToolBoxesGuiManager) instance of manager that is responsible for
             all loaded tool boxes components to QGIS GUI.
    """
    return productionToolsGuiManager().toolBoxesGuiManager

def mapToolsGuiManager():
    """
    Gets the current instance of GUI manager class.
    :return: (MapToolsGuiManager) instance of manager that is responsible for
             all loaded maptools components to QGIS GUI.
    """
    return productionToolsGuiManager().mapToolsGuiManager

def toolbarsGuiManager():
    """
    Gets the current instance of GUI manager class.
    :return: (ToolbarsGuiManager) instance of manager that is responsible for
             all loaded tool bars components to QGIS GUI.
    """
    return productionToolsGuiManager().toolbarsGuiManager

def stateManagedTools():
    """
    Identifies all DSGTools tools that allow their state to be managed, saved
    and set through an API call.
    """
    tools = dict()
    managers = [
        toolBoxesGuiManager(),
        mapToolsGuiManager(),
        toolbarsGuiManager()
    ]
    for idx, m in enumerate(managers):
        mName = {
            0: "Tool box",
            1: "Maptool",
            2: "Tool bar"
        }[idx]
        tools[mName] = list()
        for attr in dir(m):
            if hasattr(getattr(m, attr), "PROJECT_STATE_VAR"):
                tools[mName].append(attr)
    return tools

def getTool(tool):
    """
    Accesses the loaded instance of a DSGTools tool that has its state managed.
    :param tool: (str) name of the tool to be accessed.
    """
    managers = [
        toolBoxesGuiManager(),
        mapToolsGuiManager(),
        toolbarsGuiManager()
    ]
    for m in managers:
        for attr in dir(m):
            if hasattr(getattr(m, attr), "PROJECT_STATE_VAR"):
                return getattr(m, tool)

def toolState(tool):
    """
    Gets the tool state as string.
    :return: (str) stringfied tool state map.
    """
    t = getTool(tool)
    if t is None:
        return "{}"
    state = t.state()
    return t.stateAsString(state)

def setToolState(tool, state):
    """
    
    """
    pass

def storedToolState(tool):
    """
    
    """
    pass

def saveToolState(tool, state):
    """
    Saves the state of a state managed tool to QGIS project.
    :param tool: (str) name of the tool to have its state stored.
    """
    tool = getTool(tool)
    if tool is None:
        return
    QgsExpressionContextUtils.setProjectVariable(
        QgsProject.instance(),
        tool.PROJECT_STATE_VAR,
        state
    )

def loadToolState(tool):
    """
    
    """
    pass

def saveState():
    """
    Saves the state of all state managed tools to QGIS project.
    """
    pass

def loadState():
    """
    
    """
    pass

def start():
    """
    Starts watching for tool modifications.
    """
    app()
    print("States are now being watched/managed")

def stop():
    """
    Disconnects state manager from all managed tools.
    """
    print("States no longer watched/managed")
