import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QProgressBar,
    QLabel,
    QFrame,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt, QTimer

# from host_GUI import Ui_Form
from switchV2 import LoadingPage

# Note still needs to be linked to loadingPage


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("loading")
        self.setFixedSize(1100, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 250
        self.cond = 0

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName("LabelTitle")

        # center labels
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.move(0, 40)  # x, y
        self.labelTitle.setText("Now Loading CS3321 Email Project")
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName("LabelDesc")
        self.labelDescription.setText("<strong>Working on Task #1</strong>")
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat("%p%")
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName("LabelLoading")
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText("loading...")

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText("<strong>Working on Task #2</strong>")
        elif self.counter == int(self.n * 0.6):
            self.labelDescription.setText("<strong>Working on Task #3</strong>")
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()
            time.sleep(1)
            self.cond = 1

        self.counter += 1

    def openSwitch(self):
        self.window = QtWidgets.QWidget()
        self.ui = LoadingPage()
        self.ui.init_ui()
        self.window.show()


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
            background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
        }
    """
    )

    splash = SplashScreen()
    splash.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        splash = SplashScreen()
        app.setStyleSheet("")
        splash.openSwitch()
        sys.exit(app.exec_())
        print("Closing Window...")
