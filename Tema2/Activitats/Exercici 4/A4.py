from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtGui import QScreen
from PySide6.QtCore import QSize

from config import maxima, normal, minima, x, y

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Tamaño de la pantalla
        self.my_screen = QScreen.availableGeometry(QApplication.primaryScreen())

        self.pybutton = QPushButton('Maximiza', self)
        self.pybutton2 = QPushButton('Normalitza', self)
        self.pybutton3 = QPushButton('Minimiza', self)
        
        #Connectem la senyal clicked a la ranura button_pressed
        self.pybutton.clicked.connect(self.button_pressed1)     
        self.pybutton2.clicked.connect(self.button_pressed2)
        self.pybutton3.clicked.connect(self.button_pressed3)
        
        self.pybutton.resize(x, y)
        self.pybutton2.resize(x, y)
        self.pybutton3.resize(x, y)
           
           
        self.setWindowTitle("Ventana normal")

        self.cambia_tam(normal)
        self.setFixedSize(normal)

        self.pybutton.setEnabled(True)
        self.pybutton2.setEnabled(False) 
        self.pybutton3.setEnabled(True)




    def button_pressed1(self):

        self.setWindowTitle("Ventana Maximizada")
        self.setFixedSize(maxima)
        self.cambia_tam(maxima)
        
        self.pybutton.setEnabled(False)
        self.pybutton2.setEnabled(True)
        self.pybutton3.setEnabled(True)
        
            
    def button_pressed2(self):

        self.setWindowTitle("Ventana Normal")
        self.setFixedSize(normal)
        self.cambia_tam(normal)
        
        self.pybutton.setEnabled(True)
        self.pybutton2.setEnabled(False) 
        self.pybutton3.setEnabled(True)

        
    def button_pressed3(self):

        self.setWindowTitle("Ventana Minimizada")
        self.setFixedSize(minima)
        self.cambia_tam(minima)
        
        self.pybutton.setEnabled(True)
        self.pybutton2.setEnabled(True)
        self.pybutton3.setEnabled(False)
        

    def cambia_tam(self, gran):
        
        self.move((self.my_screen.width() - gran.width()) / 2, (self.my_screen.height() - gran.height()) / 2)
        self.pybutton.move((gran.width() / 5) - (x / 2), (gran.height() / 2) - (y / 2))
        self.pybutton2.move((gran.width() / 2) - (x / 2), (gran.height() / 2) - (y / 2))
        self.pybutton3.move((gran.width() / 1.25) - (x / 2), (gran.height() / 2) - (y / 2))
    

if __name__ == "__main__":
    app = QApplication([])
    mainWin = MainWindow()
    mainWin.show()
    app.exec()