# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Client_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import threading


class Ui_Form(object):
    host_ip = ""
    port = 0
    nickname = ""

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1603, 1473)
        self.hostLbl = QtWidgets.QLabel(Form)
        self.hostLbl.setGeometry(QtCore.QRect(20, 30, 89, 25))
        self.hostLbl.setObjectName("hostLbl")
        self.portLbl = QtWidgets.QLabel(Form)
        self.portLbl.setGeometry(QtCore.QRect(500, 30, 89, 25))
        self.portLbl.setObjectName("portLbl")
        self.logLbl = QtWidgets.QLabel(Form)
        self.logLbl.setGeometry(QtCore.QRect(820, 250, 291, 25))
        self.logLbl.setObjectName("logLbl")
        self.msgLbl = QtWidgets.QLabel(Form)
        self.msgLbl.setGeometry(QtCore.QRect(30, 250, 89, 25))
        self.msgLbl.setObjectName("msgLbl")
        self.hostTxt = QtWidgets.QLineEdit(Form)
        self.hostTxt.setGeometry(QtCore.QRect(20, 70, 411, 31))
        self.hostTxt.setObjectName("hostTxt")
        self.portTxt = QtWidgets.QLineEdit(Form)
        self.portTxt.setGeometry(QtCore.QRect(500, 70, 411, 31))
        self.portTxt.setObjectName("portTxt")
        self.connectBtn = QtWidgets.QPushButton(Form)
        self.connectBtn.setGeometry(QtCore.QRect(20, 120, 150, 46))
        self.connectBtn.setObjectName("connectBtn")
        self.msgTxt = QtWidgets.QTextEdit(Form)
        self.msgTxt.setEnabled(False)
        self.msgTxt.setGeometry(QtCore.QRect(30, 280, 751, 711))
        self.msgTxt.setObjectName("msgTxt")
        self.logTxt = QtWidgets.QTextEdit(Form)
        self.logTxt.setEnabled(False)
        self.logTxt.setReadOnly(True)
        self.logTxt.setGeometry(QtCore.QRect(820, 280, 751, 711))
        self.logTxt.setObjectName("logTxt")
        self.sendBtn = QtWidgets.QPushButton(Form)
        self.sendBtn.setEnabled(False)
        self.sendBtn.setGeometry(QtCore.QRect(30, 1010, 150, 46))
        self.sendBtn.setObjectName("sendBtn")
        self.nicknameTxt = QtWidgets.QLineEdit(Form)
        self.nicknameTxt.setEnabled(False)
        self.nicknameTxt.setGeometry(QtCore.QRect(990, 70, 411, 31))
        self.nicknameTxt.setObjectName("nicknameTxt")
        self.nicknameBtn = QtWidgets.QPushButton(Form)
        self.nicknameBtn.setEnabled(False)
        self.nicknameBtn.setGeometry(QtCore.QRect(990, 120, 150, 46))
        self.nicknameBtn.setObjectName("nicknameBtn")
        self.nicknameLbl = QtWidgets.QLabel(Form)
        self.nicknameLbl.setGeometry(QtCore.QRect(990, 30, 111, 25))
        self.nicknameLbl.setObjectName("nicknameLbl")
        self.closeBtn = QtWidgets.QPushButton(Form)
        self.closeBtn.setEnabled(False)
        self.closeBtn.setGeometry(QtCore.QRect(820, 1010, 150, 46))
        self.closeBtn.setObjectName("closeBtn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.connectBtn.clicked.connect(lambda: self.connect_setup())
        self.nicknameBtn.clicked.connect(lambda: self.nickname_setup(self.client_socket))
        self.sendBtn.clicked.connect(lambda: self.write(Ui_Form.nickname, self.client_socket))
        self.closeBtn.clicked.connect(lambda: self.close_client(self.client_socket))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.hostLbl.setText(_translate("Form", "Host IP:"))
        self.portLbl.setText(_translate("Form", "Port:"))
        self.logLbl.setText(_translate("Form", "Message Log:"))
        self.msgLbl.setText(_translate("Form", "Message:"))
        self.connectBtn.setText(_translate("Form", "Connect"))
        self.sendBtn.setText(_translate("Form", "Send Message"))
        self.nicknameBtn.setText(_translate("Form", "Set Nickname"))
        self.nicknameLbl.setText(_translate("Form", "Nickname:"))
        self.closeBtn.setText(_translate("Form", "Close Client"))

    def connect_setup(self):
        self.logTxt.setEnabled(True)
        Ui_Form.host_ip = self.hostTxt.text()
        Ui_Form.port = self.portTxt.text()
        while True:
            if Ui_Form.port.isdigit():
                if 10000 <= int(Ui_Form.port) <= 65535:
                    self.client_socket = socket
                    self.client_socket = self.client_socket.socket(self.client_socket.AF_INET, self.client_socket.SOCK_STREAM)

                    try:
                        self.client_socket.connect((Ui_Form.host_ip, int(Ui_Form.port)))
                        break
                    except:
                        self.logTxt.insertPlainText("Host IP number or port number is incorrect. Please recheck your information "
                                                    "and try again.\nIf problem persists, you can try creating a server and inviting friends!\n")
                        self.client_socket.close()
                        return
            else:
                self.logTxt.insertPlainText("Host IP or port is incorrect. Port must be between 10000 and 65535.\n")
                return

        self.connectBtn.setEnabled(False)
        self.hostTxt.setEnabled(False)
        self.portTxt.setEnabled(False)
        self.nicknameTxt.setEnabled(True)
        self.nicknameBtn.setEnabled(True)
        self.logTxt.insertPlainText("Socket succeeded.\n")
        return


    def nickname_setup(self, client_socket):
        Ui_Form.nickname = self.nicknameTxt.text()
        if Ui_Form.nickname.isspace() or len(Ui_Form.nickname) == 0:
            self.msgTxt.insertPlainText("Incorrect nickname. Nickname can't be white space.\n")
            return
        else:
            self.nicknameTxt.setEnabled(False)
            self.nicknameBtn.setEnabled(False)
            self.msgTxt.setEnabled(True)
            self.sendBtn.setEnabled(True)
            self.closeBtn.setEnabled(True)
            self.logTxt.insertPlainText(f"Nickname set to {Ui_Form.nickname}.\n")
            self.logTxt.insertPlainText("Client starting.\n")
            self.msgTxt.clear()
            threading.Thread(target=self.client, args=(Ui_Form.nickname, client_socket,)).start()
            client_socket.sendall(Ui_Form.nickname.encode('ascii'))
            return


    def write(self, nickname, client_socket):
        message = f'{nickname}: {self.msgTxt.toPlainText()}'
        if message:
            client_socket.sendall(message.encode())
            self.msgTxt.clear()
            
    def close_client(self, client_socket):
        client_socket.close()
        self.logTxt.clear()
        self.logTxt.setEnabled(False)
        self.msgTxt.setEnabled(False)
        self.closeBtn.setEnabled(False)
        self.sendBtn.setEnabled(False)
        self.connectBtn.setEnabled(True)
        self.hostTxt.setEnabled(True)
        self.portTxt.setEnabled(True)
        return

    def client(self, nickname, client_socket):
        def receive():
            while True:
                try:
                    msg = client_socket.recv(1024).decode('ascii')
                    if msg == 'NICK':
                        client_socket.sendall(nickname.encode('ascii'))
                    else:
                        self.logTxt.insertPlainText(msg + "\n")
                except:
                    self.logTxt.insertPlainText("Error \n")
                    self.close_client(client_socket)
                    break

        receive_thread = threading.Thread(target=receive)
        receive_thread.start()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())