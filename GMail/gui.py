from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from gmail import *
import sys

class MainGUI( QMainWindow ):	
    def __init__( self ):
        super(MainGUI, self).__init__()

    def composeClicked(self):
        dlg = ComposeDialog(mainWindow)
        recipient, subject, body, attachments, send = dlg.getResults()
        filePaths = []

        for attm in attachments:
            filePaths.append(attm[0])

        if send == True:
            self.gmail.sendEmail(self.gmail.address, recipient, subject, msg_plain=body, attachments=filePaths)
        else:
            pass

    def itemClicked(self, item):
        print(self.emailList.currentRow())

    def refreshClicked(self):
        if self.currInbox == 'INBOX':
            self.inboxClicked()
        elif self.currInbox == 'SENT':
            self.sentClicked()
        elif self.currInbox == 'DRAFT':
            self.draftsClicked()
        elif self.currInbox == 'SPAM':
            self.spamClicked()
        else:
            self.trashClicked()

    def inboxClicked(self):
        self.currInbox = 'INBOX'
        self.enableAllButtons()
        self.inboxButton.setEnabled(False)
        self.emailList.clear()
        inbox = []
        inbox = self.gmail.refreshInbox()
        inboxDisplay = self.gmail.getSubjectAndSender(inbox)

        for msg in inboxDisplay:
            item = QListWidgetItem(msg)
            item.setSizeHint(QSize(0, 50))
            self.emailList.addItem(item)

    def sentClicked(self):
        self.currInbox = 'SENT'
        self.enableAllButtons()
        self.sentButton.setEnabled(False)
        self.emailList.clear()
        sent = []

        if self.firstSentQuery:
            sent = self.gmail.getSent()
            sentDisplay = self.gmail.getSubjectAndRecipient(sent)
            self.firstSentQuery = False
        else:
            sent = self.gmail.refreshSent()
            sentDisplay = self.gmail.getSubjectAndRecipient(sent)

        for msg in sentDisplay:
            item = QListWidgetItem(msg)
            item.setSizeHint(QSize(0, 50))
            self.emailList.addItem(item)

    def draftsClicked(self):
        self.currInbox = 'DRAFT'
        self.enableAllButtons()
        self.draftsButton.setEnabled(False)
        self.emailList.clear()
        drafts = []

        if self.firstDraftsQuery:
            drafts = self.gmail.getDrafts()
            draftsDisplay = self.gmail.getSubjectAndRecipient(drafts)
            self.firstDraftsQuery = False
        else:
            drafts = self.gmail.refreshDrafts()
            draftsDisplay = self.gmail.getSubjectAndRecipient(drafts)

        for msg in draftsDisplay:
            item = QListWidgetItem(msg)
            item.setSizeHint(QSize(0, 50))
            self.emailList.addItem(item)

    def spamClicked(self):
        self.currInbox = 'SPAM'
        self.enableAllButtons()
        self.spamButton.setEnabled(False)
        self.emailList.clear()
        spam = []

        if self.firstSpamQuery:
            spam = self.gmail.getSpam()
            spamDisplay = self.gmail.getSubjectAndSender(spam)
            self.firstSpamQuery = False
        else:
            spam = self.gmail.refreshSpam()
            spamDisplay = self.gmail.getSubjectAndSender(spam)

        for msg in spamDisplay:
            item = QListWidgetItem(msg)
            item.setSizeHint(QSize(0, 50))
            self.emailList.addItem(item)

    def trashClicked(self):
        self.currInbox = 'TRASH'
        self.enableAllButtons()
        self.trashButton.setEnabled(False)
        self.emailList.clear()
        trash = []

        if self.firstTrashQuery:
            trash = self.gmail.getTrash()
            trashDisplay = self.gmail.getSubjectAndSender(trash)
            self.firstTrashQuery = False
        else:
            trash = self.gmail.getTrash()
            trashDisplay = self.gmail.getSubjectAndSender(trash)

        for msg in trashDisplay:
            item = QListWidgetItem(msg)
            item.setSizeHint(QSize(0, 50))
            self.emailList.addItem(item)

    def enableAllButtons(self):
        self.inboxButton.setEnabled(True)
        self.sentButton.setEnabled(True)
        self.draftsButton.setEnabled(True)
        self.spamButton.setEnabled(True)
        self.trashButton.setEnabled(True)


    def initUI(self, window):
        self.gmail = GMail()

        self.currInbox = 'INBOX'
        self.emailList = QListWidget(window)
        self.composeButton = QPushButton('Compose', window)
        self.refreshButton = QPushButton('Refresh', window)
        self.inboxButton = QPushButton('Inbox', window)
        self.sentButton = QPushButton('Sent', window)
        self.draftsButton = QPushButton('Drafts', window)
        self.spamButton = QPushButton('Spam', window)
        self.trashButton = QPushButton('Trash', window)

        self.firstSentQuery = True
        self.firstDraftsQuery = True
        self.firstSpamQuery = True
        self.firstTrashQuery = True

        self.inbox = self.gmail.getInbox()
        self.inboxDisplay = self.gmail.getSubjectAndSender(self.inbox)

        window.setWindowTitle("Email Inbox")

        self.emailList.setGeometry(150, 5, 645, 490)
        self.composeButton.setGeometry(15, 25, 120, 50)
        self.refreshButton.setGeometry(15, 75, 120, 30)
        self.inboxButton.setGeometry(0, 145, 150, 50)
        self.sentButton.setGeometry(0, 185, 150, 50)
        self.draftsButton.setGeometry(0, 225, 150, 50)
        self.spamButton.setGeometry(0, 265, 150, 50)
        self.trashButton.setGeometry(0, 305, 150, 50)

        window.setFixedWidth(800)
        window.setFixedHeight(500)

        for msg in self.inboxDisplay:
            item = QListWidgetItem(msg)
            item.setSizeHint(QSize(0, 50))
            self.emailList.addItem(item)
        self.emailList.setAlternatingRowColors(True)
        self.inboxButton.setEnabled(False)

        self.composeButton.clicked.connect(self.composeClicked)
        self.inboxButton.clicked.connect(self.inboxClicked)
        self.sentButton.clicked.connect(self.sentClicked)
        self.draftsButton.clicked.connect(self.draftsClicked)
        self.spamButton.clicked.connect(self.spamClicked)
        self.trashButton.clicked.connect(self.trashClicked)
        self.refreshButton.clicked.connect(self.refreshClicked)
        self.emailList.itemClicked.connect(self.itemClicked)

class ComposeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Compose")
        self.setFixedWidth(500)
        self.setFixedHeight(500)

        self.filePaths = []

        self.toEdit = QLineEdit(self)
        self.subjectEdit = QLineEdit(self)
        self.messageBody = QTextEdit(self)
        self.sendButton = QPushButton('Send', self)
        self.attachButton = QPushButton('Add Attachments', self)

        self.toEdit.setGeometry(15, 15, 465, 25)
        self.toEdit.setPlaceholderText('To: ')
        self.subjectEdit.setGeometry(15, 55, 465, 25)
        self.subjectEdit.setPlaceholderText('Subject: ')
        self.messageBody.setGeometry(15, 95, 465, 360)
        self.messageBody.setPlaceholderText('Message Body: ')
        self.sendButton.setGeometry(420, 465, 70, 25)
        self.attachButton.setGeometry(15, 465, 150, 25)

        self.sendButton.clicked.connect(self.sendClicked)
        self.attachButton.clicked.connect(self.attachClicked)

    def sendClicked(self):
        if self.toEdit.text() == '':
            dlg = NoRecipient(self)
            dlg.exec()
        elif self.messageBody.toPlainText() == '':
            dlg = EmptyBody(self)
            dlg.exec()
        else:
            self.accept()

    def attachClicked(self):
        filePath = QFileDialog.getOpenFileName(self)
        if filePath[0] != '':
            self.filePaths.append(filePath)
        
    def getResults(self):
        if self.exec() == 1:
            recipient = self.toEdit.text()
            subject = self.subjectEdit.text()
            body = self.messageBody.toPlainText()
            attachments = self.filePaths
            send = True
            return recipient, subject, body, attachments, send
        elif self.exec() == 0:
            recipient = self.toEdit.text()
            subject = self.subjectEdit.text()
            body = self.messageBody.toPlainText()
            attachments = self.filePaths
            send = False
            return recipient, subject, body, attachments, send
        else:
            return None

class NoRecipient(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        QButton = QDialogButtonBox.Ok
        self.setWindowTitle('Email Failed to Send')
        self.buttonBox = QDialogButtonBox(QButton)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()

        message = QLabel("'To:' field cannot be empty")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class EmptyBody(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        QButton = QDialogButtonBox.Ok
        self.setWindowTitle('Email Failed to Send')
        self.buttonBox = QDialogButtonBox(QButton)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()

        message = QLabel("Email body cannot be empty")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QWidget()
    gui = MainGUI()
    gui.initUI(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())