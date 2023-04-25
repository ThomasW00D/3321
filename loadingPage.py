import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
# Import host_GUI UI note, must have host_GUI in folder
from host_GUI import Ui_Form
# Import Client_GUI UI note, must have Client_GUI in folder
from Client_GUI import Ui_Client
# Import gmailgui UI note, must have gmailgui in folder
from gmailgui import MainGUI
from PyQt5 import QtWidgets

class LoadingPage(QWidget):
    def __init__(self):
        super(LoadingPage, self).__init__()
        self.init_ui()

    # Method to open Host GUI UI
    def openHost(self):
        self.window =QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        self.window.show()

    # Method to open Client GUI UI
    def openClient(self):
        self.window =QtWidgets.QWidget()
        self.ui = Ui_Client()
        self.ui.setupUi(self.window)
        self.window.show()

    # Method to open Gmail GUI UI
    def openGmail(self):
        self.window =QWidget()
        self.ui = MainGUI()
        self.ui.initUI(self.window)
        self.window.show()

    # Method to open Welcome GUI UI
    def openWelcome(self):
        #welcomePage = SplashScreen()
        #self.window = welcomePage
        self.window.show()

    def init_ui(self):
        self.setWindowTitle('Loading Page')
        self.setGeometry(300, 300, 400, 150)

        # Create widgets
        label = QLabel('                                Welcome to the Home Loading Page!', self)
        #label.setAlignment.(AlignCenter)
        button1 = QPushButton('E-Mail', self)
        button2 = QPushButton('Host Server', self)
        button3 = QPushButton('Join Server', self)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        self.setLayout(layout)

        # Connect button signals to slots
        button1.clicked.connect(self.option1_clicked)
        button2.clicked.connect(self.option2_clicked)
        button3.clicked.connect(self.option3_clicked)

    # Slot functions for button clicks
    def option1_clicked(self):
        self.openGmail()

    # If host is clicked openHost
    def option2_clicked(self):
        self.openHost()

    # If join is clicked openClient
    def option3_clicked(self):
        self.openClient()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoadingPage()
    window.show()
    sys.exit(app.exec_())
