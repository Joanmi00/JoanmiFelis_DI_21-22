import math
import os.path
import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QGridLayout, QPushButton, QStackedLayout, QMessageBox,
    QDialog, QDialogButtonBox, QLabel)
from PySide6.QtGui import Qt, QAction, QKeySequence


# Finestra principal
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Asignem el nom de la calculadora, com comença en la normal li posem Calculadora Normal
        self.setWindowTitle("Calculadora Normal")

        # Creem el widget principal
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        # Creem el Layout principal per a almacenar les dos calculadores
        self.stack = QStackedLayout(self.widget)

        # Widget i layout de la calculadora Normal
        self.normal = QWidget()
        self.layoutN = QVBoxLayout(self.normal)
        self.normal.setLayout(self.layoutN)

        # Widget i layout de la calculadora cientifica
        self.cientifi = QWidget()
        self.layoutC = QVBoxLayout(self.cientifi)
        self.cientifi.setLayout(self.layoutC)

        # Agreguem els widgets al layout principal
        self.stack.addWidget(self.normal)
        self.stack.addWidget(self.cientifi)

        """
            Comencem a crear el menu per a cambiar de calculadora, guardar o eixir
        """
        # Creem el boto de la calculadora normal, com comencem en la normal el desactivem
        self.opcioN = QAction("Normal", self)
        self.opcioN.triggered.connect(self.LaNormal)
        self.opcioN.setDisabled(True)

        # Creem el boto de la calculador cientifica, aquest si estara activat
        self.opcioC = QAction("Cientifica", self)
        self.opcioC.triggered.connect(self.LaCientifica)

        # Creem el check per a guardar els resultats
        self.guardar = QAction("&Guardar Operaciones", self)
        self.guardar.setCheckable(True)
        self.guardar.triggered.connect(self.Guardar)

        # I per ultim el boto de eixir de la aplicació
        eixir = QAction("Eixir", self)
        eixir.triggered.connect(self.Eixir)

        # S'agreguen els botons al menu i els de les calculadores en un submenu anomenat "Mode"
        menu = self.menuBar().addMenu("&Menu")
        sub = menu.addMenu("Mode")
        sub.addAction(self.opcioN)
        sub.addAction(self.opcioC)
        menu.addAction(self.guardar)
        menu.addAction(eixir)

        """
            Part visible de la calculadora Normal
        """
        # Creem i afegim al layout el lineEdit per a mostrar el que escrivim, no es podrá seleccionar el text
        self.lineEditN = QLineEdit()
        self.lineEditN.setAlignment(Qt.AlignRight)
        self.lineEditN.setReadOnly(True)
        self.layoutN.addWidget(self.lineEditN)

        # Creem el layout per als botons
        self.botonsN = {}
        BLayoutN = QGridLayout()

        # Crearem la llista amb els botons amb la seva posició
        botonsN = {'AC': (0, 0), '(': (0, 1), ')': (0, 2), '/': (0, 3),
                   '7': (1, 0), '8': (1, 1), '9': (1, 2), '*': (1, 3),
                   '4': (2, 0), '5': (2, 1), '6': (2, 2), '+': (2, 3),
                   '1': (3, 0), '2': (3, 1), '3': (3, 2), '-': (3, 3),
                   '0': (4, 0), '.': (4, 1), '<-': (4, 2), '=': (4, 3)}

        # Bucle per a afegir el text als botons i seleccionar el tamany "50, 50"
        for i, p in botonsN.items():
            self.botonsN[i] = QPushButton(i)
            self.botonsN[i].setFixedSize(50, 50)

            # Per a poder escriure per teclat utilitzem els if, tambe li agregue colors per a que siga mes visible
            if i == '=':
                self.botonsN[i].setShortcut(QKeySequence('Return'))
                self.botonsN[i].setStyleSheet('QPushButton {background-color: #e951ea }')
            elif i == '<-':
                self.botonsN[i].setShortcut(QKeySequence('Backspace'))
                self.botonsN[i].setStyleSheet('QPushButton {background-color: #e2ec57}')
            elif i == 'AC':
                self.botonsN[i].setShortcut(QKeySequence('Delete'))
                self.botonsN[i].setStyleSheet('QPushButton {background-color: #f62c2c}')
            else:
                self.botonsN[i].setShortcut(i)
                if i == '*' or i == '/' or i == '-' or i == '+' or i == '(' or i == ')':
                    self.botonsN[i].setStyleSheet('QPushButton {background-color: #efb047}')
                else:
                    self.botonsN[i].setStyleSheet('QPushButton {background-color: #51b1ea}')

            # Afegim els botons al layout
            BLayoutN.addWidget(self.botonsN[i], p[0], p[1])

            # Si apretem un boto es conectará a la funció per a calcular les operacions
            self.botonsN[i].clicked.connect(self.calc)

        # Afegim el layout dels botons al layout de la calculadora normal
        self.layoutN.addLayout(BLayoutN)

        """
            Part visible de la calculadora Cientifica
        """
        # Creem i afegim al layout el lineEdit per a mostrar el que escrivim, no es podrá seleccionar el text
        self.lineEditC = QLineEdit()
        self.lineEditC.setAlignment(Qt.AlignRight)
        self.lineEditC.setReadOnly(True)
        self.layoutC.addWidget(self.lineEditC)

        # Creem el layout per als botons
        self.botonsC = {}
        BLayoutC = QGridLayout()

        # Crearem la llista amb els botons amb la seva posició
        botonsC = {'AC': (0, 0), '(': (0, 1), ')': (0, 2), '/': (0, 3), '%': (0, 4),
                   '7': (1, 0), '8': (1, 1), '9': (1, 2), '*': (1, 3), '√': (1, 4),
                   '4': (2, 0), '5': (2, 1), '6': (2, 2), '+': (2, 3), '^': (2, 4),
                   '1': (3, 0), '2': (3, 1), '3': (3, 2), '-': (3, 3), 'π': (3, 4),
                   '00': (4, 0), '0': (4, 1), '.': (4, 2), '<-': (4, 3), '=': (4, 4)}

        # Bucle per a afegir el text als botons i seleccionar el tamany "50, 50"
        for i, p in botonsC.items():
            self.botonsC[i] = QPushButton(i)
            self.botonsC[i].setFixedSize(50, 50)

            # Per a poder escriure per teclat utilitzem els if, tambe li agregue colors per a que siga mes visible
            if i == '=':
                self.botonsC[i].setShortcut(QKeySequence('Return'))
                self.botonsC[i].setStyleSheet('QPushButton {background-color: #e951ea}')
            elif i == '<-':
                self.botonsC[i].setShortcut(QKeySequence('Backspace'))
                self.botonsC[i].setStyleSheet('QPushButton {background-color: #e2ec57}')
            elif i == 'AC':
                self.botonsC[i].setShortcut(QKeySequence('Delete'))
                self.botonsC[i].setStyleSheet('QPushButton {background-color: #f62c2c}')
            elif i == 'π':
                self.botonsC[i].setShortcut(QKeySequence('P'))
                self.botonsC[i].setStyleSheet('QPushButton {background-color: #efb047}')
            elif i == "√":
                self.botonsC[i].setShortcut(QKeySequence('V'))
                self.botonsC[i].setStyleSheet('QPushButton {background-color: #efb047}')
            elif i == "^":
                self.botonsC[i].setShortcut(QKeySequence('E'))
                self.botonsC[i].setStyleSheet('QPushButton {background-color: #efb047}')
            else:
                self.botonsC[i].setShortcut(i)
                if i == '*' or i == '/' or i == '-' or i == '+' or i == '(' or i == ')' or i == '%':
                    self.botonsC[i].setStyleSheet('QPushButton {background-color: #efb047}')
                else:
                    self.botonsC[i].setStyleSheet('QPushButton {background-color: #51b1ea}')

            # Afegim els botons al layout
            BLayoutC.addWidget(self.botonsC[i], p[0], p[1])

            # Si apretem un boto es conectará a la funció per a calcular les operacions
            self.botonsC[i].clicked.connect(self.calc)

        # Afegim el layout dels botons al layout de la calculadora normal
        self.layoutC.addLayout(BLayoutC)

        self.tecles = ""
        self.solucio = ""

    """
        FUNCIONS
    """

    # Funció per a calcular les operacions senyalades en la calculadora
    def calc(self):
        if self.sender().text() == "=":
            self.tecles = str((eval(self.tecles)))
            self.solucio += "=" + self.tecles
            self.Guardar()

        elif self.sender().text() == "√":
            if self.tecles == '':
                self.tecles = '0'

            self.tecles = "√" + self.tecles + "=" + str(math.sqrt(int(self.tecles)))
            self.solucio = self.tecles
            self.Guardar()

        elif self.sender().text() == "%":
            self.tecles += "/100"
            self.solucio = self.tecles

        elif self.sender().text() == "^":
            self.tecles += "**"
            self.solucio = self.tecles

        elif self.sender().text() == "π":
            self.tecles += str(math.pi)
            self.solucio = self.tecles

        elif self.sender().text() == "AC":
            self.tecles = ""
            self.solucio = self.tecles

        elif self.sender().text() == "<-":
            self.tecles = self.tecles[:-1]
            self.solucio = self.tecles

        else:
            self.tecles += self.sender().text()
            self.solucio = self.tecles

        self.lineEditC.setText(self.solucio)
        self.lineEditN.setText(self.solucio)

    # Funció per a cambiar a la calculadora normal, habilita el boto de la cientifica i desactiva el de la normal
    def LaNormal(self):
        self.stack.setCurrentWidget(self.normal)
        self.setWindowTitle("Calculadora Normal")
        self.opcioN.setDisabled(True)
        self.opcioC.setDisabled(False)

    # Funció per a cambiar a la calculadora cientifica, habilita el boto de la normal i desactiva el de la cientifica
    def LaCientifica(self):
        self.stack.setCurrentWidget(self.cientifi)
        self.setWindowTitle("Calculadora Cientifica")
        self.opcioC.setDisabled(True)
        self.opcioN.setDisabled(False)

    # Funció per a guardar en un document .txt si el check en el menu esta activat
    def Guardar(self):
        if self.guardar.isChecked():
            try:
                with open(os.path.join(os.path.dirname(__file__), "Resultats.txt"), 'a+') as file:
                    file.write(self.solucio + "\n")
                    file.close()
            except FileNotFoundError as ex:
                return ex
            except IOError as ex:
                return ex

    # Funció per a eixir del programa
    def Eixir(self):

        # Creem el cuadre de dialeg
        eixir = QDialog(self)
        eixir.setWindowTitle("EIXIR")

        # Dos botons, un per a cancelar i seguir en l'aplicacio i l'altre per a eixir
        bto = QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        seleccionar = QDialogButtonBox(bto)

        # Si apretes Ok ix
        seleccionar.accepted.connect(quit)

        # Si apretes Cancelar seguiras en l'aplicació
        seleccionar.rejected.connect(eixir.reject)

        # Creem el layout i li afegim la frase per a confirmar si vol eixir i els botons
        layoutFi = QVBoxLayout()
        segur = QLabel("Segur que vols eixir?")
        segur.setAlignment(Qt.AlignCenter)
        layoutFi.addWidget(segur)
        layoutFi.addWidget(seleccionar)

        eixir.setLayout(layoutFi)
        eixir.exec()


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
