import sys

from Client_GUI import Ui_Client
from host_GUI import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


# LoadingPage UI class
class LoadingPage(QWidget):
    def __init__(self):
        super(LoadingPage, self).__init__()
        self.init_ui()

    # Method to open Host GUI UI
    def openHost(self):
        self.window = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        self.window.show()

    # Method to open Client GUI UI
    def openClient(self):
        self.window = QtWidgets.QWidget()
        self.ui = Ui_Client()
        self.ui.setupUi(self.window)
        self.window.show()

    # Method to open Gmail GUI UI
    def openGmail(self):
        self.window = QWidget()
        # self.ui = MainGUI()
        self.ui.initUI(self.window)
        self.window.show()

    # Method to open Welcome GUI UI
    # def openWelcome(self):

    # Define the loading page
    def init_ui(self):
        self.setWindowTitle("Loading Page")
        self.setGeometry(300, 300, 400, 150)
        self.center()

        # Create widgets
        label = QLabel("Welcome to the Home Loading Page!", self)

        button1 = QPushButton("E-Mail", self)
        button2 = QPushButton("Host Server", self)
        button3 = QPushButton("Join Server", self)

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

    # If user selects Gmail box, call openGmail
    def option1_clicked(self):
        self.openGmail()

    # If user selects Host box, call openWelcome first to
    # show loading screen then call openHost
    def option2_clicked(self):
        self.openHost()

    # If user selects Join Server box, call openWelcome first
    # to show loading screen then call openClient
    def option3_clicked(self):
        self.openClient()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(
        """
        #LabelTitle {
            font-size: 60px;
            color: #93deed;
        }
        #LabelDesc {
            font-size: 30px;
            color: #c2ced1;
        }
        #LabelLoading {
            font-size: 30px;
            color: #e8e8eb;
        }
        QFrame {
            background-color: #2F4454;
            color: rgb(220, 220, 220);
        }
        QProgressBar {
            background-color: #DA7B93;
            color: rgb(200, 200, 200);
            border-style: none;
            border-radius: 10px;
            text-align: center;
            font-size: 30px;
        }
        QProgressBar::chunk {
            border-radius: 10px;
            background-color: qlineargradient(spread:pad x1:0, x2:1,
             y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
        }
    """
    )

    app.setStyleSheet("")
    window = LoadingPage()
    window.show()
    sys.exit(app.exec_())
