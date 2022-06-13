import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        uic.loadUi("E:\-\\2022-1\파이썬\CALENDAR\custom\welcome.ui", self)
        self.login.clicked.connect(self.gotologin)
        self.new_account.clicked.connect(self.gotocreate)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 2)

    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        uic.loadUi("E:\-\\2022-1\파이썬\CALENDAR\custom\\reactive_login.ui", self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.returnPressed.connect(self.loginfunction)
        self.id.returnPressed.connect(self.loginfunction)
        self.loginbox.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user = self.id.text()
        pw = self.password.text()

        if len(user) == 0 or len(pw) == 0:
            self.error.setText("값을 입력해주세요.")

        else:
            conn = sqlite3.connect("E:\-\\2022-1\파이썬\CALENDAR\\test_DB.db")
            cur = conn.cursor()
            query = 'SELECT password FROM test WHERE id =\'' + user + "\'"
            try:
                cur.execute(query)
                result_pass = cur.fetchone()[0]
                if result_pass == pw:
                    print("Successfully logged in.")
                    self.error.setText("")
                    QApplication.instance().quit()

                else:
                    self.error.setText("비밀번호 또는 아이디를 확인해주세요.")

            except:
                self.error.setText("비밀번호 또는 아이디를 확인해주세요.")


class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        uic.loadUi("E:\-\\2022-1\파이썬\CALENDAR\custom\\reactive_sign_up.ui", self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Signup.clicked.connect(self.signupfunction)
        self.id.returnPressed.connect(self.signupfunction)
        self.password.returnPressed.connect(self.signupfunction)
        self.password_2.returnPressed.connect(self.signupfunction)

    def signupfunction(self):
        user = self.id.text()
        password = self.password.text()
        password_2 = self.password_2.text()

        if len(user) == 0 or len(password) == 0 or len(password_2) == 0:
            self.error.setText("값을 입력해주세요.")

        elif password != password_2:
            self.error.setText("비밀번호를 확인해주세요.")

        else:
            conn = sqlite3.connect('E:\-\\2022-1\파이썬\CALENDAR\\test_DB.db')
            cur = conn.cursor()

            user_info = [user, password]
            cur.execute('INSERT INTO test (id, password) VALUES (?, ?)', user_info)

            conn.commit()
            conn.close()

            self.error.setText("")
            widget.setCurrentIndex(widget.currentIndex() - 1)

    def setUserinfo(self, num, password):
        self.loginfo = [num, password]

    def getUserinfo(self):
        return self.loginfo


app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.show()

try:
    sys.exit(app.exec())

except:
    print("Exiting")