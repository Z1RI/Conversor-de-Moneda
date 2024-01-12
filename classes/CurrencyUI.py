from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QComboBox, QLabel, QPushButton, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from lark import UnexpectedInput

from helpers.conversionRates import conversionRates
from helpers.exchangeRate import exchangeRate
from helpers.dates import dates
from styles.CurrencyAppStyles import currencyTextStyle, currencyText2Style, inputLineEditStyle, currencyComboStyle, resultLabelStyle

from classes.ConvertCurrency import convertCurrency

class CurrencyUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CONVERSOR DE DIVISAS')
        self.setGeometry(100, 100, 780, 280)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.setStyleSheet('background-color: #202124')

        # Boton de carga de archivos
        self.uploadButton = QPushButton('Subir archivo', self)
        self.uploadButton.clicked.connect(self.showFileDialog)
        
        # LAYOUTS
        mainLayout = QVBoxLayout()
        layout = QHBoxLayout()
        layoutCurrency = QVBoxLayout()
        layoutFrom = QHBoxLayout()
        layoutTo = QHBoxLayout()
        layoutText = QHBoxLayout()
        layoutUploadButton = QHBoxLayout()

        self.currencyText = QLabel('1 Dolar estadounidense es igual a')
        self.currencyText2 = QLabel('1 Dolar estadounidense')
        
        # Sección del gráfico y el select de moneda
        self.chartCanvas = FigureCanvas(plt.figure(figsize=(5, 7), facecolor='#202124', edgecolor='#81C995'))

        self.currencyCombo = QComboBox()
        self.currencyCombo.addItems([conversionRate for conversionRate in conversionRates.keys()])
        self.currencyCombo.currentIndexChanged.connect(self.updateChart)

        self.currencyCombo.currentIndexChanged.connect(self.changeCurrencyCombo)

        self.toCurrencyComboChart = QComboBox()
        self.toCurrencyComboChart.addItems([conversionRate for conversionRate in conversionRates.keys()])
        self.toCurrencyComboChart.currentIndexChanged.connect(self.updateChart)
        
        self.toCurrencyComboChart.currentIndexChanged.connect(self.changeCurrencyComboChart)

        # INPUT TEXT
        self.inputLineEdit = QLineEdit()
        self.inputLineEdit2 = QLineEdit()

        # INPUT TEXT DE SOLO LECTURA
        self.inputLineEdit2.setReadOnly(True)
        
        self.resultLabel = QLabel()
        
        self.inputLineEdit.textChanged.connect(self.showResult)

        # AGREGANDO ESTILOS A LOS WIDGETS Y LAYOUTS
        # LABELS
        self.currencyText.setStyleSheet(currencyTextStyle)
        self.currencyText2.setStyleSheet(currencyText2Style)
        self.resultLabel.setStyleSheet(resultLabelStyle)

        # INPUTS
        self.inputLineEdit.setStyleSheet(inputLineEditStyle)
        self.inputLineEdit2.setStyleSheet(inputLineEditStyle)

        # COMBOBOX
        self.currencyCombo.setStyleSheet(currencyComboStyle)
        self.toCurrencyComboChart.setStyleSheet(currencyComboStyle)

        # QFileDialog
        self.uploadButton.setStyleSheet('color: white')

        # AGREGANDO WIDGETS Y LAYOUTS A LAYOUTS 
        layoutFrom.addWidget(self.inputLineEdit)
        layoutFrom.addWidget(self.currencyCombo)
        layoutTo.addWidget(self.inputLineEdit2)
        layoutTo.addWidget(self.toCurrencyComboChart)

        layoutText.addWidget(self.currencyText)
        layoutText.addWidget(self.currencyText2)

        layoutCurrency.addLayout(layoutFrom)
        layoutCurrency.addLayout(layoutTo)

        layout.addLayout(layoutCurrency)
        layout.addWidget(self.chartCanvas)

        layoutUploadButton.addWidget(self.uploadButton)

        mainLayout.addLayout(layoutText)
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.resultLabel)
        mainLayout.addLayout(layoutUploadButton)

        self.centralWidget.setLayout(mainLayout)

        # FECHAS (EN ESTE CASO EN BASE A 5 DIAS)
        self.dates = dates

        # TASAS DE INTERCAMBIO
        self.currencyValues = exchangeRate

        self.updateChart()

    def showFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'Seleccionar un archivo', '', 'Archivos de texto (*.txt);;Todos los archivos (*)', options = options)

        if fileName:
            self.resultLabel.setText('Archivo cargado exitosamente: Resultados en el archivo resultTxt.txt')
            self.resultLabel.setStyleSheet('color: #61DC00; font-size: 16px; font-weight: bold')
            archivoTxt = open(fileName, 'r')
            resultTxt = open('resultTxt.txt', 'w')
            resultTxt.write('---------- RESULTADOS CONVERSIONES ---------- \n')

            for i in archivoTxt.read().split('\n'):
                try:
                    result = convertCurrency(i)        
                    resultToWrite = str(round(float(result.pretty().split()[-1]), 3))
                    resultTxt.write(f'{i} = {resultToWrite} {i.split(' ')[-1]} \n')

                except UnexpectedInput as e:
                    resultTxt.write('Entrada no válida \n')
                    print(f'Ocurrio un error durante el analisis sintactico: {e}')
                    continue

            archivoTxt.close()

    def changeCurrencyCombo(self):
        currencyComboValue = self.currencyCombo.currentText()
        toCurrencyComboChartValue = self.toCurrencyComboChart.currentText()
        conversion = conversionRates[currencyComboValue]["exchange"][toCurrencyComboChartValue]
        
        self.currencyText2.setText(f'{conversion} {conversionRates[toCurrencyComboChartValue]["currency"]}')
        self.currencyText.setText(f'1 {conversionRates[currencyComboValue]["currency"]} es igual a')
        self.inputLineEdit.setText('')

    def changeCurrencyComboChart(self):
        currencyComboValue = self.currencyCombo.currentText()
        toCurrencyComboChartValue = self.toCurrencyComboChart.currentText()
        conversion = conversionRates[currencyComboValue]["exchange"][toCurrencyComboChartValue]
        self.currencyText2.setText(f'{conversion} {conversionRates[toCurrencyComboChartValue]["currency"]}')
        self.inputLineEdit.setText('')

    def showResult(self):
        inputText = self.inputLineEdit.text()
        try:
            result = ''
            if(inputText == ''):
                result = convertCurrency(f'0 {self.currencyCombo.currentText()} to {self.toCurrencyComboChart.currentText()}')  
                print(f'----- ARBOL SINTACTICO ----- \n {result.pretty().center(28)}')
            
                resultToShow = str(round(float(result.pretty().split()[-1]), 3))
                self.inputLineEdit2.setText(resultToShow)
                self.resultLabel.setText('')
            else:
                try:
                    result = convertCurrency(f'{inputText} {self.currencyCombo.currentText()} to {self.toCurrencyComboChart.currentText()}')    
                
                    print(f'----- ARBOL SINTACTICO ----- \n {result.pretty().center(28)}')

                    resultToShow = str(round(float(result.pretty().split()[-1]), 3))
                    self.inputLineEdit2.setText(resultToShow)
                    self.resultLabel.setText('')

                except UnexpectedInput as e:
                    self.resultLabel.setStyleSheet('color: red; font-size: 16px; font-weight: bold')
                    self.resultLabel.setText('WARNING: Valor no valido ingresado')
                    self.inputLineEdit2.setText('')
                    print(f'Ocurrio un error durante el analisis sintactico: {e}')

        except Exception as e:
            print(f'Ocurrio un error al procesar la expresion: {e}')
            self.resultLabel.hasSelectedText('Error al procesar la expresion')
 
    # METODO PARA LA ACTUALIZACION DEL GRAFICO
    def updateChart(self):
        selectedCurrency = self.currencyCombo.currentText()
        toCurrency = self.toCurrencyComboChart.currentText()

        # VALORES DE LA TASA DE CAMBIO
        values = [value for value in self.currencyValues[selectedCurrency]['exchange'][toCurrency]]

        if values:
            currentExchangeRate = self.currencyValues[selectedCurrency]['exchange'][toCurrency]
            self.chartCanvas.figure.clear()
            ax = self.chartCanvas.figure.add_subplot(1, 1, 1)

            # ESTILOS AL FONDO DEL GRAFICO Y A LOS BORDES
            ax.set_facecolor('#202124')
            ax.spines['left'].set_color(None)  
            ax.spines['right'].set_color(None) 
            ax.spines['top'].set_color(None) 
            ax.spines['bottom'].set_color(None)

            # ESTILOS A LOS LABELS DEL GRAFICO
            ax.tick_params(axis='both', color='#5F6368', labelcolor='#5F6368')
            
            if currentExchangeRate[0] < currentExchangeRate[-1]:
                ax.plot(self.dates, values, marker='o', color='#81C995')
                ax.fill_between(self.dates, values, color='#394C41')
            elif currentExchangeRate[0] > currentExchangeRate[-1]:
                ax.plot(self.dates, values, marker='o', color='#E5847B')
                ax.fill_between(self.dates, values, color='#463435')
            else:
                ax.plot(self.dates, values, marker='o', color='#8A8A8A')
                ax.fill_between(self.dates, values, color='#393A3C')

            ax.set_xticks(self.dates)
            ax.set_xticklabels([d.strftime('%d-%b') for d in self.dates], color='#5F6368')
           
            # ESTILOS A LAS LINEAS HORIZONTALES DEL GRAFICO    
            ax.yaxis.grid(True, color='#2E3034', alpha=0.7)

            plt.subplots_adjust(bottom=0.4) 

            self.chartCanvas.draw()
