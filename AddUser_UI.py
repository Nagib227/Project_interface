# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddUser.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(391, 510)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 51))
        self.label.setStyleSheet("font: 16pt \"Perpetua\";")
        self.label.setObjectName("label")
        self.line_name = QtWidgets.QLineEdit(Dialog)
        self.line_name.setGeometry(QtCore.QRect(110, 20, 271, 31))
        self.line_name.setObjectName("line_name")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(10, 150, 371, 191))
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.listWidget.setObjectName("listWidget")
        self.line_data = QtWidgets.QLineEdit(Dialog)
        self.line_data.setGeometry(QtCore.QRect(170, 70, 211, 31))
        self.line_data.setObjectName("line_data")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 151, 41))
        self.label_2.setStyleSheet("font: 14pt \"Perpetua\";")
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(110, 110, 271, 31))
        self.comboBox.setStyleSheet("font: 12pt \"Perpetua\";")
        self.comboBox.setObjectName("comboBox")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 91, 31))
        self.label_3.setStyleSheet("font: 14pt \"Perpetua\";")
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(70, 470, 231, 31))
        self.pushButton.setStyleSheet("font: 13pt \"Perpetua\";")
        self.pushButton.setObjectName("pushButton")
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 350, 251, 31))
        self.comboBox_2.setObjectName("comboBox_2")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 350, 111, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox_3 = QtWidgets.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(10, 390, 181, 31))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_4 = QtWidgets.QComboBox(Dialog)
        self.comboBox_4.setGeometry(QtCore.QRect(200, 390, 181, 31))
        self.comboBox_4.setObjectName("comboBox_4")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(110, 430, 171, 31))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "??????:"))
        self.label_2.setText(_translate("Dialog", "???????? ????????????????:"))
        self.label_3.setText(_translate("Dialog", "????????????:"))
        self.pushButton.setText(_translate("Dialog", "????????????????"))
        self.pushButton_2.setText(_translate("Dialog", "??????????????"))
        self.pushButton_3.setText(_translate("Dialog", "???????????????? ????????????"))
