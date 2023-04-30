import unittest
from Host_GUI import Ui_Host
from PyQt5 import QtWidgets
from unittest.mock import patch


class TestHost(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication([])
        self.form = QtWidgets.QMainWindow()
        self.ui = Ui_Host()
        self.ui.setupUi(self.form)

    def test_client_setup_successful(self):
        self.ui.nicknameTxt.setText("TestUser")

        self.ui.nickname = self.ui.nicknameTxt.text()

        with patch.object(Ui_Host, "start_client", return_value=None):
            self.ui.client_setup()

        self.assertFalse(self.ui.nicknameTxt.isEnabled())
        self.assertFalse(self.ui.nicknameBtn.isEnabled())
        self.assertTrue(self.ui.msgTxt.isEnabled())
        self.assertTrue(self.ui.logTxt.isEnabled())
        self.assertTrue(self.ui.sendBtn.isEnabled())
        self.assertIn(
            f"Nickname set to {Ui_Host.nickname}.\n",
            self.ui.logTxt.toPlainText()
        )
        self.assertIn("Client starting.\n", self.ui.logTxt.toPlainText())

    def test_client_setup_unsuccessful(self):
        self.ui.nicknameTxt.setText("   ")
        self.ui.nickname = self.ui.nicknameTxt.text()
        self.ui.client_setup()
        self.assertIn(
            "Incorrect nickname. Nickname can't be white space.\n",
            self.ui.msgTxt.toPlainText(),
        )


if __name__ == "__main__":
    unittest.main()
