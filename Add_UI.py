# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Add_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Add_component(object):
    def setupUi(self, Add_component):
        Add_component.setObjectName("Add_component")
        Add_component.resize(218, 242)
        Add_component.setMinimumSize(QtCore.QSize(218, 242))
        Add_component.setMaximumSize(QtCore.QSize(218, 242))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Add_component.setWindowIcon(icon)
        Add_component.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Add_component)
        self.buttonBox.setGeometry(QtCore.QRect(30, 190, 151, 31))
        self.buttonBox.setMinimumSize(QtCore.QSize(151, 31))
        self.buttonBox.setMaximumSize(QtCore.QSize(151, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Add_component)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 10, 162, 157))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(3)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(70, 22))
        self.label.setMaximumSize(QtCore.QSize(70, 22))
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(70, 22))
        self.label_2.setMaximumSize(QtCore.QSize(70, 22))
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox_2.setMinimumSize(QtCore.QSize(87, 20))
        self.spinBox_2.setMaximumSize(QtCore.QSize(87, 20))
        self.spinBox_2.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_2.setMaximum(10000)
        self.spinBox_2.setObjectName("spinBox_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox_2)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setMinimumSize(QtCore.QSize(70, 22))
        self.label_5.setMaximumSize(QtCore.QSize(70, 22))
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_4)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(70, 22))
        self.label_3.setMaximumSize(QtCore.QSize(70, 22))
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setMinimumSize(QtCore.QSize(70, 22))
        self.label_6.setMaximumSize(QtCore.QSize(70, 22))
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.spinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox.setMinimumSize(QtCore.QSize(87, 20))
        self.spinBox.setMaximumSize(QtCore.QSize(87, 20))
        self.spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox.setMaximum(10000)
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(70, 22))
        self.label_4.setMaximumSize(QtCore.QSize(70, 22))
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.cases_box = QtWidgets.QComboBox(self.formLayoutWidget)
        self.cases_box.setObjectName("cases_box")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cases_box)

        self.retranslateUi(Add_component)
        self.buttonBox.accepted.connect(Add_component.accept) # type: ignore
        self.buttonBox.rejected.connect(Add_component.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Add_component)
        Add_component.setTabOrder(self.lineEdit_2, self.spinBox_2)
        Add_component.setTabOrder(self.spinBox_2, self.lineEdit_4)
        Add_component.setTabOrder(self.lineEdit_4, self.lineEdit_3)
        Add_component.setTabOrder(self.lineEdit_3, self.spinBox)

    def retranslateUi(self, Add_component):
        _translate = QtCore.QCoreApplication.translate
        Add_component.setWindowTitle(_translate("Add_component", "Добавить компонент"))
        self.label.setText(_translate("Add_component", "Корпус"))
        self.label_2.setText(_translate("Add_component", "Номинал"))
        self.label_5.setText(_translate("Add_component", "Допуск"))
        self.label_3.setText(_translate("Add_component", "Адрес"))
        self.label_6.setText(_translate("Add_component", "Материал"))
        self.label_4.setText(_translate("Add_component", "Количество"))
import Resourses_rc