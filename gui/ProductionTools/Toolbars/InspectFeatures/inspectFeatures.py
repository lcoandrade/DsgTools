# -*- coding: utf-8 -*-
"""
/***************************************************************************
InspectFeatures
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2016 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
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
import json

from qgis.core import (Qgis,
                       QgsProject,
                       QgsMapLayer,
                       QgsWkbTypes,
                       QgsVectorLayer,
                       QgsFeatureRequest,
                       QgsCoordinateTransform,
                       QgsCoordinateReferenceSystem)
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QWidget, QSpinBox, QMessageBox 


from .inspectFeatures_ui import Ui_Form
# FORM_CLASS, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'inspectFeatures.ui'))

class InspectFeatures(QWidget,Ui_Form):
    idxChanged = pyqtSignal(int)
    PROJECT_STATE_VAR = "inspectFeatureState"

    def __init__(self, iface, parent = None):
        """
        Constructor
        """
        super(InspectFeatures, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.splitter.hide()
        self.iface = iface
        # self.iface.currentLayerChanged.connect(self.enableScale)
        self.mMapLayerComboBox.layerChanged.connect(self.enableScale)
        self.mMapLayerComboBox.layerChanged.connect(self.setLayerToFilter)
        if not self.iface.activeLayer():
            self.enableTool(False)
        # self.iface.currentLayerChanged.connect(self.enableTool)
        self.mMapLayerComboBox.layerChanged.connect(self.enableTool)
        self.zoomPercentageSpinBox.setMinimum(0)
        self.zoomPercentageSpinBox.setMaximum(100)
        self.zoomPercentageSpinBox.setDecimals(3)
        self.zoomPercentageSpinBox.setSingleStep(1)
        self.zoomPercentageSpinBox.setSuffix('%')
        self.zoomPercentageSpinBox.setValue(100)
        self.zoomPercentageSpinBox.setEnabled(False)
        self.zoomPercentageSpinBox.hide()
        self.mScaleWidget.setScaleString('1:40000')
        self.mScaleWidget.setEnabled(False)
        self.mScaleWidget.hide()
        self.enableScale()
        self.canvas = self.iface.mapCanvas()
        self.allLayers={}
        self.idxChanged.connect(self.setNewId)
        self.setToolTip('')
        icon_path = ':/plugins/DsgTools/icons/inspectFeatures.png'
        text = self.tr('DSGTools: Inspect Features')
        self.activateToolAction = self.add_action(icon_path, text, self.inspectPushButton.toggle, parent = self.parent)
        self.iface.registerMainWindowAction(self.activateToolAction, '')
        icon_path = ':/plugins/DsgTools/icons/backInspect.png'
        text = self.tr('DSGTools: Back Inspect')
        self.backButtonAction = self.add_action(icon_path, text, self.backInspectButton.click, parent = self.parent)
        self.iface.registerMainWindowAction(self.backButtonAction, '')
        icon_path = ':/plugins/DsgTools/icons/nextInspect.png'
        text = self.tr('DSGTools: Next Inspect')
        self.nextButtonAction = self.add_action(icon_path, text, self.nextInspectButton.click, parent = self.parent)
        self.iface.registerMainWindowAction(self.nextButtonAction, '')
        icon_path = ':/plugins/DsgTools/icons/reload.png'
        text = self.tr('DSGTools: Set Active Layer on Feature Inspector')
        self.refreshPushButtonAction = self.add_action(icon_path, text, self.refreshPushButton.click, parent = self.parent)
        self.iface.registerMainWindowAction(self.refreshPushButtonAction, '')
        self.refreshPushButton.setToolTip(self.tr('Set current layer as selected layer on inspect tool'))
    
    def add_action(self, icon_path, text, callback, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        if parent:
            parent.addAction(action)
        return action
    
    def getIterateLayer(self):
        """
        Reads current layer set to combo box widget. Alias to 'currentLayer'.
        :return: (QgsVectorLayer) current selected layer.
        """
        return self.currentLayer()

    def enableTool(self, enabled = True):
        if enabled == None or not isinstance(enabled, QgsVectorLayer):
            allowed = False
        else:
            allowed = True
        toggled = self.isToggled()
        enabled = allowed and toggled
        self.backInspectButton.setEnabled(enabled)
        self.nextInspectButton.setEnabled(enabled)
        self.idSpinBox.setEnabled(enabled)
        
    def enableScale(self):
        """
        The scale combo should only be enabled for point layers
        """
        currentLayer = self.getIterateLayer()
        if QgsMapLayer is not None and currentLayer:
                if currentLayer.type() == QgsMapLayer.VectorLayer:
                    if currentLayer.geometryType() == QgsWkbTypes.PointGeometry:
                        self.mScaleWidget.setEnabled(True)
                        self.mScaleWidget.show()
                        self.zoomPercentageSpinBox.setEnabled(False)
                        self.zoomPercentageSpinBox.hide()
                    else:
                        self.mScaleWidget.setEnabled(False)
                        self.mScaleWidget.hide()
                        self.zoomPercentageSpinBox.setEnabled(True)
                        self.zoomPercentageSpinBox.show()
 
    @pyqtSlot(bool)
    def on_nextInspectButton_clicked(self):
        """
        Inspects the next feature
        """
        if self.nextInspectButton.isEnabled():
            method = getattr(self, 'testIndexFoward')
            self.iterateFeature(method)
    
    def testIndexFoward(self, index, maxIndex, minIndex):
        """
        Gets the next index
        """
        index += 1
        if index > maxIndex:
            index = minIndex
        return index
    
    def testIndexBackwards(self, index, maxIndex, minIndex):
        """
        gets the previous index
        """
        index -= 1
        if index < minIndex:
            index = maxIndex
        return index
            
    @pyqtSlot(bool)
    def on_backInspectButton_clicked(self):
        """
        Inspects the previous feature
        """
        if self.backInspectButton.isEnabled():
            method = getattr(self, 'testIndexBackwards')
            self.iterateFeature(method)
    
    @pyqtSlot(int, name = 'on_idSpinBox_valueChanged')
    def setNewId(self, newId):
        if not isinstance(self.sender(), QSpinBox):
            self.idSpinBox.setValue(newId)
        else:
            currentLayer = self.getIterateLayer()
            lyrName = currentLayer.name()
            if lyrName not in list(self.allLayers.keys()):
                self.allLayers[lyrName] = 0
                return
            oldIndex = self.allLayers[lyrName]
            if oldIndex == 0:
                return
            featIdList = self.getFeatIdList(currentLayer)
            if oldIndex not in featIdList:
                oldIndex = 0
            zoom = self.zoomLevel()
            if oldIndex == newId:
                # self.iface.messageBar().pushMessage(self.tr('Warning!'), self.tr('Selected id does not exist in layer {0}. Returned to previous id.').format(lyrName), level=Qgis.Warning, duration=2)
                return
            try:
                index = featIdList.index(newId)
                self.allLayers[lyrName] = index
                self.makeZoom(zoom, currentLayer, newId)
                self.idSpinBox.setSuffix(' ({0}/{1})'.format(index+1,len(featIdList)))
            except:
                # self.iface.messageBar().pushMessage(self.tr('Warning!'), self.tr('Selected id does not exist in layer {0}. Returned to previous id.').format(lyrName), level=Qgis.Warning, duration=2)
                self.idSpinBox.setValue(oldIndex)
                self.makeZoom(zoom, currentLayer, oldIndex)

    def zoomLevel(self):
        """
        Reads screen size proportions from GUI. If active layer is made of
        points, zoom level is given as the denominator for map scale, otherwise
        it'll be a percentage of the screen (proportions of selected feature to
        canvas).
        :return: (float) zoom level for feature display/zoom.
        """
        if self.getIterateLayer().geometryType() == QgsWkbTypes.PointGeometry:
            return self.mScaleWidget.scale()
        return self.zoomPercentageSpinBox.value()

    def setZoomLevel(self, zoom):
        """
        Reads screen size proportions from GUI. If active layer is made of
        points, zoom level is given as the denominator for map scale, otherwise
        it'll be a percentage of the screen (proportions of selected feature to
        canvas).
        :param zoom: (float) zoom level for feature display/zoom.
        """
        if self.getIterateLayer().geometryType() == QgsWkbTypes.PointGeometry:
            self.mScaleWidget.setScale(zoom)
        else:
            self.zoomPercentageSpinBox.setValue(zoom)

    def currentFeatureId(self):
        """
        Reads current feature ID selected to be zoomed in.
        :return: current feature ID as read from GUI.
        """
        return self.idSpinBox.value()

    def setCurrentFeatureId(self, featId):
        """
        Sets current feature ID selected to be zoomed in.
        :param featId: (int) feature ID to be set to GUI.
        """
        return self.idSpinBox.setValue(featId)

    def getFeatIdList(self, currentLayer):
        #getting all features ids
        if self.currentFilterText() == '':
            featIdList = currentLayer.allFeatureIds()
        elif not self.hasValidExpression():
            self.iface.messageBar().pushMessage(self.tr('Warning!'), self.tr('Invalid attribute filter!'), level=Qgis.Warning, duration=2)
            return []
        else:
            request = QgsFeatureRequest().setFilterExpression(self.mFieldExpressionWidget.asExpression())
            request.setFlags(QgsFeatureRequest.NoGeometry)
            featIdList = [i.id() for i in currentLayer.getFeatures(request)]
        #sort is faster than sorted (but sort is just available for lists)
        featIdList.sort()
        return featIdList
    
    def iterateFeature(self, method):
        """
        Iterates over the features selecting and zooming to the desired one
        method: method used to determine the desired feature index
        """
        currentLayer = self.getIterateLayer()
        lyrName = currentLayer.name()
        zoom = self.zoomLevel()
        featIdList = self.getFeatIdList(currentLayer)
        
        if currentLayer and len(featIdList) > 0:
            #checking if this is the first time for this layer (currentLayer)
            first = False
            if lyrName not in list(self.allLayers.keys()):
                self.allLayers[lyrName] = 0
                first = True

            #getting the current index
            index = self.allLayers[lyrName]

            #getting max and min ids
            #this was made because the list is already sorted, there's no need to calculate max and min
            maxIndex = len(featIdList) - 1
            minIndex = 0
            
            self.idSpinBox.setMaximum(featIdList[maxIndex])
            self.idSpinBox.setMinimum(featIdList[minIndex])

            #getting the new index
            if not first:
                index = method(index, maxIndex, minIndex)
            self.idSpinBox.setSuffix(' ({0}/{1})'.format(index+1,len(featIdList)))
            self.allLayers[lyrName] = index

            #getting the new feature id
            id = featIdList[index]

            #adjustin the spin box value
            self.idxChanged.emit(id)

            self.makeZoom(zoom, currentLayer, id)
            self.selectLayer(id, currentLayer)
        else:
            self.errorMessage()
            
    def errorMessage(self):
        """
        Shows am error message
        """
        QMessageBox.warning(self.iface.mainWindow(), self.tr(u"ERROR:"), self.tr(u"<font color=red>There are no features in the current layer:<br></font><font color=blue>Add features and try again!</font>"), QMessageBox.Close)

    def selectLayer(self, index, currentLayer):
        """
        Remove current layer feature selection
        currentLayer: layer that will have the feature selection removed
        """
        if currentLayer:
            currentLayer.removeSelection()
            currentLayer.select(index)
    
    def zoomToLayer(self, layer, zoom = None):
        box = layer.boundingBoxOfSelected()
        if zoom is not None:
            box.grow(100-zoom)
        # Defining the crs from src and destiny
        epsg = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
        crsDest = QgsCoordinateReferenceSystem(epsg)
        #getting srid from something like 'EPSG:31983'
        if not layer:
            layer = self.iface.mapCanvas().currentLayer()
        srid = layer.crs().authid()
        crsSrc = QgsCoordinateReferenceSystem(srid) #here we have to put authid, not srid
        # Creating a transformer
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance())
        newBox = coordinateTransformer.transform(box)

        self.iface.mapCanvas().setExtent(newBox)
        self.iface.mapCanvas().refresh()

    def zoomFeature(self, zoom, idDict = None):
        """
        Zooms to current layer selected features according to a specific zoom
        zoom: zoom to be applied
        """
        idDict = dict() if idDict is None else idDict
        currentLayer = self.getIterateLayer()
        if idDict == {}:
            self.zoomToLayer(currentLayer, zoom=float(zoom))
        else:
            id = idDict['id']
            lyr = idDict['lyr']
            selectIdList = lyr.selectedFeatureIds()
            lyr.removeSelection()
            lyr.selectByIds([id])
            self.zoomToLayer(layer = lyr, zoom=float(zoom))
            lyr.selectByIds(selectIdList)

        if self.getIterateLayer().geometryType() == QgsWkbTypes.PointGeometry:
            self.iface.mapCanvas().zoomScale(float(zoom))
        
    @pyqtSlot(bool, name = 'on_inspectPushButton_toggled')
    def toggleBar(self, toggled=None):
        """
        Shows/Hides the tool bar
        """
        if toggled is None:
            toggled = self.isToggled()
        if toggled:
            self.splitter.show()
            self.enableTool(self.currentLayer())
            self.setToolTip(self.tr('Select a vector layer to enable tool'))
        else:
            self.splitter.hide()   
            self.enableTool(False)
            self.setToolTip('') 

    def setValues(self, featIdList, currentLayer):
        lyrName = currentLayer.name()
        featIdList.sort()
        self.allLayers[lyrName] = 0

        maxIndex = len(featIdList) - 1
        minIndex = 0
        
        self.idSpinBox.setMaximum(featIdList[maxIndex])
        self.idSpinBox.setMinimum(featIdList[minIndex])

        #getting the new feature id
        id = featIdList[0]

        #adjustin the spin box value
        self.idxChanged.emit(id)
        #self.idSpinBox.setValue(id)

        zoom = self.mScaleWidget.scale()
        self.makeZoom(zoom, currentLayer, id)

    def makeZoom(self, zoom, currentLayer, id):
        #selecting and zooming to the feature
        # if not self.onlySelectedRadioButton.isChecked():
        #     self.selectLayer(id, currentLayer)
        #     self.zoomFeature(zoom)
        # else:
        self.zoomFeature(zoom, idDict = {'id':id, 'lyr':currentLayer})        

    @pyqtSlot(bool)
    def on_onlySelectedRadioButton_toggled(self, toggled):
        currentLayer = self.getIterateLayer()
        if toggled:
            featIdList = currentLayer.selectedFeatureIds()
            self.setValues(featIdList, currentLayer)
            self.idSpinBox.setEnabled(False)
        else:
            featIdList = currentLayer.allFeatureIds()
            self.setValues(featIdList, currentLayer)
            self.idSpinBox.setEnabled(True)

    def isToggled(self):
        """
        Identifies whether tool bar is toggled ("open").
        :return: (bool) if tool bar is toggled.
        """
        return self.inspectPushButton.isChecked()

    def setToggled(self, checked):
        """
        Set tool bar's toggling status (if it's "open"). Alias to "toggleBar".
        :param checked: (bool) if tool bar is toggled.
        """
        self.inspectPushButton.setChecked(checked)
        return self.toggleBar(checked)

    def currentLayer(self):
        """
        Reads current layer set to combo box widget.
        :return: (QgsVectorLayer) current selected layer.
        """
        return self.mMapLayerComboBox.currentLayer()

    def currentLayerName(self):
        """
        Reads current layer's name set to combo box widget.
        :return: (str) current selected layer's name.
        """
        return self.mMapLayerComboBox.currentText()

    def setLayer(self, layer):
        """
        Sets a layer as current layer on its combo box. Input may be either its
        name or a vector that is currently loaded to canvas.
        :param layer: (str/QgsVectorLayer) either layer name or a vector layer.
        """
        if isinstance(layer, str):
            self.mMapLayerComboBox.setCurrentText(layer)
        else:
            self.mMapLayerComboBox.setLayer(layer)

    def setLayerToFilter(self, layer):
        """
        Sets a layer as current layer on the filter widget.
        :param layer: (QgsVectorLayer) vector layer to be set.
        """
        self.mFieldExpressionWidget.setLayer(layer)

    def hasValidExpression(self):
        """
        Checks if currently filled expression on filter expression widget is
        valid.
        :return: (bool) whether current expression is valid.
        """
        return self.mFieldExpressionWidget.isValidExpression()

    def currentFilterText(self):
        """
        Reads current expression filled on filter expression widget as text.
        :return: (str) feature filtering expression from read GUI.
        """
        return self.mFieldExpressionWidget.currentText()

    def setExpression(self, exp):
        """
        Sets current expression filled on filter expression widget as text.
        :param exp: (str) feature filtering expression to be set to GUI.
        """
        self.mFieldExpressionWidget.setExpression(exp)

    def currentFilterExpression(self):
        """
        Reads current expression filled on filter expression widget as text.
        :return: (str) feature filtering expression from read GUI.
        """
        return self.mFieldExpressionWidget.asExpression()

    def state(self):
        """
        Reads current tool's attributes that compose its state.
        :return: (dict) an attribute value map that represents current tool's
                state.
        """
        return {
            "layer": self.currentLayerName(),
            "zoom": self.zoomLevel(),
            "featId": self.currentFeatureId(),
            "expression": self.currentFilterText(),
            "isOpen": self.isToggled()
        }

    def stateAsString(self, state=None):
        """
        Stringfied states is a simple and effective form of serializing objects for
        QGIS environment variable settings, as well as outside QGIS systems
        communications. This method transforms a tool's state map into a string.
        :param state: (dict) the map to be stringfied.
        :return: (str) stringfied tool state map.
        """
        state = state or self.state()
        return json.dumps(state)

    def stateFromString(self, state):
        """
        Reverts a string into a valid tool state map.
        :param state: (str) the map to be de-stringfied.
        :return: (dict) an attribute value map that represents current tool's
                state.
        """
        return json.loads(state)

    def validateState(self, state):
        """
        Verifies if a map is is a valid representation of a tool's state.
        :param state: (dict) the map to be checked.
        :return: (bool) whether the provided map represents a tool state.
        """
        if "layer" in state and not isinstance(state["layer"], str):
            return False
        if "zoom" in state and not isinstance(state["zoom"], float):
            return False
        if "featId" in state and not isinstance(state["featId"], int):
            return False
        if "expression" in state and not isinstance(state["expression"], str):
            return False
        if "isOpen" in state and not isinstance(state["isOpen"], bool):
            return False
        return True

    def setState(self, state):
        """
        Updates tool's attributes related to its state.
        :param state: (dict) an attribute value map that represents current tool's
                    state.
        :return: (bool) whether given parameters reflects tool's state after
                aplying it.
        """
        if not self.validateState(state):
            return False
        self.setLayer(state["layer"])
        self.setZoomLevel(state["zoom"])
        self.setCurrentFeatureId(state["featId"])
        self.setExpression(state["expression"])
        self.setToggled(state["isOpen"])
        return True

    @pyqtSlot(bool)
    def on_refreshPushButton_clicked(self):
        activeLayer = self.iface.activeLayer()
        if isinstance(activeLayer, QgsVectorLayer):
            self.setLayer(activeLayer)
        else:
            self.iface.messageBar().pushMessage(self.tr('Warning!'), self.tr('Active layer is not valid to be used in this tool.'), level=Qgis.Warning, duration=2)
    
    def unload(self):
        self.iface.unregisterMainWindowAction(self.activateToolAction)
        self.iface.unregisterMainWindowAction(self.backButtonAction)
        self.iface.unregisterMainWindowAction(self.nextButtonAction)
        self.mMapLayerComboBox.layerChanged.disconnect(self.enableScale)
        self.mMapLayerComboBox.layerChanged.disconnect(self.setLayerToFilter)
        self.mMapLayerComboBox.layerChanged.disconnect(self.enableTool)
