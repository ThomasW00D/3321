from __future__ import print_function

import os.path
import sys
import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
import mimetypes

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GMail():
    def __init__(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """

        self.inbox_messages = []
        self.trash_messages = []
        self.draft_messages = []
        self.sent_messages = []
        self.spam_messages = []
        self.address = ''

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '3321/GMail/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            self.service = build('gmail', 'v1', credentials=creds)
            self.address = self.service.users().getProfile(userId='me').execute()
            self.address = self.address['emailAddress']
            
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

    def sendEmail(self, sender, to, subject='', msg_html=None, msg_plain=None, cc=None, bcc=None, attachments=None):
        msg = self.createEmail(sender, to, subject, msg_html, msg_plain, cc=cc, bcc=bcc, attachments=attachments)

        try:
            # Call the Gmail API
            self.service.users().messages().send(userId='me', body=msg).execute()

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

    def createEmail(self, sender, to, subject='', msg_html=None, msg_plain=None, cc=None, bcc=None, attachments=None):
        msg = MIMEMultipart('mixed' if attachments else 'alternative')
        msg['To'] = to
        msg['Sender'] = sender
        msg['Subject'] = subject

        if cc:
            msg['Cc'] = ', '.join(cc)

        if bcc:
            msg['Bcc'] = ', '.join(bcc)

        attach_plain = MIMEMultipart('alternative') if attachments else msg
        attach_html = MIMEMultipart('related') if attachments else msg

        if msg_plain:
            attach_plain.attach(MIMEText(msg_plain, 'plain'))

        if msg_html:
            attach_html.attach(MIMEText(msg_html, 'html'))

        if attachments != [] and attachments is not None:
            attach_plain.attach(attach_html)
            msg.attach(attach_plain)

            self.readyAttachments(msg, attachments)

        encoded_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        return { 'raw' : encoded_message}
    
    def readyAttachments(self, msg, attachments):
        for path in attachments:
            content_type, encoding = mimetypes.guess_type(path)

            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'

            main_type, sub_type = content_type.split('/', 1)
            with open(path, 'rb') as file:
                raw_data = file.read()

                attm = None
                if main_type == 'text':
                    attm = MIMEText(raw_data.decode('utf-8'), _subtype=sub_type)
                elif main_type == 'image':
                    attm = MIMEImage(raw_data, _subtype=sub_type)
                elif main_type == 'audio':
                    attm = MIMEAudio(raw_data, _subtype=sub_type)
                elif main_type == 'application':
                    attm = MIMEApplication(raw_data, _subtype=sub_type)
                else:
                    attm = MIMEBase(main_type, sub_type)
                    attm.set_payload(raw_data)

            file_name = os.path.basename(path)
            attm.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(attm)

    def getEmails(self, user_id='me', labels=None):

        if labels is None:
            labels = []

        try:
            # Call the Gmail API
            response = self.service.users().messages().list(userId=user_id, labelIds=labels, includeSpamTrash=True, maxResults=10).execute()
            messages = response['messages']

            for obj in messages:
                message = self.service.users().messages().get(userId=user_id, id=obj['id']).execute()
                
                for label in message['labelIds']:
                    if label == 'SENT':
                        self.sent_messages.append(message)
                        break
                    elif label == 'TRASH':
                        self.trash_messages.append(message)
                        break
                    elif label == 'SPAM':
                        self.spam_messages.append(message)
                        break
                    elif label == 'DRAFT':
                        self.draft_messages.append(message)
                        break
                    else:
                        self.inbox_messages.append(message)
                        break

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

        return self.sent_messages, self.draft_messages, self.inbox_messages, self.spam_messages, self.trash_messages
    
    # Function for getting the inbox emails the first time
    # If getting inbox for the second time, call inboxRefresh
    def getInbox(self, user_id='me', label='INBOX'):
        try:
            # Call the Gmail API
            response = self.service.users().messages().list(userId=user_id, labelIds=[label], includeSpamTrash=True, maxResults=5).execute()
            messages = response['messages']

            for obj in messages:
                message = self.service.users().messages().get(userId=user_id, id=obj['id']).execute()
                self.inbox_messages.append(message)

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

        return self.inbox_messages
    
    # Function for getting the trashed emails the first time
    # If getting trash for the second time, call trashRefresh
    def getTrash(self, user_id='me', label='TRASH'):
        try:
            # Call the Gmail API
            response = self.service.users().messages().list(userId=user_id, labelIds=[label], includeSpamTrash=True, maxResults=25).execute()
            messages = response['messages']

            for obj in messages:
                message = self.service.users().messages().get(userId=user_id, id=obj['id']).execute()
                self.trash_messages.append(message)

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

        return self.trash_messages
    
    # Function for getting the draft emails the first time
    # If getting draft for the second time, call draftRefresh
    def getDrafts(self, user_id='me', label='DRAFT'):
        try:
            # Call the Gmail API
            response = self.service.users().messages().list(userId=user_id, labelIds=[label], includeSpamTrash=True, maxResults=25).execute()
            messages = response['messages']

            for obj in messages:
                message = self.service.users().messages().get(userId=user_id, id=obj['id']).execute()
                self.draft_messages.append(message)

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

        return self.draft_messages
    
    # Function for getting the sent emails the first time
    # If getting sent emails for the second time, call sentRefresh
    def getSent(self, user_id='me', label='SENT'):
        try:
            # Call the Gmail API
            response = self.service.users().messages().list(userId=user_id, labelIds=[label], includeSpamTrash=True, maxResults=25).execute()
            messages = response['messages']

            for obj in messages:
                message = self.service.users().messages().get(userId=user_id, id=obj['id']).execute()
                self.sent_messages.append(message)

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

        return self.sent_messages
    
    # Function for getting the spam emails the first time
    # If getting spam for the second time, call spamRefresh
    def getSpam(self, user_id='me', label='SPAM'):
        try:
            # Call the Gmail API
            response = self.service.users().messages().list(userId=user_id, labelIds=[label], includeSpamTrash=True, maxResults=25).execute()
            messages = response['messages']

            for obj in messages:
                message = self.service.users().messages().get(userId=user_id, id=obj['id']).execute()
                self.spam_messages.append(message)

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

        return self.spam_messages
    
    def getSubjectAndSender(self, messages):
        ret = []
        for msg in messages:
            header = msg['payload']['headers']
            subject = '(no subject)'

            for obj in header:
                if obj['name'] == 'Subject':
                    subject = obj['value']
                elif obj['name'] == 'From':
                    email_from = obj['value']
                    sender = email_from.split('<', 1)[0]
            
            email_str = sender + ':\n' + subject
            ret.append(email_str)
        
        return ret
    
    def getSubjectAndRecipient(self, messages):
        ret = []
        for msg in messages:
            header = msg['payload']['headers']
            subject = '(no subject)'

            for obj in header:
                if obj['name'] == 'Subject':
                    subject = obj['value']
                elif obj['name'] == 'To':
                    email_to = obj['value']
                    recipient = email_to.split('<', 1)[0]

            email_str = recipient + ':\n' + subject
            ret.append(email_str)

        return ret
    
    def refreshInbox(self):
        try:
            # Call the Gmail API
            response = self.service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
            message = response['messages']

            if message[0]['id'] == self.inbox_messages[0]['id']:
                return self.inbox_messages, False
            else:
                self.inbox_messages.insert(0, message)
                return self.inbox_messages, True

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')
        
    def refreshSent(self):
        try:
            # Call the Gmail API
            response = self.service.users().messages().list(userId='me', labelIds=['SENT'], maxResults=1).execute()
            message = response['messages']

            if message[0]['id'] == self.sent_messages[0]['id']:
                return self.sent_messages
            else:
                self.sent_messages.insert(0, message)
                return self.sent_messages

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

    def refreshDrafts(self):
        try:
            # Call the Gmail API
            response = self.service.users().messages().list(userId='me', labelIds=['DRAFT'], maxResults=1).execute()
            message = response['messages']

            if message[0]['id'] == self.draft_messages[0]['id']:
                return self.draft_messages
            else:
                self.draft_messages.insert(0, message)
                return self.draft_messages

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

    def refreshSpam(self):
        try:
            # Call the Gmail API
            response = self.service.users().messages().list(userId='me', labelIds=['SPAM'], maxResults=1).execute()
            message = response['messages']

            if message[0]['id'] == self.spam_messages[0]['id']:
                return self.spam_messages
            else:
                self.spam_messages.insert(0, message)
                return self.spam_messages

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')

    def refreshTrash(self):
        try:
            # Call the Gmail API
            response = self.service.users().messages().list(userId='me', labelIds=['TRASH'], maxResults=1).execute()
            message = response['messages']

            if message[0]['id'] == self.trash_messages[0]['id']:
                return self.trash_messages
            else:
                self.trash_messages.insert(0, message)
                return self.trash_messages

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')
    
    def createDraft(self):
            pass

    def sendDraft(self):
        pass

