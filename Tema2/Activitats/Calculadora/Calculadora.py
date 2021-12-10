import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QGridLayout, QPushButton
from PySide6.QtGui import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora")

        self.widget = QWidget(self)
        self.layout = QVBoxLayout(self.widget)

        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.layout)

        self.lineEdit = QLineEdit()
        self.lineEdit.setAlignment(Qt.AlignRight)
        self.lineEdit.setFixedHeight(30)
        self.lineEdit.setReadOnly(True)
        self.layout.addWidget(self.lineEdit)

        self.botons = {}
        botons = {'AC': (0, 0), '<-': (0, 1), '%': (0, 2), '/': (0, 3),
                  '7': (1, 0), '8': (1, 1), '9': (1, 2), '*': (1, 3),
                  '4': (2, 0), '5': (2, 1), '6': (2, 2), '+': (2, 3),
                  '1': (3, 0), '2': (3, 1), '3': (3, 2), '-': (3, 3),
                  '0': (4, 0), '.': (4, 1), '=': (4, 3)}

        BLayout = QGridLayout()
        for i, p in botons.items():
            self.botons[i] = QPushButton(i)
            self.botons[i].setFixedSize(50, 50)

            BLayout.addWidget(self.botons[i], p[0], p[1])
            self.botons[i].clicked.connect(self.calc)

        self.tecles = ""
        self.layout.addLayout(BLayout)
        
        self.botons['='].clicked.connect(self.resultat)

    def calc(self):
        if self.sender().text() == "=":
            pass

        elif self.sender().text() == "AC":
            self.tecles = ""

        elif self.sender().text() == "<-":
            self.tecles = self.tecles[:-1]

        else:
            self.tecles += self.sender().text()

        self.lineEdit.setText(self.tecles)

    def resultat(self):
        self.lineEdit.setText(str(eval(self.tecles)))


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
