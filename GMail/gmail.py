from __future__ import print_function

import base64
import mimetypes
import os.path
import sys
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


class GMail:
    def __init__(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """

        self.inbox_messages = []
        self.trash_messages = []
        self.draft_messages = []
        self.sent_messages = []
        self.spam_messages = []
        self.address = ""

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        try:
            # Call the Gmail API
            self.service = build("gmail", "v1", credentials=creds)
            self.address = self.service.users().getProfile(userId="me").execute()
            self.address = self.address["emailAddress"]
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def sendEmail(
        self,
        sender,
        to,
        subject="",
        msg_html=None,
        msg_plain=None,
        cc=None,
        bcc=None,
        attachments=None,
    ):
        msg = self.createEmail(
            sender,
            to,
            subject,
            msg_html,
            msg_plain,
            cc=cc,
            bcc=bcc,
            attachments=attachments,
        )

        try:
            # Call the Gmail API
            self.service.users().messages().send(userId="me", body=msg).execute()
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def createEmail(
        self,
        sender,
        to,
        subject="",
        msg_html=None,
        msg_plain=None,
        cc=None,
        bcc=None,
        attachments=None,
        draft=False,
    ):
        msg = MIMEMultipart("mixed" if attachments else "alternative")
        msg["To"] = to
        msg["Sender"] = sender
        msg["Subject"] = subject

        if cc:
            msg["Cc"] = ", ".join(cc)
        if bcc:
            msg["Bcc"] = ", ".join(bcc)
        text_part = MIMEMultipart("alternative") if attachments else msg

        if msg_plain:
            text_part.attach(MIMEText(msg_plain, "plain"))
        if msg_html:
            text_part.attach(MIMEText(msg_html, "html"))
        if attachments:
            msg.attach(text_part)

            self.readyAttachments(msg, attachments)
        encoded_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        if not draft:
            return {"raw": encoded_message}
        else:
            return {"message": {"raw": encoded_message}}

    def readyAttachments(self, msg, attachments):
        for path in attachments:
            content_type, encoding = mimetypes.guess_type(path)

            if content_type is None or encoding is not None:
                content_type = "application/octet-stream"
            main_type, sub_type = content_type.split("/", 1)
            with open(path, "rb") as file:
                raw_data = file.read()

                attm: MIMEBase
                if main_type == "text":
                    attm = MIMEText(raw_data.decode("UTF-8"), _subtype=sub_type)
                elif main_type == "image":
                    attm = MIMEImage(raw_data, _subtype=sub_type)
                elif main_type == "audio":
                    attm = MIMEAudio(raw_data, _subtype=sub_type)
                elif main_type == "application":
                    attm = MIMEApplication(raw_data, _subtype=sub_type)
                else:
                    attm = MIMEBase(main_type, sub_type)
                    attm.set_payload(raw_data)
            file_name = os.path.basename(path)
            attm.add_header("Content-Disposition", "attachment", filename=file_name)
            msg.attach(attm)

    def getEmails(self, user_id="me", labels=None):
        if labels is None:
            labels = []
        try:
            # Call the Gmail API
            response = (
                self.service.users()
                .messages()
                .list(
                    userId=user_id,
                    labelIds=labels,
                    includeSpamTrash=True,
                    maxResults=10,
                )
                .execute()
            )
            messages = response["messages"]

            for obj in messages:
                message = (
                    self.service.users()
                    .messages()
                    .get(userId=user_id, id=obj["id"])
                    .execute()
                )

                for label in message["labelIds"]:
                    if label == "SENT":
                        self.sent_messages.append(message)
                        break
                    elif label == "TRASH":
                        self.trash_messages.append(message)
                        break
                    elif label == "SPAM":
                        self.spam_messages.append(message)
                        break
                    elif label == "DRAFT":
                        self.draft_messages.append(message)
                        break
                    else:
                        self.inbox_messages.append(message)
                        break
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")
        return (
            self.sent_messages,
            self.draft_messages,
            self.inbox_messages,
            self.spam_messages,
            self.trash_messages,
        )

    # Function for getting the inbox emails the first time
    # If getting inbox for the second time, call inboxRefresh
    def getInbox(self, user_id="me", label="INBOX"):
        self.inbox_messages = []
        try:
            # Call the Gmail API
            response = (
                self.service.users()
                .messages()
                .list(
                    userId=user_id,
                    labelIds=[label],
                    includeSpamTrash=True,
                    maxResults=30,
                )
                .execute()
            )
            if response["resultSizeEstimate"] == 0:
                return self.inbox_messages
            messages = response["messages"]

            for obj in messages:
                message = (
                    self.service.users()
                    .messages()
                    .get(userId=user_id, id=obj["id"])
                    .execute()
                )
                self.inbox_messages.append(message)
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")
        return self.inbox_messages

    # Function for getting the trashed emails the first time
    # If getting trash for the second time, call trashRefresh
    def getTrash(self, user_id="me", label="TRASH"):
        self.trash_messages = []
        try:
            # Call the Gmail API
            response = (
                self.service.users()
                .messages()
                .list(
                    userId=user_id,
                    labelIds=[label],
                    includeSpamTrash=True,
                    maxResults=25,
                )
                .execute()
            )

            if response["resultSizeEstimate"] == 0:
                return self.trash_messages
            messages = response["messages"]

            for obj in messages:
                message = (
                    self.service.users()
                    .messages()
                    .get(userId=user_id, id=obj["id"])
                    .execute()
                )
                self.trash_messages.append(message)
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")
        return self.trash_messages

    # Function for getting the draft emails the first time
    # If getting draft for the second time, call draftRefresh
    def getDrafts(self, user_id="me", label="DRAFT"):
        self.draft_messages = []
        try:
            # Call the Gmail API
            response = (
                self.service.users()
                .messages()
                .list(
                    userId=user_id,
                    labelIds=[label],
                    includeSpamTrash=True,
                    maxResults=25,
                )
                .execute()
            )

            if response["resultSizeEstimate"] == 0:
                return self.draft_messages
            messages = response["messages"]

            for obj in messages:
                message = (
                    self.service.users()
                    .messages()
                    .get(userId=user_id, id=obj["id"])
                    .execute()
                )
                self.draft_messages.append(message)
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")
        return self.draft_messages

    # Function for getting the sent emails the first time
    # If getting sent emails for the second time, call sentRefresh
    def getSent(self, user_id="me", label="SENT"):
        self.sent_messages = []
        try:
            # Call the Gmail API
            response = (
                self.service.users()
                .messages()
                .list(
                    userId=user_id,
                    labelIds=[label],
                    includeSpamTrash=True,
                    maxResults=25,
                )
                .execute()
            )

            if response["resultSizeEstimate"] == 0:
                return self.sent_messages
            messages = response["messages"]

            for obj in messages:
                message = (
                    self.service.users()
                    .messages()
                    .get(userId=user_id, id=obj["id"])
                    .execute()
                )
                self.sent_messages.append(message)
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")
        return self.sent_messages

    # Function for getting the spam emails the first time
    # If getting spam for the second time, call spamRefresh
    def getSpam(self, user_id="me", label="SPAM"):
        self.spam_messages = []
        try:
            # Call the Gmail API
            response = (
                self.service.users()
                .messages()
                .list(
                    userId=user_id,
                    labelIds=[label],
                    includeSpamTrash=True,
                    maxResults=25,
                )
                .execute()
            )

            if response["resultSizeEstimate"] == 0:
                return self.spam_messages
            messages = response["messages"]

            for obj in messages:
                message = (
                    self.service.users()
                    .messages()
                    .get(userId=user_id, id=obj["id"])
                    .execute()
                )
                self.spam_messages.append(message)
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")
        return self.spam_messages

    def getSubjectAndSender(self, messages):
        ret = []
        for msg in messages:
            header = msg["payload"]["headers"]
            subject = "(No Subject)"

            for obj in header:
                if obj["name"] == "Subject":
                    subject = obj["value"]
                elif obj["name"] == "From":
                    email_from = obj["value"]
                    sender = email_from.split("<", 1)[0]
            email_str = sender + ":\n" + subject
            ret.append(email_str)
        return ret

    def getSubjectAndRecipient(self, messages):
        ret = []
        for msg in messages:
            header = msg["payload"]["headers"]
            subject = "(No Subject)"

            for obj in header:
                if obj["name"] == "Subject":
                    subject = obj["value"]
                elif obj["name"] == "To":
                    email_to = obj["value"]
                    recipient = email_to.split("<", 1)[0]
            email_str = recipient + ":\n" + subject
            ret.append(email_str)
        return ret

    def refreshInbox(self):
        try:
            # Call the Gmail API
            response = (
                self.service.users()
                .messages()
                .list(userId="me", labelIds=["INBOX"], maxResults=1)
                .execute()
            )

            if response["resultSizeEstimate"] == 0:
                return self.inbox_messages
            message = response["messages"]

            if message[0]["id"] == self.inbox_messages[0]["id"]:
                return self.inbox_messages
            else:
                self.inbox_messages.insert(0, message[0])
                return self.inbox_messages
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def refreshSent(self):
        try:
            # Call the Gmail API
            response = (
                self.service.users()
                .messages()
                .list(userId="me", labelIds=["SENT"], maxResults=1)
                .execute()
            )

            if response["resultSizeEstimate"] == 0:
                return self.sent_messages
            message = response["messages"]

            if message[0]["id"] == self.sent_messages[0]["id"]:
                return self.sent_messages
            else:
                self.sent_messages.insert(0, message[0])
                return self.sent_messages
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def refreshDrafts(self):
        try:
            # Call the Gmail API
            response = (
                self.service.users()
                .messages()
                .list(userId="me", labelIds=["DRAFT"], maxResults=1)
                .execute()
            )

            if response["resultSizeEstimate"] == 0:
                return self.draft_messages
            message = response["messages"]

            if message[0]["id"] == self.draft_messages[0]["id"]:
                return self.draft_messages
            else:
                self.draft_messages.insert(0, message[0])
                return self.draft_messages
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def refreshSpam(self):
        try:
            # Call the Gmail API
            response = (
                self.service.users()
                .messages()
                .list(userId="me", labelIds=["SPAM"], maxResults=1)
                .execute()
            )

            if response["resultSizeEstimate"] == 0:
                return self.spam_messages
            message = response["messages"]

            if message[0]["id"] == self.spam_messages[0]["id"]:
                return self.spam_messages
            else:
                self.spam_messages.insert(0, message[0])
                return self.spam_messages
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def refreshTrash(self):
        try:
            # Call the Gmail API
            response = (
                self.service.users()
                .messages()
                .list(userId="me", labelIds=["TRASH"], maxResults=1)
                .execute()
            )

            if response["resultSizeEstimate"] == 0:
                return self.trash_messages
            message = response["messages"]

            if message[0]["id"] == self.trash_messages[0]["id"]:
                return self.trash_messages
            else:
                self.trash_messages.insert(0, message[0])
                return self.trash_messages
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def getEmail(self, currInbox, index):
        if currInbox == "INBOX":
            return self.inbox_messages[index]
        elif currInbox == "SENT":
            return self.sent_messages[index]
        elif currInbox == "DRAFT":
            return self.draft_messages[index]
        elif currInbox == "SPAM":
            return self.spam_messages[index]
        else:
            return self.trash_messages[index]

    def evaluateMessageHeader(self, message):
        header = message["payload"]["headers"]
        subject = "(No Subject)"

        for obj in header:
            if obj["name"] == "Subject":
                subject = "Subject: " + obj["value"]
            elif obj["name"] == "From":
                sender = obj["value"]
                sender = "From: " + sender.split("<", 1)[0]
            elif obj["name"] == "To":
                recipient = obj["value"]

                if "<" in recipient:
                    recAddress = recipient.split("<", 1)
                    recipient = "To: " + recAddress[0]
                    recAddress = recAddress[1].split(">", 1)[0]
                else:
                    recipient = "To: " + recipient.split("<", 1)[0]
                    recAddress = recipient
        return sender, recipient, recAddress, subject

    def evaluateMessagePayload(self, payload, user_id, msg_id, attachments="reference"):
        if "attachmentId" in payload["body"]:
            if attachments == "ignore":
                return []
            attm_id = payload["body"]["attachmentId"]
            filename = payload["filename"]
            if not filename:
                filename = "unknown"
            obj = {
                "part_type": "attachment",
                "filetype": payload["mimeType"],
                "filename": filename,
                "attachment_id": attm_id,
                "data": None,
            }

            if attachments == "reference":
                return [obj]
            else:
                res = (
                    self.service.users()
                    .messages()
                    .attachments()
                    .get(userId=user_id, messageId=msg_id, id=attm_id)
                    .execute()
                )
                data = res["data"]
            file_data = base64.urlsafe_b64decode(data)
            obj["data"] = file_data
            return [obj]
        elif payload["mimeType"] == "text/html":
            data = payload["body"]["data"]
            data = base64.urlsafe_b64decode(data)
            body = BeautifulSoup(data, "lxml", from_encoding="utf-8").body
            return [{"part_type": "html", "body": str(body)}]
        elif payload["mimeType"] == "text/plain":
            data = payload["body"]["data"]
            data = base64.urlsafe_b64decode(data)
            body = data.decode("UTF-8")
            return [{"part_type": "plain", "body": body}]
        elif payload["mimeType"].startswith("multipart"):
            ret = []
            if "parts" in payload:
                for part in payload["parts"]:
                    ret.extend(
                        self.evaluateMessagePayload(part, user_id, msg_id, attachments)
                    )
            return ret
        return []

    def downloadAttachment(self, attachment, msg_id):
        res = (
            self.service.users()
            .messages()
            .attachments()
            .get(userId="me", messageId=msg_id, id=attachment["attachment_id"])
            .execute()
        )

        data = res["data"]
        retData = base64.urlsafe_b64decode(data)

        with open(attachment["filename"], "wb") as f:
            f.write(retData)

    def changeLabels(self, msg_id, toLabel, fromLabel):
        if toLabel == "INBOX":
            req = {"addLabelIds": [toLabel], "removeLabelIds": [fromLabel]}
            try:
                res = (
                    self.service.users()
                    .messages()
                    .modify(userId="me", id=msg_id, body=req)
                    .execute()
                )
            except HttpError as error:
                print(f"An error occurred: {error}")
        elif toLabel == "SPAM":
            req = {"addLabelIds": [toLabel], "removeLabelIds": [fromLabel]}
            try:
                res = (
                    self.service.users()
                    .messages()
                    .modify(userId="me", id=msg_id, body=req)
                    .execute()
                )
            except HttpError as error:
                print(f"An error occurred: {error}")
        elif toLabel == "TRASH":
            req = {"addLabelIds": [toLabel], "removeLabelIds": [fromLabel]}
            try:
                res = (
                    self.service.users()
                    .messages()
                    .modify(userId="me", id=msg_id, body=req)
                    .execute()
                )
            except HttpError as error:
                print(f"An error occurred: {error}")

    def createDraft(
        self,
        sender,
        to,
        subject="",
        msg_html=None,
        msg_plain=None,
        cc=None,
        bcc=None,
        attachments=None,
    ):
        draft = self.createEmail(
            sender,
            to,
            subject,
            msg_html,
            msg_plain,
            cc=cc,
            bcc=bcc,
            attachments=attachments,
            draft=True,
        )

        try:
            # Call the Gmail API
            self.service.users().drafts().create(userId="me", body=draft).execute()
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def sendDraft(self, draft_id):
        try:
            # Call the Gmail API
            self.service.users().drafts().send(
                userId="me", body={"id": draft_id}
            ).execute()
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def getDraftID(self, index):
        try:
            # Call the Gmail API
            response = (
                self.service.users().drafts().list(userId="me", maxResults=25).execute()
            )
            messages = response["drafts"]
            drafts = []

            for obj in messages:
                drafts.append(obj["id"])
            return drafts[index]
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")

    def updateDraft(
        self,
        sender,
        to,
        draft_id,
        subject="",
        msg_html=None,
        msg_plain=None,
        cc=None,
        bcc=None,
        attachments=None,
    ):
        draft = self.createEmail(
            sender,
            to,
            subject,
            msg_html,
            msg_plain,
            cc=cc,
            bcc=bcc,
            attachments=attachments,
            draft=True,
        )

        try:
            # Call the Gmail API
            self.service.users().drafts().update(
                userId="me", id=draft_id, body=draft
            ).execute()
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")
