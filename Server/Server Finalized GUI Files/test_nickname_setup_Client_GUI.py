import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication, QMainWindow
from Client_GUI import Ui_Client


class TestUiClient(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.form = QMainWindow()
        self.ui = Ui_Client()
        self.ui.setupUi(self.form)

    def test_nickname_setup_successful(self):
        # Set up the input fields
        self.ui.nicknameTxt.setText("TestUser")

        self.ui.nickname = self.ui.nicknameTxt.text()

        with patch.object(
            Ui_Client, "start_thread", return_value=None
        ):  # Mock start_thread method
            # Simulate a successful nickname setup
            self.ui.nickname_setup()

        # Check that the UI elements are in the correct state
        self.assertFalse(self.ui.nicknameTxt.isEnabled())
        self.assertFalse(self.ui.nicknameBtn.isEnabled())
        self.assertTrue(self.ui.msgTxt.isEnabled())
        self.assertTrue(self.ui.sendBtn.isEnabled())
        self.assertTrue(self.ui.closeBtn.isEnabled())
        self.assertIn(
            f"Nickname set to {self.ui.nickname}.\n",
            self.ui.logTxt.toPlainText()
        )
        self.assertIn("Client starting.\n", self.ui.logTxt.toPlainText())

    def test_nickname_setup_unsuccessful(self):
        # Set up the input fields
        self.ui.nicknameTxt.setText("")
        self.ui.nickname = self.ui.nicknameTxt.text()

        # Simulate an unsuccessful nickname setup
        self.ui.nickname_setup()
        self.assertIn(
            "Incorrect nickname. Nickname can't be white space.\n",
            self.ui.msgTxt.toPlainText(),
        )


if __name__ == "__main__":
    unittest.main()
