# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_processingTools.ui'
#
# Created: Tue Mar 10 13:32:09 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(557, 371)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.formLayout = QtGui.QFormLayout(self.tab)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.checkBox = QtGui.QCheckBox(self.tab)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.checkBox)
        self.label = QtGui.QLabel(self.tab)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.fileListWidget = QtGui.QListWidget(self.tab)
        self.fileListWidget.setObjectName(_fromUtf8("fileListWidget"))
        self.horizontalLayout_2.addWidget(self.fileListWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addButton = QtGui.QPushButton(self.tab)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(self.tab)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.verticalLayout.addWidget(self.removeButton)
        self.addFolderButton = QtGui.QPushButton(self.tab)
        self.addFolderButton.setObjectName(_fromUtf8("addFolderButton"))
        self.verticalLayout.addWidget(self.addFolderButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.srLineEdit = QtGui.QLineEdit(self.tab)
        self.srLineEdit.setObjectName(_fromUtf8("srLineEdit"))
        self.horizontalLayout.addWidget(self.srLineEdit)
        self.srsButton = QtGui.QPushButton(self.tab)
        self.srsButton.setObjectName(_fromUtf8("srsButton"))
        self.horizontalLayout.addWidget(self.srsButton)
        self.formLayout.setLayout(8, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(11, QtGui.QFormLayout.LabelRole, self.label_5)
        self.numberComboBox = QtGui.QComboBox(self.tab)
        self.numberComboBox.setObjectName(_fromUtf8("numberComboBox"))
        self.numberComboBox.addItem(_fromUtf8(""))
        self.numberComboBox.addItem(_fromUtf8(""))
        self.numberComboBox.addItem(_fromUtf8(""))
        self.numberComboBox.addItem(_fromUtf8(""))
        self.numberComboBox.addItem(_fromUtf8(""))
        self.numberComboBox.addItem(_fromUtf8(""))
        self.numberComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(11, QtGui.QFormLayout.FieldRole, self.numberComboBox)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_3)
        self.stretchComboBox = QtGui.QComboBox(self.tab)
        self.stretchComboBox.setObjectName(_fromUtf8("stretchComboBox"))
        self.stretchComboBox.addItem(_fromUtf8(""))
        self.stretchComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.stretchComboBox)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.tab_2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_2 = QtGui.QLabel(self.tab_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lineEdit_2 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.xmlModelButton = QtGui.QPushButton(self.tab_2)
        self.xmlModelButton.setObjectName(_fromUtf8("xmlModelButton"))
        self.horizontalLayout_3.addWidget(self.xmlModelButton)
        self.formLayout_2.setLayout(6, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.checkBox_2 = QtGui.QCheckBox(self.tab_2)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.SpanningRole, self.checkBox_2)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_4.addWidget(self.label_6)
        self.outputFolderEdit = QtGui.QLineEdit(Dialog)
        self.outputFolderEdit.setObjectName(_fromUtf8("outputFolderEdit"))
        self.horizontalLayout_4.addWidget(self.outputFolderEdit)
        self.outputFolderButton = QtGui.QPushButton(Dialog)
        self.outputFolderButton.setObjectName(_fromUtf8("outputFolderButton"))
        self.horizontalLayout_4.addWidget(self.outputFolderButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Batch Image Processor", None))
        self.checkBox.setText(_translate("Dialog", "Process images", None))
        self.label.setText(_translate("Dialog", "Input images:", None))
        self.addButton.setText(_translate("Dialog", "Add", None))
        self.removeButton.setText(_translate("Dialog", "Remove", None))
        self.addFolderButton.setText(_translate("Dialog", "Add folder", None))
        self.label_4.setText(_translate("Dialog", "Spatial Reference System:", None))
        self.srsButton.setText(_translate("Dialog", "CRS", None))
        self.label_5.setText(_translate("Dialog", "Output raster type", None))
        self.numberComboBox.setItemText(0, _translate("Dialog", "Byte", None))
        self.numberComboBox.setItemText(1, _translate("Dialog", "Unsigned Int 16", None))
        self.numberComboBox.setItemText(2, _translate("Dialog", "Int 16", None))
        self.numberComboBox.setItemText(3, _translate("Dialog", "Unsigned Int 32", None))
        self.numberComboBox.setItemText(4, _translate("Dialog", "Int 32", None))
        self.numberComboBox.setItemText(5, _translate("Dialog", "Float 32", None))
        self.numberComboBox.setItemText(6, _translate("Dialog", "Float 64", None))
        self.label_3.setText(_translate("Dialog", "Apply contrast enhancement:", None))
        self.stretchComboBox.setItemText(0, _translate("Dialog", "None", None))
        self.stretchComboBox.setItemText(1, _translate("Dialog", "Linear 2%", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Image", None))
        self.label_2.setText(_translate("Dialog", "Metadata output XML model:", None))
        self.xmlModelButton.setText(_translate("Dialog", "Search", None))
        self.checkBox_2.setText(_translate("Dialog", "Process metadata", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Metadata", None))
        self.label_6.setText(_translate("Dialog", "Output files folder:", None))
        self.outputFolderButton.setText(_translate("Dialog", "Search", None))

