# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Host_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import socket
import random
import time


class Ui_Form(object):
    nickname = ""
    host_ip = ""
    port = 0
    server_socket = None
    client_socket = None

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

        self.createBtn.clicked.connect(
            lambda: threading.Thread(target=self.server).start()
        )
        self.nicknameBtn.clicked.connect(lambda: self.client_setup())
        self.sendBtn.clicked.connect(lambda: self.write(Ui_Form.nickname))
        self.closeBtn.clicked.connect(lambda: self.close_host())

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

    def client_setup(self):
        Ui_Form.nickname = self.nicknameTxt.text()
        if Ui_Form.nickname.isspace() or len(Ui_Form.nickname) == 0:
            self.msgTxt.insertPlainText(
                "Incorrect nickname. Nickname can't be white space.\n"
            )
            return
        else:
            self.nicknameTxt.setEnabled(False)
            self.nicknameBtn.setEnabled(False)
            self.msgTxt.setEnabled(True)
            self.logTxt.setEnabled(True)
            self.sendBtn.setEnabled(True)
            self.logTxt.insertPlainText(f"Nickname set to {Ui_Form.nickname}.\n")
            self.logTxt.insertPlainText("Client starting.\n")
            self.msgTxt.clear()
            Ui_Form.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Ui_Form.client_socket.connect((Ui_Form.host_ip, Ui_Form.port))
            threading.Thread(target=self.client, args=(Ui_Form.nickname,)).start()
            return

    def write(self, nickname):
        message = f"(Host) {nickname}: {self.msgTxt.toPlainText()}"
        time.sleep(0.1)
        if message:
            Ui_Form.client_socket.sendall(message.encode())
            time.sleep(0.1)
            self.msgTxt.clear()

    def close_host(self):
        self.logTxt.clear()
        self.serverTxt.clear()
        self.closeBtn.setEnabled(False)
        self.createBtn.setEnabled(True)
        self.nicknameBtn.setEnabled(False)
        self.sendBtn.setEnabled(False)
        self.msgTxt.setEnabled(False)
        self.logTxt.setEnabled(False)
        self.serverTxt.setEnabled(False)
        self.nicknameTxt.setEnabled(False)
        Ui_Form.client_socket.close()
        Ui_Form.server_socket.close()
        return

    def server(self):
        self.serverTxt.setEnabled(True)
        self.createBtn.setEnabled(False)
        self.closeBtn.setEnabled(True)
        Ui_Form.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Ui_Form.host_ip = socket.gethostbyname(socket.gethostname())
        time.sleep(0.1)
        while Ui_Form.server_socket:
            randint = random.randint(10000, 65535)
            Ui_Form.port = randint
            try:
                Ui_Form.server_socket.bind((Ui_Form.host_ip, Ui_Form.port))
                break
            except:
                self.serverTxt.insertPlainText(
                    f"Port {Ui_Form.port} was taken. Reattempting.\n"
                )
                time.sleep(0.1)
                continue

        self.nicknameBtn.setEnabled(True)
        self.nicknameTxt.setEnabled(True)
        self.serverTxt.insertPlainText(
            f"Host IP: {Ui_Form.host_ip}\nHost Port: {Ui_Form.port}\n"
        )
        time.sleep(0.1)
        Ui_Form.server_socket.listen()

        clients = []
        nicknames = []

        def broadcast(msg):
            for client in clients:
                client.send(msg)
                time.sleep(0.01)

        def handle(client):
            while True:
                try:
                    msg = client.recv(1024)
                    broadcast(msg)
                    time.sleep(0.1)
                except:
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    nickname = nicknames[index]
                    broadcast(f"{nickname} left the chat.\n".encode("ascii"))
                    time.sleep(0.1)
                    nicknames.remove(nickname)
                    break

        def receive():
            while True:
                try:
                    client, address = Ui_Form.server_socket.accept()
                    self.serverTxt.insertPlainText(f"Connected with {str(address)}\n")
                    time.sleep(0.1)
                    client.sendall("NICK".encode("ascii"))
                    nickname = client.recv(1024).decode("ascii")
                    time.sleep(0.1)
                    nicknames.append(nickname)
                    clients.append(client)

                    self.serverTxt.insertPlainText(
                        f"Nickname of new client is {nickname}.\n"
                    )
                    time.sleep(0.1)
                    broadcast(f"{nickname} joined the chat.\n".encode("ascii"))
                    time.sleep(0.1)
                    client.sendall("Connected to the server.\n".encode("ascii"))
                    time.sleep(0.1)

                    handle_thread = threading.Thread(target=handle, args=(client,))
                    handle_thread.start()
                except:
                    self.serverTxt.insertPlainText("Server closed.\n")
                    break

        self.serverTxt.insertPlainText("Server is listening.\n")
        time.sleep(0.1)

        receive()

    def client(self, nickname):
        def receive():
            while True:
                try:
                    msg = Ui_Form.client_socket.recv(1024).decode("ascii")
                    if msg == 'NICK':
                        Ui_Form.client_socket.sendall(nickname.encode("ascii"))
                    else:
                        self.logTxt.insertPlainText(msg + "\n")
                        time.sleep(0.1)
                    time.sleep(0.1)
                except:
                    self.logTxt.insertPlainText("Error \n")
                    time.sleep(0.1)
                    Ui_Form.client_socket.close()
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
