import unittest
from PyQt5.QtWidgets import QApplication, QWidget
from switchV2 import LoadingPage


class TestLoadingPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a QApplication instance before running tests
        cls.app = QApplication([])

    @classmethod
    def tearDownClass(cls):
        # Clean up after running tests
        cls.app.quit()

    def setUp(self):
        # Create an instance of the LoadingPage class
        self.loading_page = LoadingPage()

    def tearDown(self):
        # Clean up after each test
        self.loading_page.close()

    def test_widget_existence(self):
        # Test that the LoadingPage widget is created
        self.assertIsNotNone(self.loading_page)

    def test_widget_title(self):
        # Test that the LoadingPage widget has the correct title
        self.assertEqual(self.loading_page.windowTitle(), "Loading Page")

    def test_button_click(self):
        # Test that clicking the "E-Mail" button opens the Gmail GUI
        # self.loading_page.option1_clicked()
        # self.assertIsInstance(self.loading_page.window, QWidget)

        # Test that clicking the "Host Server" button opens the Host GUI
        self.loading_page.option2_clicked()
        self.assertIsInstance(self.loading_page.window, QWidget)

        # Test that clicking the "Join Server" button opens the Client GUI
        self.loading_page.option3_clicked()
        self.assertIsInstance(self.loading_page.window, QWidget)


if __name__ == "__main__":
    unittest.main()
