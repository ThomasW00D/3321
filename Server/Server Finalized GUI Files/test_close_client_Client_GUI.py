import unittest
from unittest.mock import MagicMock, patch

from Client_GUI import Ui_Client
from PyQt5 import QtWidgets


class TestUiClient(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication([])
        self.form = QtWidgets.QMainWindow()
        self.ui = Ui_Client()
        self.ui.setupUi(self.form)

    @patch("socket.socket.connect")
    def test_close_client(self, mock_socket):
        mock_client_socket = MagicMock()
        mock_socket.return_value = mock_client_socket

        self.ui.client_socket = mock_socket.return_value
        self.ui.close_client()

        self.assertFalse(self.ui.logTxt.isEnabled())
        self.assertFalse(self.ui.msgTxt.isEnabled())
        self.assertFalse(self.ui.closeBtn.isEnabled())
        self.assertFalse(self.ui.sendBtn.isEnabled())

        self.assertTrue(self.ui.connectBtn.isEnabled())
        self.assertTrue(self.ui.hostTxt.isEnabled())
        self.assertTrue(self.ui.portTxt.isEnabled())


if __name__ == "__main__":
    unittest.main()
