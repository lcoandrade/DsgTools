# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-24
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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
import os
import json
from collections import defaultdict

from qgis.core import (Qgis,
                       QgsProject,
                       QgsMessageLog,
                       QgsVectorLayer,
                       QgsEditorWidgetSetup,
                       QgsCoordinateReferenceSystem)
from qgis.PyQt.QtSql import QSqlQuery

from .spatialiteLayerLoader import SpatialiteLayerLoader
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget

class GeopackageLayerLoader(SpatialiteLayerLoader):
    def __init__(self, iface, abstractDb, loadCentroids):
        """Constructor."""
        super(GeopackageLayerLoader, self).__init__(iface, abstractDb, loadCentroids)
        
        self.provider = 'geopackage'
        
        try:
            dbVersion = abstractDb.getDatabaseVersion()
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), 'DSGTools Plugin', Qgis.Critical)
            return

        self.buildUri()

    def specialEdgvAttributes(self):
        """
        Gets the list of attributes shared by many EDGV classes and have a different domain
        depending on which category the EDGV class belongs to.
        :return: (list-of-str) list of "special" EDGV classes. 
        """
        return ["finalidade", "relacionado", "coincidecomdentrode", "tipo"]

    def tableFields(self, table):
        """
        Gets all attribute names for a table.
        :return: (list-of-str) list of attribute names.
        """
        return self.abstractDb.tableFields(table)

    def domainMapping(self, modelVersion):
        """
        Identifies wich table and attribute is related to all tables available
        in the database that has a mapping (FK to a domain table).
        :param modelVersion: (str) which model version is identified (e.g. 3.0)
        :return: (dict) mapping from each layer's attributes to its FK relative
        - Mapping format:
            {
                "schema_layer_name": {
                    "layer_attribute_name": [
                        "domain_table_name",
                        "domain_refereced_attribute_name"
                    ]
                }
            }
        """
        basePath = os.path.join(
            os.path.dirname(__file__), "..", "..", "DbModels", "DomainMapping")
        path = {
            "3.0": os.path.join(basePath, "edgv_3.json"),
            "2.1.3 Pro": os.path.join(basePath, "edgv_213_pro.json")
        }.pop(modelVersion, None)
        if path is None or not os.path.exists(path):
            return dict()
        with open(path, "r") as fp:
            # file generated based on PostGIS FK metadata
            return json.load(fp)

    def getAllEdgvDomainsFromTableName(self, schema, table):
        """
        EDGV databases deployed by DSGTools have a set of domain tables. Gets the value map from such DB.
        It checks for all attributes found.
        :param table: (str) layer to be checked for its EDGV mapping.
        :return: (dict) value map for all attributes that have one.
        """
        self.abstractDb.checkAndOpenDb()
        ret = defaultdict(dict)
        db = self.abstractDb.db
        edgv = self.abstractDb.getDatabaseVersion()
        domainMap = self.domainMapping(edgv)
        fullTablaName = schema + "_" + table
        sql = 'select code, code_name from dominios_{field} order by code'
        for fieldName in self.tableFields(fullTablaName):
            if fullTablaName in domainMap:
                domains = domainMap[fullTablaName]
                # if domain mapping is not yet available for current version
                if fieldName in domains:
                    # replace this method over querying db for the table...
                    domainTable = domains[fieldName][0]
                elif fieldName.replace("_", "") in domains:
                    domainTable = domains[fieldName.replace("_", "")][0]
                else:
                    domainTable = fieldName
                query = QSqlQuery(sql.format(field=domainTable), db)
            elif fieldName in self.specialEdgvAttributes():
                # EDGV "special" attributes that are have different domains depending on
                # which class it belongs to
                if edgv in ("2.1.3 Pro", "3.0 Pro"):
                    # Pro versions now follow the logic "{attribute}_{CLASS_NAME}"
                    cat = table.rsplit("_", 1)[0].split("_", 1)[-1]
                else:
                    cat = table.split("_")[0]
                attrTable = "{attribute}_{cat}".format(attribute=fieldName, cat=cat)
                query = QSqlQuery(sql.format(field=attrTable), db)
            else:
                query = QSqlQuery(sql.format(field=fieldName), db)
            if not query.isActive():
                continue
            while query.next():
                code = str(query.value(0))
                code_name = query.value(1)
                ret[fieldName][code_name] = code
        return ret

    def load(self, inputList, useQml=False, uniqueLoad=False, useInheritance=False, stylePath=None, onlyWithElements=False, geomFilterList=[], isEdgv=True, customForm=False, editingDict=None, parent=None):
        """
        1. Get loaded layers
        2. Filter layers;
        3. Load domains;
        4. Get Aux Dicts;
        5. Build Groups;
        6. Load Layers;
        """
        self.iface.mapCanvas().freeze() #done to speedup things
        layerList, isDictList = self.preLoadStep(inputList)
        #2. Filter Layers:
        filteredLayerList = self.filterLayerList(layerList, False, onlyWithElements, geomFilterList)
        filteredDictList = [i for i in inputList if i['tableName'] in filteredLayerList] if isDictList else filteredLayerList
        edgvVersion = self.abstractDb.getDatabaseVersion()
        rootNode = QgsProject.instance().layerTreeRoot()
        dbNode = self.getDatabaseGroup(rootNode)
        #3. Load Domains
        #do this only if EDGV Version = FTer
        # domLayerDict = self.loadDomains(filteredLayerList, dbNode, edgvVersion)
        #4. Get Aux dicts
        lyrDict = self.getLyrDict(filteredDictList, isEdgv=isEdgv)
        #5. Build Groups
        groupDict = self.prepareGroups(dbNode, lyrDict)
        #5. load layers
        if parent:
            primNumber = 0
            for prim in list(lyrDict.keys()):
                for cat in list(lyrDict[prim].keys()):
                    for lyr in lyrDict[prim][cat]:
                        primNumber += 1
            localProgress = ProgressWidget(1, primNumber-1, self.tr('Loading layers... '), parent=parent)
        loadedDict = dict()
        for prim in list(lyrDict.keys()):
            for cat in list(lyrDict[prim].keys()):
                for lyr in lyrDict[prim][cat]:
                    try:
                        vlayer = self.loadLayer(lyr, groupDict[prim][cat], uniqueLoad, stylePath, None)
                        if vlayer:
                            if isinstance(lyr, dict):
                                key = lyr['lyrName']
                            else:
                                key = lyr
                            loadedDict[key]=vlayer
                    except Exception as e:
                        if isinstance(lyr, dict):
                            key = lyr['lyrName']
                        else:
                            key = lyr
                        self.logErrorDict[key] = self.tr('Error for layer ')+key+': '+':'.join(e.args)
                        self.logError()
                    if parent:
                        localProgress.step()
        self.removeEmptyNodes(dbNode)
        self.iface.mapCanvas().freeze(False) #done to speedup things
        return loadedDict

    def loadLayer(self, inputParam, parentNode, uniqueLoad, stylePath, domLayerDict):
        """
        Loads a layer
        :param lyrName: Layer nmae
        :param idSubgrupo: sub group id
        :param uniqueLoad: boolean to mark if the layer should only be loaded once
        :param stylePath: path to the styles used
        :param domLayerDict: domain dictionary
        :return:
        """
        lyrName, schema, geomColumn, tableName, srid = self.getParams(inputParam)
        lyr = self.checkLoaded(tableName)
        if uniqueLoad and lyr:
            return lyr
        vlayer = self.getLayerByName("{0}_{1}".format(schema, tableName))
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSGTools Plugin", Qgis.Critical)
        QgsProject.instance().addMapLayer(vlayer, addToLegend=False)
        crs = QgsCoordinateReferenceSystem(int(srid), QgsCoordinateReferenceSystem.EpsgCrsId)
        vlayer.setCrs(crs)
        # vlayer = self.setDomainsAndRestrictionsWithQml(vlayer)
        for field, valueMap in self.getAllEdgvDomainsFromTableName(schema, tableName).items():
            fieldIndex = vlayer.fields().indexFromName(field)
            widgetSetup = QgsEditorWidgetSetup("ValueMap", {"map": valueMap})
            vlayer.setEditorWidgetSetup(fieldIndex, widgetSetup)
        # vlayer = self.setMulti(vlayer, domLayerDict)
        if stylePath:
            fullPath = self.getStyle(stylePath, tableName)
            if fullPath:
                vlayer.loadNamedStyle(fullPath, True)
        parentNode.addLayer(vlayer)
        vlayer = self.createMeasureColumn(vlayer)
        return vlayer

    def getLayerByName(self, layer):
        """
        Return the layer layer from a given layer name.
        :param layer: (str) table name - for GPKG it is [SCHEMA]_[CATEGORY]_[CLASS].
        :return: (QgsVectorLayer) vector layer. 
        """
        # parent class reimplementation
        schema = layer.split('_')[0]
        table = layer[len(schema) + 1:]
        lyrName, schema, geomColumn, tableName, srid = self.getParams(table)
        self.setDataSource('', layer, geomColumn, '')
        return QgsVectorLayer("{0}|layername={1}".format(self.abstractDb.db.databaseName(), layer), table, "ogr")
