from pyscipopt import Model, quicksum, multidict
import pandas as pd

################################
# I - sklep , J - magazyn , K - typ produktu
#MODEL
def mctransp(I, J, K, c, d, M):
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
def load_data(file_name, sheet_name):

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

def solve():
    file_name = 'Database.xlsx'

    # OGRANICZENIA

    # Ilosc sztuk danego produktow K (wszystkich) w J magazynie
    #J,M = multidict({'Magazyn 1': 3000, 'Magazyn 2': 3000, 'Magazyn 3':3000})
    J,M = multidict(load_data(file_name, 'PojemnoscMagazynu'))
    # Jakie produkty sa dostepne w J magazynie
    produkt = load_data(file_name, 'DostepnoscProduktowWMagazynach')
    print(produkt)

    # Zapotrzebowanie J klienta na K produktu
    d = load_data(file_name, 'Zapotrzebowanie')

    # Lista sklepow
    I = set([i for (i,k) in d])

    # Lista produktow
    K = set([k for (i,k) in d])
    print(produkt)
    # Wagi produktow
    waga = load_data(file_name, 'WagaProduktu')

    # Koszt transportu
    koszt = load_data(file_name, 'Koszt')

    # Koszt dotarcia z J magazynu do M sklepu
    c = {}
    for i in I:
        for j in J:
            for k in produkt[j]:
                c[i, j, k] = koszt[i,j] * waga[k] # Koszt*waga transportu z magazynu j do klienta i produktu k

    # Model
    model = mctransp(I, J, K, c, d, M)

    # Optymalizacja
    model.optimize()

    EPS = 1.e-6
    x = model.data
    resultAsList = []
    print("Ogolny koszt transportu wynosi:", model.getObjVal())
    for i,j,k in x:
        if model.getVal(x[i,j,k]) > EPS:
            print("Wysylka %10g sztuk %3s z magazynu %3s do klienta %3s" % (model.getVal(x[i,j,k]), k, j, i))
            resultAsList.append([i, j, k, model.getVal(x[i,j,k])])

    return model.getObjVal(), resultAsList

def getRawData(file_name, sheet_name):
    dataFrame = pd.read_excel(file_name, sheet_name)
    for columnName in list(dataFrame.columns.values):
        dataFrame[columnName] = dataFrame[columnName].astype(str)
    return dataFrame.values.tolist()
