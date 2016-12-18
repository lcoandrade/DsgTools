# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-31
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
#DsgTools Imports
from DsgTools.Factories.DbCustomizationFactory.dbCustomization import DbCustomization

class AttributeCustomization(DbCustomization):
    def __init__(self, customJson):
        super(AttributeCustomization, self).__init__(customJson)
    
    def buildSql(self):
        '''
        self.customJson['AttributeToAdd'] = [{'schemaName':'schema', 'tableName':'nome', 'attrList':[-list of attrDef-]}]
        attrDef = [{'attrName':'nome', 'attrType':'varchar(80)', 'isPk':False, 'isNullable':True, 'references':None, 'default':None}]
        '''
        #Abstract method. Must be reimplemented in each child.
        sql = ''
        for modItem in self.customJson['AttributeToAdd']:
            schema = modItem['schemaName']
            table = modItem['tableName']
            for attr in modItem['attrList']:
                auxSql = 'ALTER TABLE "{0}"."{1}" ADD COLUMN {2} {3}'.format(schema,table,attr['attrName'],attr['attrType'])
                if not attr['isNullable']:
                    auxSql += ' NOT NULL '
                if 'references' in attr.keys():
                    if attr['references']:
                        if attr['default']:
                            auxSql += ' REFERENCES {0} DEFAULT {1}'.format(attr['references'], attr['default'])
                        else:
                            auxSql += ' REFERENCES {0}'.format(attr['references'])
                auxSql += ';\n'
                sql += auxSql
        return sql
    
    def buildUndoSql(self):
        #Abstract method. Must be reimplemented in each child.
        sql = ''
        for modItem in self.customJson['AttributeToAdd']:
            schema = modItem['schemaName']
            table = modItem['tableName']
            for attr in modItem['attrList']:
                sql += 'ALTER TABLE "{0}"."{1}" DROP COLUMN IF EXISTS "{2}" CASCADE;'.format(schema, table, attr['attrName'])
        return sql