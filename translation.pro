 SOURCES         =	AttributeTools/attributes_viewer.py \
					AttributeTools/code_list.py \
					BDGExTools/BDGExTools.py \
					ComplexTools/complexWindow.py \
 					ComplexTools/manageComplex.py \
					ConversionTools/convert_database.py \
					CustomWidgets/connectionWidget.py \
					CustomWidgets/exploreServerWidget.py \
 					DbTools/PostGISTool/postgisDBTool.py \
 					DbTools/SpatialiteTool/cria_spatialite_dialog.py \
					Factories/DbFactory/abstractDb.py \
					Factories/DbFactory/dbFactory.py \
					Factories/DbFactory/postgisDb.py \
					Factories/DbFactory/spatialiteDb.py \
					Factories/LayerFactory/edgv_layer.py \
					Factories/LayerFactory/layerFactory.py \
					Factories/LayerFactory/postgis_layer.py \
					Factories/LayerFactory/spatialite_layer.py \
					Factories/SqlFactory/postgisSqlGenerator.py \
					Factories/SqlFactory/spatialiteSqlGenerator.py \
					Factories/SqlFactory/sqlGenerator.py \
					Factories/SqlFactory/sqlGeneratorFactory.py \
 					Factories/ThreadFactory/dpiThread.py \
 					Factories/ThreadFactory/genericThread.py \
 					Factories/ThreadFactory/inventoryThread.py \
 					Factories/ThreadFactory/postgisDbThread.py \
 					Factories/ThreadFactory/threadFactory.py \
 					ImageTools/processingTools.py \
 					ImageTools/raster_processing.py \
					InventoryTools/inventoryTools.py \
 					LayerTools/load_by_category.py \
 					LayerTools/load_by_class.py \
 					LayerTools/map_index.py \
 					LayerTools/ui_create_inom_dialog.py \
 					ProcessingTools/processManager.py \
 					ProductionTools/acquisition_tools.py \
 					QmlTools/qml_creator.py \
 					QmlTools/qmlParser.py \
					ServerTools/exploreDb.py \
 					ServerTools/serverConfigurator.py \
					ServerTools/serverDBExplorer.py \
 					ServerTools/viewServers.py \
					ToolboxTools/models_and_scripts_installer.py \
					UserTools/alter_user_password.py \
					UserTools/assign_profiles.py \
					UserTools/create_profile.py \
					UserTools/create_user.py \
					UserTools/permission_properties.py \
					UserTools/profile_editor.py \
					UserTools/user_profiles.py \
					Utils/utils.py \
					VectorTools/calc_contour.py \
					VectorTools/contour_tool.py \
					VectorTools/dsg_line_tool.py \
 					aboutdialog.py \
 					dsg_tools.py \

 FORMS         =	AttributeTools/attributes_viewer.ui \
					AttributeTools/code_list.ui \
					ComplexTools/complexWindow_base.ui \
 					ComplexTools/ui_manageComplex.ui \
					ConversionTools/convert_database.ui \
					CustomWidgets/connectionWidget.ui \
					CustomWidgets/exploreServerWidget.ui \
 					DbTools/PostGISTool/ui_postgisDBTool.ui \
 					DbTools/SpatialiteTool/cria_spatialite_dialog_base.ui \							
 					ImageTools/ui_processingTools.ui \
					InventoryTools/ui_inventoryTools.ui \
 					LayerTools/load_by_category_dialog.ui \
 					LayerTools/load_by_class_base.ui \
 					LayerTools/ui_create_inom_dialog_base.ui \
					ServerTools/exploreDb.ui \
 					ServerTools/ui_serverConfigurator.ui \
					ServerTools/ui_serverDBExplorer.ui \
 					ServerTools/ui_viewServers.ui \
					ToolboxTools/models_and_scripts_installer.ui \
					UserTools/alter_user_password.ui \
					UserTools/assign_profiles.ui \
					UserTools/create_profile.ui \
					UserTools/create_user.ui \
					UserTools/permission_properties.ui \
					UserTools/profile_editor.ui \
					UserTools/user_profiles.ui \
					VectorTools/calc_contour.ui \
 					ui_about.ui \

 TRANSLATIONS    = i18n/DsgTools_pt.ts

RESOURCES += \
    resources.qrc
