import json

import gmail
from gmail import GMailClass
from typing import Optional

gmail: Optional[GMailClass] = gmail.GMailClass(True)

with open("3321/mock-email-list.json") as data_file:
    emailList = []
    emailList = json.load(data_file)

with open("3321/mock-email.json") as data_file:
    email1 = json.load(data_file)


def testSendEmail(mocker):
    mocked_email = mocker.patch.object(gmail, "createEmail")
    mocked_email.return_value = True
    mocked_send = mocker.patch.object(
        gmail.service.users().messages().send(userId="me", body=""), "execute"
    )
    mocked_send.return_value = True

    gmail.sendEmail(sender="", to="")

    mocked_email.assert_called
    mocked_send.asssert_called


def testFillMessageLists(mocker):
    mocked_message_list = mocker.patch.object(gmail, "getEmails")
    mocked_message_list.return_value = ["1", "2", "3", "4"]
    mocked_message_list2 = mocker.patch.object(gmail, "refreshEmails")
    mocked_message_list2.return_value = ["4", "3", "2", "1"]

    assert gmail.fillMessageLists("INBOX") == ["4", "3", "2", "1"]
    assert gmail.fillMessageLists("INBOX", True) == ["1", "2", "3", "4"]


def testGetEmail(mocker):
    mocked_message_list = mocker.patch.object(gmail, "inbox_messages")
    mocked_message_list.return_value = ["4", "3", "2", "1"]

    assert gmail.getEmail("INBOX", 0) == mocked_message_list[0]
    assert gmail.getEmail("INBOX", 2) == mocked_message_list[2]


def testGetEmails():
    mockEmailList = gmail.getEmails()
    mockEmail1 = mockEmailList[0]["messages"][0]["id"]

    assert mockEmailList[0]["messages"] == emailList["messages"]
    assert mockEmail1 == email1["id"]


def testEvaluateMessageHeader():
    sender, recipient, recAddress, subject = gmail.evaluateMessageHeader(email1)

    assert sender == "From: fakeaddress@gmail.com"
    assert recipient == "To: fakeaddress@gmail.com"
    assert recAddress == "To: fakeaddress@gmail.com"
    assert subject == "Subject: Please work"
