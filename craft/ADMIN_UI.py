# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ADMIN.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(365, 129)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(90, 90, 151, 31))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(150, 10, 211, 31))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.line_pass = QtWidgets.QLineEdit(Dialog)
        self.line_pass.setGeometry(QtCore.QRect(150, 50, 211, 31))
        self.line_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_pass.setObjectName("line_pass")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 121, 31))
        self.label.setStyleSheet("font: 15pt \"Perpetua\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 111, 31))
        self.label_2.setStyleSheet("font: 15pt \"Perpetua\";")
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Войти"))
        self.lineEdit.setText(_translate("Dialog", "ADMIN"))
        self.label.setText(_translate("Dialog", "Логин:"))
        self.label_2.setText(_translate("Dialog", "Пароль:"))