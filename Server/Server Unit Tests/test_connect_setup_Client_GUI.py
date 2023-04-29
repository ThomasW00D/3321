import unittest
from unittest.mock import patch

from Client_GUI import Ui_Client
from PyQt5 import QtWidgets


class TestConnectSetup(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication([])
        self.form = QtWidgets.QMainWindow()
        self.ui = Ui_Client()
        self.ui.setupUi(self.form)

    def test_connect_setup_correct_input(self):
        self.ui.hostTxt.setText("192.168.1.8")
        self.ui.portTxt.setText("12345")
        with patch("socket.socket") as mock_socket:
            mock_socket.return_value.connect = lambda x: None
            self.ui.connect_setup()
            self.assertFalse(self.ui.connectBtn.isEnabled())
            self.assertFalse(self.ui.hostTxt.isEnabled())
            self.assertFalse(self.ui.portTxt.isEnabled())
            self.assertTrue(self.ui.nicknameTxt.isEnabled())
            self.assertTrue(self.ui.nicknameBtn.isEnabled())
            self.assertIn("Socket succeeded.\n", self.ui.logTxt.toPlainText())

    def test_connect_setup_incorrect_host_ip(self):
        self.ui.hostTxt.setText("INVALID")
        self.ui.portTxt.setText("12345")
        self.ui.connect_setup()
        self.assertIn(
            "Host IP number or port number is incorrect. Please recheck your information and try again.\n"
            "If problem persists, you can try creating a server and inviting friends!\n",
            self.ui.logTxt.toPlainText(),
        )

    def test_connect_setup_incorrect_port(self):
        self.ui.hostTxt.setText("192.168.1.8")
        self.ui.portTxt.setText("99999")
        with patch("socket.socket") as mock_socket:
            self.ui.connect_setup()
            self.assertIn(
                "Host IP or port is incorrect. Port must be between 10000 and 65535.\n",
                self.ui.logTxt.toPlainText(),
            )
            mock_socket.assert_not_called()


if __name__ == "__main__":
    unittest.main()
