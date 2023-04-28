import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QStackedWidget,
 )


class LoginWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        # Create UI components
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.email_button = QPushButton("Inbox")
        self.switch_button = QPushButton("Switch to Signup")

        # Set up layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.email_button)
        self.layout.addWidget(self.switch_button)

        self.setLayout(self.layout)

        # Connect login and switch button to handlers
        self.login_button.clicked.connect(self.login)
        self.switch_button.clicked.connect(self.switch_to_signup)
        self.email_button.clicked.connect(self.switch_to_inbox)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        # Add logic to perform login here
        print("Login with Email:", email)
        print("Password:", password)

    def switch_to_signup(self):
        self.stacked_widget.setCurrentIndex(1)

    def switch_to_inbox(self):
        self.stacked_widget.setCurrentIndex(2)
        
        
        
class SignupWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        # Create UI components
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.signup_button = QPushButton("Signup")
        self.switch_button = QPushButton("Switch to Login")

        # Set up layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.signup_button)
        self.layout.addWidget(self.switch_button)

        self.setLayout(self.layout)

        # Connect signup and switch button to handlers
        self.signup_button.clicked.connect(self.signup)
        self.switch_button.clicked.connect(self.switch_to_login)

    def signup(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        # Add logic to perform signup here
        print("Signup with Name:", name)
        print("Email:", email)
        print("Password:", password)

    def switch_to_login(self):
        self.stacked_widget.setCurrentIndex(0)
        
        
        
class EmailWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        # Create UI components
        self.recipient_label = QLabel("Recipient:")
        self.recipient_input = QLineEdit()
        self.subject_label = QLabel("Subject:")
        self.subject_input = QLineEdit()
        self.message_label = QLabel("Message:")
        self.message_input = QTextEdit()
        self.send_button = QPushButton("Send")
        self.switch_button = QPushButton("Switch to Login")

        # Set up layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.recipient_label)
        self.layout.addWidget(self.recipient_input)
        self.layout.addWidget(self.subject_label)
        self.layout.addWidget(self.subject_input)
        self.layout.addWidget(self.message_label)
        self.layout.addWidget(self.message_input)
        self.layout.addWidget(self.send_button)
        self.layout.addWidget(self.switch_button)

        self.setLayout(self.layout)

        self.switch_button.clicked.connect(self.switch_to_login)

    def switch_to_login(self):
        self.stacked_widget.setCurrentIndex(0)
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create a stacked widget to manage multiple windows
    stacked_widget = QStackedWidget()

    # Create login and signup windows
    login_window = LoginWindow(stacked_widget)
    signup_window = SignupWindow(stacked_widget)
    inbox_window = EmailWindow(stacked_widget)

    # Add login and signup windows to stacked widget
    stacked_widget.addWidget(login_window)
    stacked_widget.addWidget(signup_window)
    stacked_widget.addWidget(inbox_window)

    # Show initial window
    stacked_widget.setCurrentIndex(0)

    stacked_widget.show()
    sys.exit(app.exec_())
