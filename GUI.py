#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from pyscipopt import Model, quicksum, multidict
import pandas as pd



class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 605, 480)
        self.setWindowTitle('Modele matematyczne procesow, podobienstwo i zmiana skali')
        self.file_name = 'Database.xlsx'
        self.produkt = self.load_data(self.file_name, 'DostepnoscProduktowWMagazynach')
        self.pojemnosc = self.load_data(self.file_name, 'PojemnoscMagazynu')
        self.d = self.load_data(self.file_name, 'Zapotrzebowanie')
        self.koszt = self.load_data(self.file_name, 'Koszt')
        self.waga = self.load_data(self.file_name, 'WagaProduktu')
        self.run()

    def file_open(self):
        # need to make name an tupple otherwise i had an error and app crashed
        name = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', options=QtGui.QFileDialog.DontUseNativeDialog))
        print(str(name), 'ł')
        self.produkt = self.load_data(name, 'DostepnoscProduktowWMagazynach')
        self.pojemnosc = self.load_data(name, 'PojemnoscMagazynu')
        self.d = self.load_data(name, 'Zapotrzebowanie')
        self.koszt = self.load_data(name, 'Koszt')
        self.waga = self.load_data(name, 'WagaProduktu')
        #self.editor()
        self.repaint()
        self.run()

    def prnt(self):
        print(self.pojemnosc)

    def run(self):
        btn = QtGui.QPushButton('Run', self)
        btn.clicked.connect(self.solve)
        btn.resize(50, 40)
        btn.move(5, 5)
        btn.setIcon(QtGui.QIcon('./iconfinder_button-play_basic_green_69646.png'))
        """
        btn1 = QtGui.QPushButton('Open', self)
        btn1.clicked.connect(self.file_open)
        btn1.resize(60, 40)
        btn1.move(60, 5)
        btn1.setIcon(QtGui.QIcon('./iconfinder_folder_basic_blue_69500.png'))


        openFile = QtGui.QAction('&Open File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')

        fileMenu.addAction(openFile)
        """
        label = QtGui.QLabel(self)
        label.setText("Dostepnosc produktow w poszczegolnych magazynach")
        label.resize(280, 40)
        label.move(5, 40)
        tabela_produktu 	= QtGui.QTableWidget(self)
        tableItem 	= QtGui.QTableWidgetItem()

# initiate table
        tabela_produktu.resize(280, 115)
        tabela_produktu.move(5, 70)
        tabela_produktu.setRowCount(len(self.produkt))
        tabela_produktu.setColumnCount(2)
        tabela_produktu.setHorizontalHeaderLabels(['Magazyn', 'Produkty'])
        header = tabela_produktu.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        row = 0

        for i in self.produkt:
            tabela_produktu.setItem(row,0, QtGui.QTableWidgetItem(str(i)))
            tabela_produktu.setItem(row,1, QtGui.QTableWidgetItem(str(self.produkt[i]).replace("[", "").replace("]", "").replace("'", "")))
            row += 1

        label1 = QtGui.QLabel(self)
        label1.setText("Pojemnosc magazynow")
        label1.resize(280, 40)
        label1.move(5, 180)
        tabela_pojemnosci 	= QtGui.QTableWidget(self)
        tableItem 	= QtGui.QTableWidgetItem()

        # initiate table
        tabela_pojemnosci.resize(280, 115)
        tabela_pojemnosci.move(5, 210)
        tabela_pojemnosci.setRowCount(len(self.pojemnosc))
        tabela_pojemnosci.setColumnCount(2)
        tabela_pojemnosci.setHorizontalHeaderLabels(['Magazyn', 'Pojemnosc'])
        header = tabela_pojemnosci.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        row = 0
        for i in self.pojemnosc:
            tabela_pojemnosci.setItem(row,0, QtGui.QTableWidgetItem(str(i)))
            tabela_pojemnosci.setItem(row,1, QtGui.QTableWidgetItem(str(self.pojemnosc[i]).replace("[", "").replace("]", "").replace("'", "")))
            row += 1

        label2 = QtGui.QLabel(self)
        label2.setText("Zapotrzebowanie na produkty w sklepach")
        label2.resize(280, 40)
        label2.move(5, 320)
        tabela_zapotrzebowan 	= QtGui.QTableWidget(self)
        tableItem 	= QtGui.QTableWidgetItem()

        # initiate table
        tabela_zapotrzebowan.resize(280, 115)
        tabela_zapotrzebowan.move(5, 350)
        tabela_zapotrzebowan.setRowCount(len(self.d))
        tabela_zapotrzebowan.setColumnCount(3)
        tabela_zapotrzebowan.setHorizontalHeaderLabels(['Sklep', 'Produkt', 'Zapotrzebowanie'])
        header = tabela_zapotrzebowan.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        row = 0
        for i in self.d:
            tabela_zapotrzebowan.setItem(row,0, QtGui.QTableWidgetItem(str(i[0])))
            tabela_zapotrzebowan.setItem(row,1, QtGui.QTableWidgetItem(str(i[1])))
            tabela_zapotrzebowan.setItem(row,2, QtGui.QTableWidgetItem(str(self.d[i])))
            row += 1

        label3 = QtGui.QLabel(self)
        label3.setText("Koszt polaczenia miedzy sklepem, a magazynem")
        label3.resize(280, 40)
        label3.move(320, 40)
        tabela_kosztow 	= QtGui.QTableWidget(self)
        tableItem 	= QtGui.QTableWidgetItem()

        # initiate table
        tabela_kosztow.resize(280, 115)
        tabela_kosztow.move(320, 70)
        tabela_kosztow.setRowCount(len(self.koszt))
        tabela_kosztow.setColumnCount(3)
        tabela_kosztow.setHorizontalHeaderLabels(['Sklep', 'Magazyn', 'Koszt'])
        header = tabela_kosztow.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        row = 0
        for i in self.koszt:
            tabela_kosztow.setItem(row,0, QtGui.QTableWidgetItem(str(i[0])))
            tabela_kosztow.setItem(row,1, QtGui.QTableWidgetItem(str(i[1])))
            tabela_kosztow.setItem(row,2, QtGui.QTableWidgetItem(str(self.koszt[i])))
            row += 1

        label4 = QtGui.QLabel(self)
        label4.setText("Waga produktow")
        label4.resize(280, 40)
        label4.move(320, 180)
        tabela_wag 	= QtGui.QTableWidget(self)
        tableItem 	= QtGui.QTableWidgetItem()

        # initiate table
        tabela_wag.resize(280, 115)
        tabela_wag.move(320, 210)
        tabela_wag.setRowCount(len(self.waga))
        tabela_wag.setColumnCount(2)
        tabela_wag.setHorizontalHeaderLabels(['Produkt', 'Waga'])
        header = tabela_wag.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        row = 0
        for i in self.waga:
            tabela_wag.setItem(row,0, QtGui.QTableWidgetItem(str(i)))
            tabela_wag.setItem(row,1, QtGui.QTableWidgetItem(str(self.waga[i])))
            row += 1

# Set window size.
        self.show()

################################
# I - sklep , J - magazyn , K - typ produktu
#MODEL
    def mctransp(self, I, J, K, c, d, M):
         model = Model("multi-commodity transportation") # inicjacja modelu
         x = {}
         for i,j,k in c:
             x[i,j,k] = model.addVar(vtype="C", name="x[%s,%s,%s]" % (i, j, k)) # dodawanie zmiennych
         for i in I:
             for k in K:
                 model.addCons(quicksum(x[i,j,k] for j in J if (i,j,k) in x) == d[i,k], "Popyt[%s,%s]" % (i,k)) # ograniczenia na zapotrzebowanie
         for j in J:
             model.addCons(quicksum(x[i,j,k] for (i,j2,k) in x if j2 == j) <= M[j], "Pojemnosc[%s]" % j) # ograniczenia na pojemnosc
         model.setObjective(quicksum(c[i,j,k]*x[i,j,k]  for i,j,k in x), sense = 'minimize') # funkcja celu
         model.data = x
         return model

################################
    def load_data(self, file_name, sheet_name):

        data = pd.read_excel(file_name, sheet_name)
        dict = {}

        if sheet_name in ['DostepnoscProduktowWMagazynach']:
            for index, row in data.iterrows():
                dict[str(row[0])] = str(row[1]).split(", ")
        elif sheet_name in ['WagaProduktu', 'PojemnoscMagazynu']:
            for index, row in data.iterrows():
                dict[str(row[0])] = int(row[1])
        elif sheet_name in ['Zapotrzebowanie', 'Koszt']:
            for index, row in data.iterrows():
                dict[str(row[0]), str(row[1])] = int(row[2])
        else:
            print('Bledna nazwa arkusza!')

        return dict

    def solve(self):
        self.file_name = 'Database.xlsx'

        # OGRANICZENIA

        # Ilosc sztuk danego produktow K (wszystkich) w J magazynie
        #J,M = multidict({'Magazyn 1': 3000, 'Magazyn 2': 3000, 'Magazyn 3':3000})
        J,M = multidict(self.pojemnosc)
        # Jakie produkty sa dostepne w J magazynie
        #produkt = self.load_data(file_name, 'DostepnoscProduktowWMagazynach')

        # Zapotrzebowanie J klienta na K produktu


        # Lista sklepow
        I = set([i for (i,k) in self.d])

        # Lista produktow
        K = set([k for (i,k) in self.d])
        # Wagi produktow

        # Koszt transportu


        # Koszt dotarcia z J magazynu do M sklepu
        c = {}
        for i in I:
            for j in J:
                for k in self.produkt[j]:
                    c[i, j, k] = self.koszt[i,j] * self.waga[k] # Koszt*waga transportu z magazynu j do klienta i produktu k

        # Model
        model = self.mctransp(I, J, K, c, self.d, M)

        # Optymalizacja
        model.optimize()

        EPS = 1.e-6
        x = model.data

        self.w1 = QtGui.QWidget()
        self.w1.setWindowTitle('Wyniki')
        self.w1.resize(455, 380)
        self.objective = QtGui.QLabel(self.w1)
        self.objective.setText("Ogolny koszt transportu wynosi: " + str(model.getObjVal()))
        self.objective.resize(450, 50)
        self.objective.move(5, 5)
        self.objective.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        result_table = QtGui.QTableWidget(self.w1)
        tableItem = QtGui.QTableWidgetItem()
# initiate table
        result_table.setWindowTitle("QTableWidget Example @pythonspot.com")
        result_table.resize(445, 320)
        result_table.move(5, 50)
        result_table.setRowCount(len(x))
        result_table.setColumnCount(4)
        #result_table.setModel(model1)
        result_table.setHorizontalHeaderLabels(['Wysylka', 'produktu', 'z magazynu', 'do klienta'])
        row = 0
        for i,j,k in x:
            #if model.getVal(x[i,j,k]) > EPS:
            result_table.setItem(row, 0, QtGui.QTableWidgetItem(str(model.getVal(x[i,j,k])) + ' sztuk'))
            result_table.setItem(row, 1, QtGui.QTableWidgetItem(str(k)))
            result_table.setItem(row, 2, QtGui.QTableWidgetItem(str(j)))
            result_table.setItem(row, 3, QtGui.QTableWidgetItem(str(i)))
            row += 1
        self.w1.show()
        #retval = msg.exec_()

app = QtGui.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())
