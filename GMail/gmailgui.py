import sys

from gmail import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QDialog, QWidget, QListWidget, QListWidgetItem, QPushButton, QLabel, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog, QTextEdit, QApplication


class MainGUI( QMainWindow ):	
    def __init__( self ):
        super(MainGUI, self).__init__()

    def composeClicked(self):
        dlg = ComposeDialog(parent=self.mainWindow)
        recipient, subject, body, attachments, send, draft = dlg.getResults()
        filePaths = []

        for attm in attachments:
            filePaths.append(attm[0])

        if send:
            self.gmail.sendEmail(self.gmail.address, recipient, subject, msg_plain=body, attachments=filePaths)
            self.refreshClicked(True)
        elif draft:
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
                    body += obj['body']
                elif obj['part_type'] == 'html':
                    body = obj['body']
                    plain = False

            if plain:
                dlg = ViewMessagePlain(body, sender, recipient, subject, attachments, self.gmail, self.currInbox, message['id'], self.mainWindow)
                clickedInbox, clickedSpam, clickedTrash = dlg.getResults()
                if clickedInbox:
                    self.firstInboxQuery = True
                    if self.currInbox == 'SPAM':
                        self.firstSpamQuery = True
                        self.spamClicked(self.firstSpamQuery)
                    else:
                        self.firstTrashQuery = True
                        self.trashClicked(self.firstTrashQuery)
                elif clickedSpam:
                    self.firstSpamQuery = True
                    if self.currInbox == 'INBOX':
                        self.firstInboxQuery = True
                        self.inboxClicked(self.firstInboxQuery)
                    else:
                        self.firstTrashQuery = True
                        self.trashClicked(self.firstTrashQuery)
                elif clickedTrash:
                    self.firstTrashQuery = True
                    if self.currInbox == 'INBOX':
                        self.firstInboxQuery = True
                        self.inboxClicked(self.firstInboxQuery)
                    else:
                        self.firstSpamQuery = True
                        self.spamClicked(self.firstSpamQuery)
                    
            else:
                dlg = ViewMessageHTML(body, sender, recipient, subject, attachments, self.gmail, self.currInbox, message['id'], self.mainWindow)
                clickedInbox, clickedSpam, clickedTrash = dlg.getResults()
                if clickedInbox:
                    self.firstInboxQuery = True
                    if self.currInbox == 'SPAM':
                        self.firstSpamQuery = True
                        self.spamClicked(self.firstSpamQuery)
                    else:
                        self.firstTrashQuery = True
                        self.trashClicked(self.firstTrashQuery)
                elif clickedSpam:
                    self.firstSpamQuery = True
                    if self.currInbox == 'INBOX':
                        self.firstInboxQuery = True
                        self.inboxClicked(self.firstInboxQuery)
                    else:
                        self.firstTrashQuery = True
                        self.trashClicked(self.firstTrashQuery)
                elif clickedTrash:
                    self.firstTrashQuery = True
                    if self.currInbox == 'INBOX':
                        self.firstInboxQuery = True
                        self.inboxClicked(self.firstInboxQuery)
                    else:
                        self.firstSpamQuery = True
                        self.spamClicked(self.firstSpamQuery)
        
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

            dlg = ComposeDialog(subject, recAddress, body, True, self.mainWindow)
            recipient, subject, body, attachments, send, _ = dlg.getResults()
            filePaths = []

            for attm in attachments:
                filePaths.append(attm[0])

            if send == True:
                self.gmail.updateDraft(self.gmail.address, recAddress, draft_id, subject, msg_plain=body, attachments=filePaths)
                self.gmail.sendDraft(draft_id)
                self.firstDraftsQuery = True
                self.firstInboxQuery = True
                self.firstSentQuery = True
                self.refreshClicked(True)
            else:
                self.gmail.updateDraft(self.gmail.address, recAddress, draft_id, subject, msg_plain=body, attachments=filePaths)
            

    def refreshClicked(self, fullReload):
        if self.currInbox == 'INBOX':
            self.inboxClicked(fullReload)
        elif self.currInbox == 'SENT':
            self.sentClicked(fullReload)
        elif self.currInbox == 'DRAFT':
            self.draftsClicked(fullReload)
        elif self.currInbox == 'SPAM':
            self.spamClicked(fullReload)
        else:
            self.trashClicked(fullReload)

    def inboxClicked(self, fullReload):
        self.currInbox = 'INBOX'
        self.enableAllButtons()
        self.inboxButton.setEnabled(False)
        self.emailList.clear()
        inbox = []

        if fullReload:
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
            

    def sentClicked(self, fullReload):
        self.currInbox = 'SENT'
        self.enableAllButtons()
        self.sentButton.setEnabled(False)
        self.emailList.clear()
        sent = []

        if fullReload:
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

    def draftsClicked(self, fullReload):
        self.currInbox = 'DRAFT'
        self.enableAllButtons()
        self.draftsButton.setEnabled(False)
        self.emailList.clear()
        drafts = []

        if fullReload:
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

    def spamClicked(self, fullReload):
        self.currInbox = 'SPAM'
        self.enableAllButtons()
        self.spamButton.setEnabled(False)
        self.emailList.clear()
        spam = []

        if fullReload:
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

    def trashClicked(self, fullReload):
        self.currInbox = 'TRASH'
        self.enableAllButtons()
        self.trashButton.setEnabled(False)
        self.emailList.clear()
        trash = []

        if fullReload:
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
        self.mainWindow = window

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

        self.emailList.setGeometry(155, 10, 835, 680)
        self.composeButton.setGeometry(15, 25, 120, 50)
        self.refreshButton.setGeometry(15, 75, 120, 30)
        self.inboxButton.setGeometry(0, 225, 150, 50)
        self.sentButton.setGeometry(0, 265, 150, 50)
        self.draftsButton.setGeometry(0, 305, 150, 50)
        self.spamButton.setGeometry(0, 345, 150, 50)
        self.trashButton.setGeometry(0, 385, 150, 50)

        window.setFixedWidth(1000)
        window.setFixedHeight(700)

        for msg in self.inboxDisplay:
            item = QListWidgetItem(msg)
            item.setSizeHint(QSize(0, 50))
            self.emailList.addItem(item)
        self.emailList.setAlternatingRowColors(True)
        self.inboxButton.setEnabled(False)

        self.composeButton.clicked.connect(self.composeClicked)
        self.inboxButton.clicked.connect(lambda: self.inboxClicked(True))
        self.sentButton.clicked.connect(lambda: self.sentClicked(True))
        self.draftsButton.clicked.connect(lambda: self.draftsClicked(True))
        self.spamButton.clicked.connect(lambda: self.spamClicked(True))
        self.trashButton.clicked.connect(lambda: self.trashClicked(True))
        self.refreshButton.clicked.connect(lambda: self.refreshClicked(True))
        self.emailList.itemClicked.connect(self.itemClicked)

class ComposeDialog(QDialog):
    def __init__(self, subject='Subject: ', to='To: ', body='Message Body: ', draft=False, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Compose")
        self.setFixedWidth(500)
        self.setFixedHeight(550)

        self.filePaths = []
        self.attachmentsString = 'Attachments: '

        self.toEdit = QLineEdit(self)
        self.subjectEdit = QLineEdit(self)
        self.messageBody = QTextEdit(self)
        self.sendButton = QPushButton('Send', self)
        self.attachButton = QPushButton('Add Attachments', self)
        self.attachmentLabel = QLabel(self.attachmentsString, self)

        self.toEdit.setGeometry(15, 15, 465, 25)
        self.subjectEdit.setGeometry(15, 55, 465, 25)
        self.messageBody.setGeometry(15, 95, 465, 325)
        self.sendButton.setGeometry(420, 505, 70, 25)
        self.attachButton.setGeometry(15, 505, 140, 25)
        self.attachmentLabel.setGeometry(15, 425, 250, 75)

        self.attachmentLabel.setWordWrap(True)

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
            self.attachmentsString += filePath[0].split('/')[-1] + ', '
            self.attachmentLabel.setText(self.attachmentsString)
        
    def getResults(self):
        result = self.exec()
        if result == 1:
            recipient = self.toEdit.text()
            subject = self.subjectEdit.text()
            body = self.messageBody.toPlainText()
            attachments = self.filePaths
            send = True
            draft = False
            return recipient, subject, body, attachments, send, draft
        else:
            recipient = self.toEdit.text()
            subject = self.subjectEdit.text()
            body = self.messageBody.toPlainText()
            attachments = self.filePaths
            send = False
            dlg = SaveDraftDialog()
            if dlg.exec() == 1:
                draft = True
            else:
                draft = False
            return recipient, subject, body, attachments, send, draft

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

class SaveDraftDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.layout = QVBoxLayout()

        message = QLabel('Would you like to save this email as a draft?')
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

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
            attmString += obj[0]['filename'] + ', '

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = MainGUI()
    ui.initUI(Form)
    Form.show()
    sys.exit(app.exec_())