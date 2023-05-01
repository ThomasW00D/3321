import json
from typing import Optional

import gmail
from gmail import GMailClass

build: Optional[GMailClass] = gmail.GMailClass(True)

with open("3321/mock-email-list.json") as data_file:
    emailList = []
    emailList = json.load(data_file)

with open("3321/mock-email.json") as data_file:
    email1 = json.load(data_file)


def testSendEmail(mocker):
    mocked_email = mocker.patch.object(build, "createEmail")
    mocked_email.return_value = True
    mocked_send = mocker.patch.object(
        build.service.users().messages().send(userId="me", body=""), "execute"
    )
    mocked_send.return_value = True

    build.sendEmail(sender="", to="")

    mocked_email.assert_called
    mocked_send.asssert_called


def testFillMessageLists(mocker):
    mocked_message_list = mocker.patch.object(build, "getEmails")
    mocked_message_list.return_value = ["1", "2", "3", "4"]
    mocked_message_list2 = mocker.patch.object(build, "refreshEmails")
    mocked_message_list2.return_value = ["4", "3", "2", "1"]

    assert build.fillMessageLists("INBOX") == ["4", "3", "2", "1"]
    assert build.fillMessageLists("INBOX", True) == ["1", "2", "3", "4"]


def testGetEmail(mocker):
    mocked_message_list = mocker.patch.object(build, "inbox_messages")
    mocked_message_list.return_value = ["4", "3", "2", "1"]

    assert build.getEmail("INBOX", 0) == mocked_message_list[0]
    assert build.getEmail("INBOX", 2) == mocked_message_list[2]


def testGetEmails():
    mockEmailList = build.getEmails()
    mockEmail1 = mockEmailList[0]["messages"][0]["id"]

    assert mockEmailList[0]["messages"] == emailList["messages"]
    assert mockEmail1 == email1["id"]


def testEvaluateMessageHeader():
    sender, recipient, recAddress, subject = build.evaluateMessageHeader(email1)

    assert sender == "From: fakeaddress@gmail.com"
    assert recipient == "To: fakeaddress@gmail.com"
    assert recAddress == "To: fakeaddress@gmail.com"
    assert subject == "Subject: Please work"
