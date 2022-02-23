from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QHBoxLayout, QWidget, QPushButton, QComboBox, QVBoxLayout, QToolBar
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtGui import Qt, QAction, QPainter
from PySide6.QtCore import QPointF

import sys
import os
import csv

carpeta = os.path.dirname(__file__)
    
#Finestra de Login per a iniciar el programa
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        #Titol de la finestra login
        self.setWindowTitle("Login")
        
        #Seccio del ususari
        self.labelU = QLabel("Usuari")
        self.user = QLineEdit()
        self.user.setPlaceholderText("admin")
        
        #Secció de la contrasenya
        self.labelC = QLabel("Contrasenya")
        self.contra = QLineEdit()
        self.contra.setPlaceholderText("1234")
        self.contra.setEchoMode(QLineEdit.Password) #Contrasenya oculta 
       
        #Boto per a entrar al programa
        self.botoEntrar = QPushButton("Entrar")
        self.botoEntrar.clicked.connect(self.conectaCovid)

        #Boto per a eixir del programa
        self.botoEixir = QPushButton("Eixir")
        self.botoEixir.clicked.connect(self.tancaCovid)
        
        #Afig els botons a un layout Horizontal
        self.layoutH = QHBoxLayout()
        self.layoutH.addWidget(self.botoEntrar)
        self.layoutH.addWidget(self.botoEixir)

        #Afig la part de usuari, contrasenya y el layout horizontal a un layout vertical
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.labelU)
        self.layout.addWidget(self.user)
        self.layout.addWidget(self.labelC)
        self.layout.addWidget(self.contra)
        self.layout.addLayout(self.layoutH)

        #Crea el widget principal de l'aplicació
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        #Obri la finestra de Error en cas de estar mal el usuari o la contrasenya
        self.error = ErrorW()
        
    #Si apretes el boto de entrar, fara comprovacions per a conectarse a l'aplicació
    def conectaCovid(self):
        self.close()

        #Comprova si el usuari y la contrasenya son correctes
        if self.user.text() == "admin" and self.contra.text() == "1234":
            window.show()
        #Si no es correcte mostrará la finestra de Error
        else:
            self.error.show()

    #Si apretes el boto de eixir es tancará tota l'aplicació
    def tancaCovid(self):
        self.close()

#Finestra principal 
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #Titol de la aplicació
        self.setWindowTitle('Info Covid')
        
        #Crea els layouts
        self.layoutH = QHBoxLayout()
        self.segonLayoutH = QHBoxLayout()
        self.layoutV = QVBoxLayout()
        self.layoutV.addLayout(self.layoutH)
        self.layoutV.addLayout(self.segonLayoutH)

        #Boto de PCR del municipi seleccionat
        self.info = QAction("PCR", self)
        self.info.triggered.connect(self.traureInformacio)

        #Boto de incidencies del municipi seleccionat
        self.incide = QAction("Incidencies", self)
        self.incide.triggered.connect(self.traureIncidencies)

        #Boto de defuncions del municipi seleccionat
        self.defu = QAction("Defuncions", self)
        self.defu.triggered.connect(self.traureDefuncions)
        
        #Menu Tool Bar par a posar els botons de PCR, incidencies i defuncions
        self.menu=QToolBar("Menu")
        self.addToolBar(self.menu)
        self.menu.addAction(self.info)
        self.menu.addAction(self.incide)
        self.menu.addAction(self.defu)
        
        #Text Municipi
        self.labelMunicipi = QLabel("Municipi:")
        self.labelMunicipi.setAlignment(Qt.AlignRight)

        #Quan entrem a l'aplicació per primera vegada no es mostra ni el text, ni el ComboBox, ni el boto
        self.labelMunicipi.setVisible(False)
        
        #ComboBox per a seleccionar el municipi
        self.municipi = QComboBox()
        self.municipi.setEditable(True)
        self.municipi.setVisible(False)
        
        #Boto de buscar en la secció de Incidencies
        self.botoBuscarInsi = QPushButton("Buscar")

        #Li asigne una llargaria i el faig invisible
        self.botoBuscarInsi.setFixedWidth(100)
        self.botoBuscarInsi.setVisible(False)
        self.botoBuscarInsi.clicked.connect(self.traureIncidencies)

        #Boto de buscar en la secció de PCR
        self.botoBuscarInfo = QPushButton("Buscar")

        #Li asigne una llargaria i el faig invisible
        self.botoBuscarInfo.setFixedWidth(100)
        self.botoBuscarInfo.setVisible(False)
        self.botoBuscarInfo.clicked.connect(self.traureInformacio)

        #Boto de buscar en la secció de Defuncions
        self.botoBuscarDefu = QPushButton("Buscar")

        #Li asigne una llargaria i el faig invisible
        self.botoBuscarDefu.setFixedWidth(100)
        self.botoBuscarDefu.setVisible(False)
        self.botoBuscarDefu.clicked.connect(self.traureDefuncions)

        #Li asigne al layout horizontal el text, el comboBox i els botons
        self.layoutH.addWidget(self.labelMunicipi)
        self.layoutH.addWidget(self.municipi)
        self.layoutH.addWidget(self.botoBuscarInsi)
        self.layoutH.addWidget(self.botoBuscarInfo)
        self.layoutH.addWidget(self.botoBuscarDefu)

        #Un missatge que diu de que va l'aplicació, despres es cambiará per la informació seleccionada
        self.labelMissa = QLabel()
        self.labelMissa.setFixedHeight(90)
        self.labelMissa.setFixedWidth(700)
        self.labelMissa.setText('Informació del covid en els municipis de la Comunitat Valenciana')

        #Afig un tamany mes gran per a que es visualitze millor
        self.font = self.labelMissa.font()
        self.font.setPointSize(11)
        self.labelMissa.setFont(self.font)
        
        #Obri el archiu csv per a llegir els municipis i afegirlos al comboBox
        with open(
            carpeta + '/grafics/31.csv', mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file,  delimiter=";")
            contador = 0
            for i in leer:
                if (contador == 0):
                    contador += 1
                else:
                    self.municipi.addItem(i[1])
                    
        #Un label de 500 x 700, es on es mostraran els grafics mes avant
        self.labelChart = QLabel()
        self.labelChart.setFixedHeight(500)
        self.labelChart.setFixedWidth(700)
        self.labelChart.setText("Aplicació: Info Covid")
        self.labelChart.setAlignment(Qt.AlignCenter)
        self.segonLayoutH.addWidget(self.labelChart)

        #Tamany de lletra del text del label
        self.font2 = self.labelChart.font()
        self.font2.setPointSize(22)
        self.labelChart.setFont(self.font2)

        #ChartView per a escriure la informació de l'aplicació, posteriorment dirá la informacio del municipi seleccionat
        self.graphWidget = QChartView()
        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)

        self.layoutV.addWidget(self.labelMissa)

        #Widget central
        self.widget = QWidget()
        self.widget.setLayout(self.layoutV)
        self.setCentralWidget(self.widget)

    #Funció per a traure les incidencies dels ultims 31 dies
    def traureIncidencies(self):

        #Fem visible i funcional el boto i el comboBox de les incidencies
        self.municipi.setVisible(True)
        self.labelMunicipi.setVisible(True)
        self.botoBuscarInsi.setEnabled(True)
        self.botoBuscarInsi.setVisible(True)
        
        #Desabilitem el boto de informació
        self.botoBuscarInfo.setEnabled(False)
        self.botoBuscarInfo.setVisible(False)
        
        self.graphWidget.close()
        self.segonLayoutH.addWidget(self.labelChart)
        
        #Será un grafic de linies, aixi que gaste un LineSeries
        self.series = QLineSeries()
 
        #Obri el archiu 03.csv per a llegir els municipis i amb el for seleccionem les incidencies del municipi corresponent
        with open(
            
            carpeta + '/grafics/03.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    inci = i[5]

            #Agrega un punt en el inici(0.0) i un altre en el 3 ja que son els 3 primers dies
            self.series.append(QPointF(0.0, float(inci)))
            self.series.append(QPointF(3.0, float(inci)))

        #Obri el archiu 05.csv per a llegir els municipis i amb el for seleccionem les incidencies del municipi corresponent
        with open(
            carpeta + '/grafics/05.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    inci = i[5]

            #Agrega un punt en el 5.0 ja que dels 5 primers dies
            self.series.append(QPointF(5.0, float(inci)))

        #Obri el archiu 10.csv per a llegir els municipis i amb el for seleccionem les incidencies del municipi corresponent
        with open(
            carpeta + '/grafics/10.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    inci = i[5]

            #Agrega un punt en el 10.0 ja que dels 10 primers dies
            self.series.append(QPointF(10.0, float(inci)))

        #Obri el archiu 13.csv per a llegir els municipis i amb el for seleccionem les incidencies del municipi corresponent
        with open(
            carpeta + '/grafics/13.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    inci = i[5]

            #Agrega un punt en el 13.0 ja que dels 13 primers dies
            self.series.append(QPointF(13.0, float(inci)))

        #Obri el archiu 17.csv per a llegir els municipis i amb el for seleccionem les incidencies del municipi corresponent
        with open(
            carpeta + '/grafics/17.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    inci = i[5]

            #Agrega un punt en el 17.0 ja que dels 17 primers dies
            self.series.append(QPointF(17.0, float(inci)))

        #Obri el archiu 20.csv per a llegir els municipis i amb el for seleccionem les incidencies del municipi corresponent
        with open(
            carpeta + '/grafics/20.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    inci = i[5]

            #Agrega un punt en el 20.0 ja que dels 20 primers dies
            self.series.append(QPointF(20.0, float(inci)))

        #Obri el archiu 24.csv per a llegir els municipis i amb el for seleccionem les incidencies del municipi corresponent
        with open(
            carpeta + '/grafics/24.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    inci = i[5]

            #Agrega un punt en el 24.0 ja que dels 24 primers dies
            self.series.append(QPointF(24.0, float(inci)))

        #Obri el archiu 27.csv per a llegir els municipis i amb el for seleccionem les incidencies del municipi corresponent
        with open(
            carpeta + '/grafics/27.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    inci = i[5]

            #Agrega un punt en el 27.0 ja que dels 27 primers dies
            self.series.append(QPointF(27.0, float(inci)))

        #Obri el archiu 31.csv per a llegir els municipis i amb el for seleccionem les incidencies del municipi corresponent
        with open(
            carpeta + '/grafics/31.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    inci = i[5]

            #Cambia el text de baix del grafic posant la informació de les incidencies
            self.labelMissa.setText("Informació de " + self.municipi.currentText() + ": \n" +
            "   Numero de Incidencies: " + inci)

            #Agrega un punt en el 31.0 ja que es de tots els dies
            self.series.append(QPointF(31.0, float(inci)))
            
        #Neteja els grafics 
        self.segonLayoutH.removeWidget(self.labelChart)
        self.segonLayoutH.removeWidget(self.graphWidget)
        self.graphWidget.close()

        #Crea el grafic i li agrega les linies per a mostrar les incidencies
        self.chart = QChart()
        self.chart.setTitle("Incidencies") #Titol del grafic
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()

        #Tornem a afegir el ChartView actualizat amb el nou grafic
        self.graphWidget = QChartView(self.chart)
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.segonLayoutH.addWidget(self.graphWidget)
            
    #Funció per a mostrar els grafics de les PCR de cada municipi
    def traureInformacio(self):
        
        #Habilita el comboBox i el boto de PCR
        self.municipi.setVisible(True)
        self.labelMunicipi.setVisible(True)
        self.botoBuscarInfo.setEnabled(True)
        self.botoBuscarInfo.setVisible(True)

        #Deshabilita el boto de les incidencies i defuncions
        self.botoBuscarInsi.setEnabled(False)
        self.botoBuscarInsi.setVisible(False)
        self.botoBuscarDefu.setEnabled(False)
        self.botoBuscarDefu.setVisible(False)
        
        self.graphWidget.close()

        #Será un grafic de linies, aixi que gaste un LineSeries
        self.seriesPcr = QLineSeries()

        #Obri el archiu 03.csv per a llegir els municipis i amb el for seleccionem les pcr del municipi corresponent
        with open(
            carpeta + '/grafics/03.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    pcr = i[2]

            #Agrega un punt en el inici(0.0) i un altre en el 3 ja que son els 3 primers dies
            self.seriesPcr.append(QPointF(0.0, float(pcr)))
            self.seriesPcr.append(QPointF(3.0, float(pcr)))

        #Obri el archiu 05.csv per a llegir els municipis i amb el for seleccionem les pcr del municipi corresponent
        with open(
            carpeta + '/grafics/05.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    pcr = i[2]

            #Agrega un punt en el 5 ja que son els 5 primers dies
            self.seriesPcr.append(QPointF(5.0, float(pcr)))

        #Obri el archiu 10.csv per a llegir els municipis i amb el for seleccionem les pcr del municipi corresponent
        with open(
            carpeta + '/grafics/10.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    pcr = i[2]

            #Agrega un punt en el 10 ja que son els 10 primers dies
            self.seriesPcr.append(QPointF(10.0, float(pcr)))

        #Obri el archiu 13.csv per a llegir els municipis i amb el for seleccionem les pcr del municipi corresponent
        with open(
            carpeta + '/grafics/13.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    pcr = i[2]

            #Agrega un punt en el 13 ja que son els 13 primers dies
            self.seriesPcr.append(QPointF(13.0, float(pcr)))

        #Obri el archiu 17.csv per a llegir els municipis i amb el for seleccionem les pcr del municipi corresponent
        with open(
            carpeta + '/grafics/17.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    pcr = i[2]

            #Agrega un punt en el 17 ja que son els 17 primers dies
            self.seriesPcr.append(QPointF(17.0, float(pcr)))

        #Obri el archiu 20.csv per a llegir els municipis i amb el for seleccionem les pcr del municipi corresponent
        with open(
            carpeta + '/grafics/20.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    pcr = i[2]

            #Agrega un punt en el 20 ja que son els 20 primers dies
            self.seriesPcr.append(QPointF(20.0, float(pcr)))

        #Obri el archiu 24.csv per a llegir els municipis i amb el for seleccionem les pcr del municipi corresponent
        with open(
            carpeta + '/grafics/24.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    pcr = i[2]

            #Agrega un punt en el 24 ja que son els 24 primers dies
            self.seriesPcr.append(QPointF(24.0, float(pcr)))

        #Obri el archiu 27.csv per a llegir els municipis i amb el for seleccionem les pcr del municipi corresponent
        with open(
            carpeta + '/grafics/27.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    pcr = i[2]

            #Agrega un punt en el 3 ja que son els 27 primers dies
            self.seriesPcr.append(QPointF(27.0, float(pcr)))

        #Obri el archiu 31.csv per a llegir els municipis i amb el for seleccionem les pcr del municipi corresponent
        with open(
            carpeta + '/grafics/31.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    pcr = i[2]

            #Cambia el missatge de baix del grafic per a mostrar la informació de les PCR
            self.labelMissa.setText('Informació de ' + self.municipi.currentText() + ": \n" +
            "   Numero de PCR: " + pcr + ".")

            #Agrega un punt en el 31 ja que es tot el mes
            self.seriesPcr.append(QPointF(31.0, float(pcr)))

        #Neteja els grafics 
        self.segonLayoutH.removeWidget(self.labelChart)
        self.segonLayoutH.removeWidget(self.graphWidget)
        self.graphWidget.close()

        #Crea el grafic i li agrega les linies per a mostrar les incidencies
        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.seriesPcr)
        self.chart.createDefaultAxes()
        self.chart.setTitle("PCR")
        self.chart.createDefaultAxes()

        #Tornem a afegir el ChartView actualizat amb el nou grafic
        self.graphWidget = QChartView(self.chart)
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.segonLayoutH.addWidget(self.graphWidget)

    #Funció per a traure les incidencies dels ultims 31 dies
    def traureDefuncions(self):

        #Fem visible i funcional el boto i el comboBox de les defuncions
        self.botoBuscarDefu.setEnabled(True)
        self.botoBuscarDefu.setVisible(True)
        self.municipi.setVisible(True)
        self.labelMunicipi.setVisible(True)

        self.botoBuscarInsi.setEnabled(False)
        self.botoBuscarInsi.setVisible(False)
        
        #Desabilitem el boto de PCR i Incidencies
        self.botoBuscarInfo.setEnabled(False)
        self.botoBuscarInfo.setVisible(False)
        
        self.graphWidget.close()
        self.segonLayoutH.addWidget(self.labelChart)
        
        #Será un grafic de linies, aixi que gaste un LineSeries
        self.series = QLineSeries()
 
        #Obri el archiu 03.csv per a llegir els municipis i amb el for seleccionem les defuncions del municipi corresponent
        with open(
            
            carpeta + '/grafics/03.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    defu = i[6]

            #Agrega un punt en el inici(0.0) i un altre en el 3 ja que son els 3 primers dies
            self.series.append(QPointF(0.0, float(defu)))
            self.series.append(QPointF(3.0, float(defu)))

        #Obri el archiu 05.csv per a llegir els municipis i amb el for seleccionem les defuncions del municipi corresponent
        with open(
            carpeta + '/grafics/05.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    defu = i[6]

            #Agrega un punt en el 5.0 ja que dels 5 primers dies
            self.series.append(QPointF(5.0, float(defu)))

        #Obri el archiu 10.csv per a llegir els municipis i amb el for seleccionem les defuncions del municipi corresponent
        with open(
            carpeta + '/grafics/10.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    defu = i[6]

            #Agrega un punt en el 10.0 ja que dels 10 primers dies
            self.series.append(QPointF(10.0, float(defu)))

        #Obri el archiu 13.csv per a llegir els municipis i amb el for seleccionem les defuncions del municipi corresponent
        with open(
            carpeta + '/grafics/13.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    defu = i[6]

            #Agrega un punt en el 13.0 ja que dels 13 primers dies
            self.series.append(QPointF(13.0, float(defu)))

        #Obri el archiu 17.csv per a llegir els municipis i amb el for seleccionem les defuncions del municipi corresponent
        with open(
            carpeta + '/grafics/17.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    defu = i[6]

            #Agrega un punt en el 17.0 ja que dels 17 primers dies
            self.series.append(QPointF(17.0, float(defu)))

        #Obri el archiu 20.csv per a llegir els municipis i amb el for seleccionem les defuncions del municipi corresponent
        with open(
            carpeta + '/grafics/20.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    defu = i[6]

            #Agrega un punt en el 20.0 ja que dels 20 primers dies
            self.series.append(QPointF(20.0, float(defu)))

        #Obri el archiu 24.csv per a llegir els municipis i amb el for seleccionem les defuncions del municipi corresponent
        with open(
            carpeta + '/grafics/24.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    defu = i[6]

            #Agrega un punt en el 24.0 ja que dels 24 primers dies
            self.series.append(QPointF(24.0, float(defu)))

        #Obri el archiu 27.csv per a llegir els municipis i amb el for seleccionem les defuncions del municipi corresponent
        with open(
            carpeta + '/grafics/27.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    defu = i[6]

            #Agrega un punt en el 27.0 ja que dels 27 primers dies
            self.series.append(QPointF(27.0, float(defu)))

        #Obri el archiu 31.csv per a llegir els municipis i amb el for seleccionem les defuncions del municipi corresponent
        with open(
            carpeta + '/grafics/31.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText()
                if i[1] == municipi:
                    defu = i[6]

            #Cambia el text de baix del grafic posant la informació de les defuncions
            self.labelMissa.setText("Informació de " + self.municipi.currentText() + ": \n" +
            "   Numero de Defuncions: " + defu)

            #Agrega un punt en el 31.0 ja que es de tots els dies
            self.series.append(QPointF(31.0, float(defu)))
            
        #Neteja els grafics 
        self.segonLayoutH.removeWidget(self.labelChart)
        self.segonLayoutH.removeWidget(self.graphWidget)
        self.graphWidget.close()

        #Crea el grafic i li agrega les linies per a mostrar les incidencies
        self.chart = QChart()
        self.chart.setTitle("Defuncions") #Titol del grafic
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()

        #Tornem a afegir el ChartView actualizat amb el nou grafic
        self.graphWidget = QChartView(self.chart)
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.segonLayoutH.addWidget(self.graphWidget)
         
#Finestra de error en cas de posar mal el usuari o la contrasenya
class ErrorW(QMainWindow):
    def __init__(self):
        super(ErrorW, self).__init__()

        #Titol de la finestra
        self.setWindowTitle("ERROR")
        
        #Text que adverteix que hi ha un error
        self.label = QLabel("Usuari i contrasenya incorrecte! Torna a intentar.")

        #Boto per a tornat al login
        self.boto = QPushButton("Aceptar")
        self.boto.clicked.connect(self.cerrar)

        #Layout Vertical per a posar el text i el boto
        self.layoutV = QVBoxLayout()
        self.layoutV.addWidget(self.label)
        self.layoutV.addWidget(self.boto)

        #Widget central
        self.widget = QWidget()
        self.widget.setLayout(self.layoutV)
        self.setCentralWidget(self.widget)

    #Si apretes el boto tanca la pestanya i torna a obrir el login
    def cerrar(self):
        self.close()
        iniciar.show()

#Aplicació principal
app = QApplication(sys.argv)
#Finestra principal, la dels grafics
window = MainWindow()
#Finestra de login
iniciar = LoginWindow()
#iniciem primer la finestra de login
iniciar.show()
app.exec()