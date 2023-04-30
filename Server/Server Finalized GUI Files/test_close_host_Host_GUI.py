import unittest
from unittest.mock import MagicMock, patch
from PyQt5 import QtWidgets
from Host_GUI import Ui_Host


class TestUiClient(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication([])
        self.form = QtWidgets.QMainWindow()
        self.ui = Ui_Host()
        self.ui.setupUi(self.form)

    @patch("socket.socket.connect")
    def test_close_host(self, mock_socket):
        mock_client_socket = MagicMock()
        mock_socket.return_value = mock_client_socket

        self.ui.client_socket = mock_socket.return_value
        self.ui.close_host()

        self.assertFalse(self.ui.logTxt.isEnabled())
        self.assertFalse(self.ui.msgTxt.isEnabled())
        self.assertFalse(self.ui.closeBtn.isEnabled())
        self.assertFalse(self.ui.sendBtn.isEnabled())
        self.assertFalse(self.ui.nicknameBtn.isEnabled())
        self.assertFalse(self.ui.nicknameTxt.isEnabled())
        self.assertFalse(self.ui.serverTxt.isEnabled())

        self.assertTrue(self.ui.createBtn.isEnabled())


if __name__ == "__main__":
    unittest.main()
