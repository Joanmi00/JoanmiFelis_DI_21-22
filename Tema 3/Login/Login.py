import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFormLayout, \
    QLineEdit


class LoginW(QWidget):
    def __init__(self):
        super().__init__()
        self.mainW = None
        self.setWindowTitle("Login")

        layoutBox = QVBoxLayout()
        layoutForm = QFormLayout()

        self.usuari = QLineEdit()
        self.contrasenya = QLineEdit()
        self.contrasenya.setEchoMode(QtWidgets.QLineEdit.Password)

        layoutForm.addRow("Usuari:", self.usuari)
        layoutForm.addRow("Contraseña:", self.contrasenya)

        boto = QPushButton("Login")
        boto.clicked.connect(self.login)
        boto.setShortcut(QKeySequence('Return'))

        self.warningLabel = QLabel()
        layoutBox.addLayout(layoutForm)
        layoutBox.addWidget(boto)

        layoutBox.addWidget(self.warningLabel)
        self.setLayout(layoutBox)

    def login(self):
        self.warningLabel.setText("")

        if self.usuari.text() == "user" and self.contrasenya.text() == "1234":
            self.mainW = MainWindow("user")
            self.mainW.show()
            self.close()

        elif self.usuari.text() == "admin" and self.contrasenya.text() == "1234":
            self.mainW = MainWindow("admin")
            self.mainW.show()
            self.close()

        elif self.usuari.text() == "user" or self.usuari.text() == "admin" and self.contrasenya.text() != "1234":
            self.warningLabel.setText("Contrasenya incorrecta")

        elif self.usuari.text() != "user" or self.usuari.text() != "admin":
            self.warningLabel.setText("Usuari incorrecte")


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.login = None

        label = QLabel(f"Estas loguejat amb l'usuari {user}")
        self.deslog = QAction("&Logout")
        self.eixir = QAction("&Salir")
        self.deslog.triggered.connect(self.logout)
        self.eixir.triggered.connect(self.close)

        menu = self.menuBar()
        menuEixir = menu.addMenu("&Menu")
        menuEixir.addAction(self.deslog)
        menuEixir.addAction(self.eixir)
        self.setCentralWidget(label)

        status = self.statusBar()
        status.addWidget(QLabel(f"Usuari: {user}"))

    def logout(self):
        self.login = LoginW()
        self.login.show()
        self.close()


app = QApplication(sys.argv)
w = LoginW()
w.show()
app.exec()
