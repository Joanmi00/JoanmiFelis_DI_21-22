from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QHBoxLayout
from PySide6.QtWidgets import QWidget, QPushButton, QComboBox, QVBoxLayout, QToolBar 
from PySide6.QtGui import Qt, QAction, QPainter
from PySide6.QtCharts import (QBarSet, QChart, QChartView, QLineSeries, QStackedBarSeries, QBarCategoryAxis)

import sys
import os
import csv

carpeta = os.path.dirname(__file__)
    
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setWindowTitle("Login")
        
        self.labelU = QLabel("Usuari")
        self.user = QLineEdit()
        self.user.setPlaceholderText("admin")
        
        self.labelC = QLabel("Contrasenya")
        self.contra = QLineEdit()
        self.contra.setPlaceholderText("1234")
        self.contra.setEchoMode(QLineEdit.Password)
       
        self.botoEntrar = QPushButton("Entrar")
        self.botoEntrar.clicked.connect(self.conectarapp)

        self.botoEixir = QPushButton("Eixir")
        self.botoEixir.clicked.connect(self.cerrarapp)
        
        self.layoutH = QHBoxLayout()
        self.layoutH.addWidget(self.botoEntrar)
        self.layoutH.addWidget(self.botoEixir)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.labelU)
        self.layout.addWidget(self.user)
        self.layout.addWidget(self.labelC)
        self.layout.addWidget(self.contra)
        self.layout.addLayout(self.layoutH)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.error = ErrorW()
        
    def conectarapp(self):
        self.close()

        if self.user.text() == "admin" and self.contra.text() == "1234":
            window.show()
        else:
            self.error.show()

    def cerrarapp(self):
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Info Covid')
        
        self.widget = QWidget()
        self.layoutH = QHBoxLayout()
        self.segonLayoutH = QHBoxLayout()
        self.layoutV = QVBoxLayout()
        self.layoutV.addLayout(self.layoutH)
        self.layoutV.addLayout(self.segonLayoutH)


        self.total = QAction("Total Comunitat", self)
        self.total.triggered.connect(self.totalcovid)
        
        self.info = QAction("Info Municipis", self)
        self.info.triggered.connect(self.traureInformacio)

        self.incide = QAction("Incidencies", self)
        self.incide.triggered.connect(self.traureIncidencies)
        
        self.menu=QToolBar("Menu")
        self.addToolBar(self.menu)
        self.menu.addAction(self.total)
        self.menu.addAction(self.info)
        self.menu.addAction(self.incide)
        
        self.labelMunicipi = QLabel("Municipi:")
        self.labelMunicipi.setAlignment(Qt.AlignRight)
        self.layoutH.addWidget(self.labelMunicipi)
        
        self.municipi = QComboBox()
        self.municipi.setEditable(True)
        self.municipi.setEnabled(False)
        self.layoutH.addWidget(self.municipi)
        
        ''' BOTON INCIDENCIAS'''
        self.botoBuscarInsi = QPushButton("Buscar")

        self.botoBuscarInsi.setFixedWidth(100)
        self.botoBuscarInsi.setFixedHeight(25)
        self.botoBuscarInsi.setVisible(False)
        self.botoBuscarInsi.clicked.connect(self.traureIncidencies)

        self.layoutH.addWidget(self.botoBuscarInsi)
        
        ''' BOTON TASA FALLEICOD'''
        self.botoBuscarInfo = QPushButton("Buscar")

        self.botoBuscarInfo.setFixedWidth(100)
        self.botoBuscarInfo.setFixedHeight(25)
        self.botoBuscarInfo.setVisible(False)
        self.botoBuscarInfo.clicked.connect(self.traureInformacio)

        self.layoutH.addWidget(self.botoBuscarInfo)
        
        ''' LABEL TEXTO DATOS '''
        
        with open(
            
            carpeta + '/Covid/InfoTotal.csv', mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file)
            contador = 0

            for i in leer:
                if contador == 0:
                    pcr = i[0]
                elif contador == 2:
                    hospi = i[0]
                elif contador == 4:
                    inci = i[0]
                elif contador == 5:
                    defu = i[0]
                contador += 1

        self.labelMissa = QLabel()
        self.labelMissa.setFixedHeight(120)
        self.labelMissa.setFixedWidth(700)
        self.labelMissa.setText('INFORMACIÓ TOTAL EN LA COMUNITAT VALENCIANA:' + '\n' +
                "PCR: " + pcr + "\n" +
                "Incidencies: " + inci + "\n"+
                "Defuncions: " + defu + "\n"+
                "Hospitalitzats: " + hospi + "\n"
            )

        self.font = self.labelMissa.font()
        self.font.setPointSize(12)
        self.labelMissa.setFont(self.font)
        
        
        ''' RELLENAR COMBOBOX MUNICIPIOS'''
        with open(
            carpeta + '/Covid/grafics/31.csv', mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file,  delimiter=";")
            contador = 0
            for i in leer:
                if (contador == 0):
                    contador += 1
                else:
                    self.municipi.addItem(i[1])
                    
                    
        self.labelChart = QChartView(self.grafico_total())
        self.labelChart.setFixedHeight(500)
        self.labelChart.setFixedWidth(700)
        self.labelChart.setAlignment(Qt.AlignCenter)
        self.segonLayoutH.addWidget(self.labelChart)   

        self.graphWidget = QChartView()
        self.graphWidget.setFixedHeight(300)
        self.graphWidget.setFixedWidth(900)

        self.layoutV.addWidget(self.labelMissa)

        self.widget.setLayout(self.layoutV)
        self.setCentralWidget(self.widget)
        
    def totalcovid(self):
        
        self.municipi.setEnabled(False)
        self.botoBuscarInsi.setEnabled(False)
        self.botoBuscarInfo.setEnabled(False)

        with open(
            
            carpeta + '/Covid/InfoTotal.csv', mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file)
            contador = 0

            for i in leer:
                if contador == 0:
                    pcr = i[0]
                elif contador == 2:
                    hospi = i[0]
                elif contador == 4:
                    inci = i[0]
                elif contador == 5:
                    defu = i[0]
                contador += 1

            self.labelMissa.setText('INFORMACIÓ TOTAL EN LA COMUNITAT VALENCIANA:' + '\n' +
                "PCR: " + pcr + "\n" +
                "Incidencies: " + inci + "\n"+
                "Defuncions: " + defu + "\n"+
                "Hospitalitzats: " + hospi + "\n"
            )
            
        self.segonLayoutH.removeWidget(self.labelChart)
        self.segonLayoutH.removeWidget(self.graphWidget)
        self.graphWidget.close()

        self.graphWidget = QChartView(self.grafico_total())
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.segonLayoutH.addWidget(self.graphWidget)

    def traureIncidencies(self):

        self.municipi.setEnabled(True)
        
        self.botoBuscarInsi.setEnabled(True)
        self.botoBuscarInsi.setVisible(True)
        
        self.botoBuscarInfo.setEnabled(False)
        self.botoBuscarInfo.setVisible(False)
        
        self.graphWidget.close()
        self.segonLayoutH.addWidget(self.labelChart)
        
        self.series = QLineSeries()

        with open(
            
            carpeta + '/Covid/grafics/31.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    inci = i[5]

            self.series.append(QPointF(0.0, float(inci)))
            self.series.append(QPointF(3.0, float(inci)))

        with open(
            carpeta + '/Covid/grafics/05.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    inci = i[5]

            self.series.append(QPointF(5.0, float(inci)))

        with open(
            carpeta + '/Covid/grafics/10.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    inci = i[5]

            self.series.append(QPointF(10.0, float(inci)))

        with open(
            carpeta + '/Covid/grafics/13.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    inci = i[5]

            self.series.append(QPointF(13.0, float(inci)))

        with open(
            carpeta + '/Covid/grafics/17.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    inci = i[5]

            self.series.append(QPointF(17.0, float(inci)))

        with open(
            carpeta + '/Covid/grafics/20.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    inci = i[5]

            self.series.append(QPointF(20.0, float(inci)))

        with open(
            carpeta + '/Covid/grafics/24.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    inci = i[5]

            self.series.append(QPointF(24.0, float(inci)))

        with open(
            carpeta + '/Covid/grafics/27.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    inci = i[5]

            self.series.append(QPointF(27.0, float(inci)))

        with open(
            carpeta + '/Covid/grafics/31.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    inci = i[5]

            self.labelMissa.setText('Incidencies en ' + self.municipi.currentText() + ": " + inci)
            self.series.append(QPointF(31.0, float(inci)))
            
        self.segonLayoutH.removeWidget(self.labelChart)
        self.segonLayoutH.removeWidget(self.graphWidget)
        self.graphWidget.close()

        self.chart = QChart()
        self.chart.setTitle("incide")
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()

        self.graphWidget = QChartView(self.chart)
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.segonLayoutH.addWidget(self.graphWidget)
            
    def traureInformacio(self):
        
        self.municipi.setEnabled(True)
        
        self.botoBuscarInsi.setEnabled(False)
        self.botoBuscarInsi.setVisible(False)
        
        self.botoBuscarInfo.setEnabled(True)
        self.botoBuscarInfo.setVisible(True)

        self.graphWidget.close()

        self.seriesPcr = QLineSeries()
        self.seriesDef = QLineSeries()
        self.seriesTasa = QLineSeries()

        with open(
            carpeta + '/Covid/grafics/03.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    pcr = i[2]
                    defu = i[6]
                    tasa = i[7]

            self.seriesPcr.append(QPointF(0.0, float(pcr)))
            self.seriesDef.append(QPointF(0.0, float(defu)))
            self.seriesTasa.append(QPointF(0.0, float(tasa)))
            self.seriesPcr.append(QPointF(3.0, float(pcr)))
            self.seriesDef.append(QPointF(3.0, float(defu)))
            self.seriesTasa.append(QPointF(3.0, float(tasa)))

        with open(
            carpeta + '/Covid/grafics/05.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    pcr = i[2]
                    defu = i[6]
                    tasa = i[7]
            self.seriesPcr.append(QPointF(5.0, float(pcr)))
            self.seriesDef.append(QPointF(5.0, float(defu)))
            self.seriesTasa.append(QPointF(5.0, float(tasa)))

        with open(
            carpeta + '/Covid/grafics/10.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    pcr = i[2]
                    defu = i[6]
                    tasa = i[7]

            self.seriesPcr.append(QPointF(10.0, float(pcr)))
            self.seriesDef.append(QPointF(10.0, float(defu)))
            self.seriesTasa.append(QPointF(10.0, float(tasa)))

        with open(
            carpeta + '/Covid/grafics/13.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    pcr = i[2]
                    defu = i[6]
                    tasa = i[7]

            self.seriesPcr.append(QPointF(13.0, float(pcr)))
            self.seriesDef.append(QPointF(13.0, float(defu)))
            self.seriesTasa.append(QPointF(13.0, float(tasa)))

        with open(
            carpeta + '/Covid/grafics/17.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    pcr = i[2]
                    defu = i[6]
                    tasa = i[7]

            self.seriesPcr.append(QPointF(17.0, float(pcr)))
            self.seriesDef.append(QPointF(17.0, float(defu)))
            self.seriesTasa.append(QPointF(17.0, float(tasa)))

        with open(
            carpeta + '/Covid/grafics/20.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    pcr = i[2]
                    defu = i[6]
                    tasa = i[7]

            self.seriesPcr.append(QPointF(20.0, float(pcr)))
            self.seriesDef.append(QPointF(20.0, float(defu)))
            self.seriesTasa.append(QPointF(20.0, float(tasa)))

        with open(
            carpeta + '/Covid/grafics/24.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    pcr = i[2]
                    defu = i[6]
                    tasa = i[7]

            self.seriesPcr.append(QPointF(24.0, float(pcr)))
            self.seriesDef.append(QPointF(24.0, float(defu)))
            self.seriesTasa.append(QPointF(24.0, float(tasa)))

        with open(
            carpeta + '/Covid/grafics/27.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    pcr = i[2]
                    defu = i[6]
                    tasa = i[7]

            self.seriesPcr.append(QPointF(27.0, float(pcr)))
            self.seriesDef.append(QPointF(27.0, float(defu)))
            self.seriesTasa.append(QPointF(27.0, float(tasa)))

        with open(
            carpeta + '/Covid/grafics/31.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file, delimiter=";")

            for i in leer:
                municipi = self.municipi.currentText().replace(' ','')
                if i[1] == municipi:
                    pcr = i[2]
                    defu = i[6]
                    tasa = i[7]

            self.labelMissa.setText('INFORMACIÓ DE: ' + self.municipi.currentText() + ": \n" +
            "PCR: " + pcr + ". \n" +
            "Defuncions: " + defu + ". \n" +
            "Tasa de Defuncions: " + tasa + "%.")

            self.seriesPcr.append(QPointF(31.0, float(pcr)))
            self.seriesDef.append(QPointF(31.0, float(defu)))
            self.seriesTasa.append(QPointF(31.0, float(tasa)))

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.seriesPcr)
        self.chart.addSeries(self.seriesDef)
        self.chart.addSeries(self.seriesTasa)
        self.chart.createDefaultAxes()
        self.chart.setTitle("| 'Blau': PCR | 'Verd': Defuncions | 'Taronja': Tasa de Defuncions |")
        
        self.segonLayoutH.removeWidget(self.labelChart)
        self.segonLayoutH.removeWidget(self.graphWidget)
        self.graphWidget.close()

        self.chart.createDefaultAxes()

        self.graphWidget = QChartView(self.chart)
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.segonLayoutH.addWidget(self.graphWidget)
            
    
    def grafico_total(self):
    
        self.bar1 = QBarSet("PCR+")
        self.bar2 = QBarSet("incide")
        self.bar3 = QBarSet("Defuncions")
        self.bar4 = QBarSet("Hospitalitzats")

        self.categorias = ["PCR+", "incide",
                           "Defuncions", "Hospitalitzats"]

        with open(
            carpeta + '/Covid/InfoTotal.csv' , mode = 'r', encoding ='UTF8') as file:
            leer = csv.reader(file)

            for i, data in enumerate(leer):
                if (i == 0):
                    self.bar1.append([int(data[0]), 0, 0, 0])
                if (i == 4):
                    self.bar2.append([0, int(data[0]), 0, 0])
                if (i == 5):
                    self.bar3.append([0, 0, int(data[0]), 0])
                if (i == 2):
                    self.bar4.append([0, 0, 0, int(data[0])])

        self.barras_grafico = QStackedBarSeries()
        self.barras_grafico.append(self.bar1)
        self.barras_grafico.append(self.bar2)
        self.barras_grafico.append(self.bar3)
        self.barras_grafico.append(self.bar4)
        
        self.chart = QChart()
        self.chart.addSeries(self.barras_grafico)
        self.chart.setTitle("Gráfico TOTAL COVID")

        self.chart.createDefaultAxes()
        self.chart.removeAxis(self.chart.axisX())

        categorias_axis = QBarCategoryAxis()
        categorias_axis.append(self.categorias)

        return self.chart
         
class ErrorW(QMainWindow):
    def __init__(self):
        super(ErrorW, self).__init__()
        self.setWindowTitle("ERROR")
        
        self.label = QLabel("Usuari i contrasenya incorrecte! Torna a intentar.")

        self.boto = QPushButton("Aceptar")
        self.boto.clicked.connect(self.cerrar)

        self.layoutV = QVBoxLayout()
        self.layoutV.addWidget(self.label)
        self.layoutV.addWidget(self.boto)

        self.widget = QWidget()
        self.widget.setLayout(self.layoutV)
        self.setCentralWidget(self.widget)

    def cerrar(self):
        self.close()
        iniciar.show()

app = QApplication(sys.argv)
window = MainWindow()
iniciar = LoginWindow()
iniciar.show()
app.exec()