from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from gmail import *
import sys

class MainGUI( QMainWindow ):	
    def __init__( self ):
        super(MainGUI, self).__init__()

    def composeClicked(self):
        dlg = ComposeDialog(parent=mainWindow)
        recipient, subject, body, attachments, send = dlg.getResults()
        filePaths = []

        for attm in attachments:
            filePaths.append(attm[0])

        if send == True:
            self.gmail.sendEmail(self.gmail.address, recipient, subject, msg_plain=body, attachments=filePaths)
            self.refreshClicked()
        else:
            self.gmail.createDraft(self.gmail.address, recipient, subject, msg_plain=body, attachments=filePaths)

    def itemClicked(self):
        if self.currInbox != 'DRAFT':
            message = self.gmail.getEmail(self.currInbox, self.emailList.currentRow())
            sender, recipient, _, subject = self.gmail.evaluateMessageHeader(message)
            payload = self.gmail.evaluateMessagePayload(message['payload'], 'me', message['id'])
            body = ''
            plain = True
            attachments = []

            for obj in payload:
                if obj['part_type'] == 'attachment':
                    attachments.append([obj, message['id']])
                elif obj['part_type'] == 'plain':
                    body = obj['body']
                elif obj['part_type'] == 'html':
                    body = obj['body']
                    plain = False

            if plain:
                dlg = ViewMessagePlain(body, sender, recipient, subject, attachments, self.gmail, self.currInbox, message['id'], mainWindow)
                clickedInbox, clickedSpam, clickedTrash = dlg.getResults()
                if clickedInbox:
                    self.firstInboxQuery = True
                    if self.currInbox == 'SPAM':
                        self.firstSpamQuery = True
                        self.spamClicked()
                    else:
                        self.firstTrashQuery = True
                        self.trashClicked()
                elif clickedSpam:
                    self.firstSpamQuery = True
                    if self.currInbox == 'INBOX':
                        self.firstInboxQuery = True
                        self.inboxClicked()
                    else:
                        self.firstTrashQuery = True
                        self.trashClicked()
                elif clickedTrash:
                    self.firstTrashQuery = True
                    if self.currInbox == 'INBOX':
                        self.firstInboxQuery = True
                        self.inboxClicked()
                    else:
                        self.firstSpamQuery = True
                        self.spamClicked()
                    
            else:
                dlg = ViewMessageHTML(body, sender, recipient, subject, attachments, self.gmail, self.currInbox, message['id'], mainWindow)
                clickedInbox, clickedSpam, clickedTrash = dlg.getResults()
                if clickedInbox:
                    self.firstInboxQuery = True
                    if self.currInbox == 'SPAM':
                        self.firstSpamQuery = True
                        self.spamClicked()
                    else:
                        self.firstTrashQuery = True
                        self.trashClicked()
                elif clickedSpam:
                    self.firstSpamQuery = True
                    if self.currInbox == 'INBOX':
                        self.firstInboxQuery = True
                        self.inboxClicked()
                    else:
                        self.firstTrashQuery = True
                        self.trashClicked()
                elif clickedTrash:
                    self.firstTrashQuery = True
                    if self.currInbox == 'INBOX':
                        self.firstInboxQuery = True
                        self.inboxClicked()
                    else:
                        self.firstSpamQuery = True
                        self.spamClicked()
        
        else:
            message = self.gmail.getEmail(self.currInbox, self.emailList.currentRow())
            draft_id = self.gmail.getDraftID(self.emailList.currentRow())
            sender, _, recAddress, subject = self.gmail.evaluateMessageHeader(message)
            sender = sender[6:]
            if subject != '(No Subject)':
                subject = subject[9:]
            recAddress = recAddress[4:]
            payload = self.gmail.evaluateMessagePayload(message['payload'], 'me', message['id'])
            body = ''
            plain = True
            attachments = []

            for obj in payload:
                if obj['part_type'] == 'attachment':
                    attachments.append([obj, message['id']])
                elif obj['part_type'] == 'plain':
                    body = obj['body']
                elif obj['part_type'] == 'html':
                    body = obj['body']
                    plain = False

            dlg = ComposeDialog(subject, recAddress, body, True, mainWindow)
            recipient, subject, body, attachments, send = dlg.getResults()
            filePaths = []

            for attm in attachments:
                filePaths.append(attm[0])

            if send == True:
                self.gmail.sendDraft(draft_id)
                self.firstDraftsQuery = True
                self.firstInboxQuery = True
                self.firstSentQuery = True
                self.refreshClicked()

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

        if self.firstInboxQuery:
            inbox = self.gmail.getInbox()
            inboxDisplay = self.gmail.getSubjectAndSender(inbox)
            self.firstInboxQuery = False
        else:
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
            trash = self.gmail.refreshTrash()
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

        self.firstInboxQuery = False
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
    def __init__(self, subject='Subject: ', to='To: ', body='Message Body: ', draft=False, parent=None):
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
        self.subjectEdit.setGeometry(15, 55, 465, 25)
        self.messageBody.setGeometry(15, 95, 465, 360)
        self.sendButton.setGeometry(420, 465, 70, 25)
        self.attachButton.setGeometry(15, 465, 150, 25)

        if not draft:
            self.toEdit.setPlaceholderText(to)
            self.subjectEdit.setPlaceholderText(subject)
            self.messageBody.setPlaceholderText(body)
        else:
            self.toEdit.setText(to)
            self.subjectEdit.setText(subject)
            self.messageBody.setText(body)

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
        else:
            recipient = self.toEdit.text()
            subject = self.subjectEdit.text()
            body = self.messageBody.toPlainText()
            attachments = self.filePaths
            send = False
            return recipient, subject, body, attachments, send

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

class ViewMessagePlain(QDialog):
    def __init__(self, message_body, sender, recipient, subject, attachments, gmail, currInbox, msg_id, parent=None):
        super().__init__(parent)

        QButton = QDialogButtonBox.Ok
        self.setWindowTitle('Email View')
        self.setFixedHeight(500)
        self.setFixedWidth(500)
        self.buttonBox = QDialogButtonBox(QButton)
        self.buttonBox.accepted.connect(self.accept)

        self.clickedInbox = False
        self.clickedSpam = False
        self.clickedTrash = False

        self.layout = QVBoxLayout()
        self.footerLayout = QHBoxLayout()
        self.bodyLayout = QVBoxLayout()
        self.attmLayout = QHBoxLayout()
        
        headerLabel = QLabel(sender + '\n' + recipient)
        trashButton = QPushButton('Move to Trash')
        spamButton = QPushButton('Mark as Spam')
        inboxButton = QPushButton('Move to Inbox')
        subjectLabel = QLabel(subject)
        subjectLabel.setWordWrap(True)
        bodyLabel = ScrollLabel(self)
        bodyLabel.setText(message_body)
        self.downloadButton = QPushButton('Download Attachments')
        attmString = 'Attachments: '

        for obj in attachments:
            attmString += obj[0]['filename']

        attmLabel = QLabel(attmString)
        attmLabel.setWordWrap(True)

        self.bodyLayout.setAlignment(Qt.AlignTop)
        self.bodyLayout.setSpacing(15)
        self.bodyLayout.addWidget(headerLabel)
        self.bodyLayout.addWidget(subjectLabel)
        self.bodyLayout.addWidget(bodyLabel)

        if attachments != []:
            self.attmLayout.addWidget(attmLabel)
            self.attmLayout.addWidget(self.downloadButton)
        
        if currInbox == 'INBOX':
            self.footerLayout.addWidget(spamButton)
            self.footerLayout.addWidget(trashButton)
        elif currInbox == 'SPAM':
            self.footerLayout.addWidget(inboxButton)
            self.footerLayout.addWidget(trashButton)
        elif currInbox == 'TRASH':
            self.footerLayout.addWidget(inboxButton)
            self.footerLayout.addWidget(spamButton)
        self.footerLayout.addWidget(self.buttonBox)

        self.layout.addLayout(self.bodyLayout)
        self.layout.addLayout(self.attmLayout)
        self.layout.addLayout(self.footerLayout)
        self.setLayout(self.layout)

        self.downloadButton.clicked.connect(lambda: self.downloadClicked(attachments, gmail))
        inboxButton.clicked.connect(lambda: self.inboxClicked(msg_id, gmail, currInbox))
        spamButton.clicked.connect(lambda: self.spamClicked(msg_id, gmail, currInbox))
        trashButton.clicked.connect(lambda: self.trashClicked(msg_id, gmail, currInbox))

    def downloadClicked(self, attachments, gmail):
        for attachment in attachments:
            gmail.downloadAttachment(attachment[0], attachment[1])

    def inboxClicked(self, msg_id, gmail, currInbox):
        gmail.changeLabels(msg_id, 'INBOX', currInbox)
        self.clickedInbox = True
        self.accept()

    def spamClicked(self, msg_id, gmail, currInbox):
        gmail.changeLabels(msg_id, 'SPAM', currInbox)
        self.clickedSpam = True
        self.accept()

    def trashClicked(self, msg_id, gmail, currInbox):
        gmail.changeLabels(msg_id, 'TRASH', currInbox)
        self.clickedTrash = True
        self.accept()

    def getResults(self):
        ret = self.exec()
        if ret == 1:
            return self.clickedInbox, self.clickedSpam, self.clickedTrash
        else:
            return self.clickedInbox, self.clickedSpam, self.clickedTrash



class ViewMessageHTML(QDialog):
    def __init__(self, message_body, sender, recipient, subject, attachments, gmail, currInbox, msg_id, parent=None):
        super().__init__(parent)

        QButton = QDialogButtonBox.Ok
        self.setWindowTitle('Email View')
        self.setFixedWidth(850)
        self.buttonBox = QDialogButtonBox(QButton)
        self.buttonBox.accepted.connect(self.accept)

        self.clickedInbox = False
        self.clickedSpam = False
        self.clickedTrash = False

        self.layout = QVBoxLayout()
        self.footerLayout = QHBoxLayout()
        self.bodyLayout = QVBoxLayout()
        self.attmLayout = QHBoxLayout()

        headerLabel = QLabel(sender + '\n' + recipient)
        trashButton = QPushButton('Move to Trash')
        spamButton = QPushButton('Mark as Spam')
        inboxButton = QPushButton('Move to Inbox')
        subjectLabel = QLabel(subject)
        subjectLabel.setWordWrap(True)
        webView = QWebEngineView()
        webView.setHtml(message_body)
        self.downloadButton = QPushButton('Download Attachments')
        attmString = 'Attachments: '

        for obj in attachments:
            attmString += obj[0]['filename']

        attmLabel = QLabel(attmString)
        attmLabel.setWordWrap(True)

        self.bodyLayout.setAlignment(Qt.AlignTop)
        self.bodyLayout.setSpacing(15)
        self.bodyLayout.addWidget(headerLabel)
        self.bodyLayout.addWidget(subjectLabel)
        self.bodyLayout.addWidget(webView)
        
        if attachments != []:
            self.attmLayout.addWidget(attmLabel)
            self.attmLayout.addWidget(self.downloadButton)

        if currInbox == 'INBOX':
            self.footerLayout.addWidget(spamButton)
            self.footerLayout.addWidget(trashButton)
        elif currInbox == 'SPAM':
            self.footerLayout.addWidget(inboxButton)
            self.footerLayout.addWidget(trashButton)
        elif currInbox == 'TRASH':
            self.footerLayout.addWidget(inboxButton)
            self.footerLayout.addWidget(spamButton)
        self.footerLayout.addWidget(self.buttonBox)

        self.layout.addLayout(self.bodyLayout)
        self.layout.addLayout(self.attmLayout)
        self.layout.addLayout(self.footerLayout)
        self.setLayout(self.layout)

        self.downloadButton.clicked.connect(lambda: self.downloadClicked(attachments, gmail))
        inboxButton.clicked.connect(lambda: self.inboxClicked(msg_id, gmail, currInbox))
        spamButton.clicked.connect(lambda: self.spamClicked(msg_id, gmail, currInbox))
        trashButton.clicked.connect(lambda: self.trashClicked(msg_id, gmail, currInbox))

    def downloadClicked(self, attachments, gmail):
        for attachment in attachments:
            gmail.downloadAttachment(attachment[0], attachment[1])

    def inboxClicked(self, msg_id, gmail, currInbox):
        gmail.changeLabels(msg_id, 'INBOX', currInbox)
        self.clickedInbox = True
        self.accept()

    def spamClicked(self, msg_id, gmail, currInbox):
        gmail.changeLabels(msg_id, 'SPAM', currInbox)
        self.clickedSpam = True
        self.accept()

    def trashClicked(self, msg_id, gmail, currInbox):
        gmail.changeLabels(msg_id, 'TRASH', currInbox)
        self.clickedTrash = True
        self.accept()

    def getResults(self):
        ret = self.exec()
        if ret == 1:
            return self.clickedInbox, self.clickedSpam, self.clickedTrash
        else:
            return self.clickedInbox, self.clickedSpam, self.clickedTrash

class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        self.setWidgetResizable(True)

        content = QWidget(self)
        self.setWidget(content)

        layout = QVBoxLayout(content)

        self.label = QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)

        layout.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QWidget()
    gui = MainGUI()
    gui.initUI(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())