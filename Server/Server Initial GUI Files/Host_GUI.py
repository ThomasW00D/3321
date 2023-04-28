# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Host_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1271, 856)
        self.msgLBL = QtWidgets.QLabel(Form)
        self.msgLBL.setGeometry(QtCore.QRect(10, 140, 191, 25))
        self.msgLBL.setObjectName("msgLBL")
        self.logLbl = QtWidgets.QLabel(Form)
        self.logLbl.setGeometry(QtCore.QRect(660, 140, 281, 25))
        self.logLbl.setObjectName("logLbl")
        self.msgTxt = QtWidgets.QTextEdit(Form)
        self.msgTxt.setEnabled(False)
        self.msgTxt.setGeometry(QtCore.QRect(10, 170, 601, 351))
        self.msgTxt.setObjectName("msgTxt")
        self.createBtn = QtWidgets.QPushButton(Form)
        self.createBtn.setGeometry(QtCore.QRect(10, 10, 150, 46))
        self.createBtn.setObjectName("createBtn")
        self.sendBtn = QtWidgets.QPushButton(Form)
        self.sendBtn.setEnabled(False)
        self.sendBtn.setGeometry(QtCore.QRect(10, 530, 150, 46))
        self.sendBtn.setObjectName("sendBtn")
        self.serverTxt = QtWidgets.QTextEdit(Form)
        self.serverTxt.setEnabled(False)
        self.serverTxt.setGeometry(QtCore.QRect(10, 610, 1251, 171))
        self.serverTxt.setReadOnly(True)
        self.serverTxt.setObjectName("serverTxt")
        self.serverLbl = QtWidgets.QLabel(Form)
        self.serverLbl.setGeometry(QtCore.QRect(10, 580, 261, 25))
        self.serverLbl.setObjectName("serverLbl")
        self.closeBtn = QtWidgets.QPushButton(Form)
        self.closeBtn.setEnabled(False)
        self.closeBtn.setGeometry(QtCore.QRect(10, 790, 150, 46))
        self.closeBtn.setObjectName("closeBtn")
        self.nicknameTxt = QtWidgets.QLineEdit(Form)
        self.nicknameTxt.setEnabled(False)
        self.nicknameTxt.setGeometry(QtCore.QRect(170, 80, 441, 31))
        self.nicknameTxt.setObjectName("nicknameTxt")
        self.nicknameBtn = QtWidgets.QPushButton(Form)
        self.nicknameBtn.setEnabled(False)
        self.nicknameBtn.setGeometry(QtCore.QRect(10, 70, 150, 46))
        self.nicknameBtn.setObjectName("nicknameBtn")
        self.logTxt = QtWidgets.QTextEdit(Form)
        self.logTxt.setEnabled(False)
        self.logTxt.setGeometry(QtCore.QRect(660, 170, 601, 351))
        self.logTxt.setReadOnly(True)
        self.logTxt.setObjectName("logTxt")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.msgLBL.setText(_translate("Form", "Message:"))
        self.logLbl.setText(_translate("Form", "Message Log:"))
        self.createBtn.setText(_translate("Form", "Create Server"))
        self.sendBtn.setText(_translate("Form", "Send Message"))
        self.serverLbl.setText(_translate("Form", "Server Log:"))
        self.closeBtn.setText(_translate("Form", "Close Server"))
        self.nicknameBtn.setText(_translate("Form", "Set Nickname"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
