import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QGridLayout, QPushButton, \
    QStackedLayout
from PySide6.QtGui import Qt, QAction


def Eixir():
    app.closeAllWindows()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora")

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.stack = QStackedLayout(self.widget)

        self.normal = QWidget()
        self.layoutN = QVBoxLayout(self.normal)
        self.normal.setLayout(self.layoutN)

        self.cientifi = QWidget()
        self.layoutC = QVBoxLayout(self.cientifi)
        self.cientifi.setLayout(self.layoutC)

        self.stack.addWidget(self.normal)
        self.stack.addWidget(self.cientifi)

        opcioN = QAction("Normal", self)
        opcioN.triggered.connect(self.LaNormal)

        opcioC = QAction("Cientifica", self)
        opcioC.triggered.connect(self.LaCientifica)

        self.guardar = QAction("&Guardar Operaciones", self)
        self.guardar.setCheckable(True)
        self.guardar.triggered.connect(self.Guardar)

        eixir = QAction("Eixir", self)
        eixir.triggered.connect(Eixir)

        menu = self.menuBar().addMenu("&Menu")
        sub = menu.addMenu("Modo")
        sub.addAction(opcioN)
        sub.addAction(opcioC)
        menu.addAction(self.guardar)
        menu.addAction(eixir)

        self.tecles = ""
        self.solucio = ""

        self.lineEditN = QLineEdit()
        self.lineEditN.setAlignment(Qt.AlignRight)
        self.lineEditN.setReadOnly(True)
        self.layoutN.addWidget(self.lineEditN)

        self.botonsN = {}
        BLayoutN = QGridLayout()

        botonsN = {'AC': (0, 0), '<-': (0, 1), '%': (0, 2), '/': (0, 3),
                   '7': (1, 0), '8': (1, 1), '9': (1, 2), '*': (1, 3),
                   '4': (2, 0), '5': (2, 1), '6': (2, 2), '+': (2, 3),
                   '1': (3, 0), '2': (3, 1), '3': (3, 2), '-': (3, 3),
                   '0': (4, 0), '.': (4, 1), '=': (4, 3)}

        for i, p in botonsN.items():
            self.botonsN[i] = QPushButton(i)
            self.botonsN[i].setFixedSize(50, 50)
            self.botonsN[i].setShortcut(i)

            BLayoutN.addWidget(self.botonsN[i], p[0], p[1])
            self.botonsN[i].clicked.connect(self.calc)

        self.layoutN.addLayout(BLayoutN)

        # Botons de la calculadora Cientifica
        self.lineEditC = QLineEdit()
        self.lineEditC.setAlignment(Qt.AlignRight)
        self.lineEditC.setReadOnly(True)
        self.layoutN.addWidget(self.lineEditC)

        self.botonsC = {}
        BLayoutC = QGridLayout()

        botonsC = {'AC': (0, 0), '<-': (0, 1), '%': (0, 2), '/': (0, 3), 'exp': (0, 4),
                   '7': (1, 0), '8': (1, 1), '9': (1, 2), '*': (1, 3), 'mod': (1, 4),
                   '4': (2, 0), '5': (2, 1), '6': (2, 2), '+': (2, 3), '(': (2, 4),
                   '1': (3, 0), '2': (3, 1), '3': (3, 2), '-': (3, 3), ')': (3, 4),
                   '00': (4, 0), '0': (4, 1), '.': (4, 2), '^': (4, 3), '=': (4, 4)}

        for i, p in botonsC.items():
            self.botonsC[i] = QPushButton(i)
            self.botonsC[i].setFixedSize(50, 50)
            self.botonsC[i].setShortcut(i)

            BLayoutC.addWidget(self.botonsC[i], p[0], p[1])
            self.botonsC[i].clicked.connect(self.calc)

        self.layoutN.addLayout(BLayoutC)

    def calc(self):
        if self.sender().text() == "=":
            self.solucio = self.tecles + " = " + str((eval(self.tecles)))

        elif self.sender().text() == "AC":
            self.tecles = ""

        elif self.sender().text() == "<-":
            self.tecles = self.tecles[:-1]

        else:
            self.tecles += self.sender().text()

    def LaNormal(self):
        self.stack.setCurrentWidget(self.normal)

    def LaCientifica(self):
        self.stack.setCurrentWidget(self.cientifi)

    def Guardar(self):
        if self.guardar.isChecked():
            try:
                with open("Resultats.txt", 'a+') as file:
                    file.write(self.solucio + "\n")
                    file.close()
            except FileNotFoundError as ex:
                return ex
            except IOError as ex:
                return ex


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
