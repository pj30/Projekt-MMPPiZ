from pyscipopt import Model, quicksum, multidict
def mctransp(I, J, K, c, d, M):
     model = Model("multi-commodity transportation") # inicjacja modelu
     x = {}
     for i,j,k in c:
         x[i,j,k] = model.addVar(vtype="C", name="x[%s,%s,%s]" % (i, j, k)) # dodawanie zmiennych
     for i in I:
         for k in K:
             model.addCons(quicksum(x[i,j,k] for j in J if (i,j,k) in x) == d[i,k], "Demand[%s,%s]" % (i,k)) # ograniczenia na zapotrzebowanie
     for j in J:
         model.addCons(quicksum(x[i,j,k] for (i,j2,k) in x if j2 == j) <= M[j], "Capacity[%s]" % j) # ograniczenia na pojemność
     model.setObjective(quicksum(c[i,j,k]*x[i,j,k]  for i,j,k in x), sense = 'minimize') # funkcja celu
     model.data = x
     return model

J,M = multidict({1:3000, 2:3000, 3:3000}) # J -> lista magazynów, M -> pojemność
produce = {1:[2,4], 2:[1,2,3], 3:[2,3,4]} # produkty w danym magazynie
d = {(1,1):80,   (1,2):85,   (1,3):300,  (1,4):6,
     (2,1):270,  (2,2):160,  (2,3):400,  (2,4):7,
     (3,1):250,  (3,2):130,  (3,3):350,  (3,4):4,
     (4,1):160,  (4,2):60,   (4,3):200,  (4,4):3,
     (5,1):180,  (5,2):40,   (5,3):150,  (5,4):5
     } # zapotrzebowanie
I = set([i for (i,k) in d]) # lista klientów
K = set([k for (i,k) in d])
weight = {1:5, 2:2, 3:3, 4:4}
cost = {(1,1):4,  (1,2):6, (1,3):9,
        (2,1):5,  (2,2):4, (2,3):7,
        (3,1):6,  (3,2):3, (3,3):4,
        (4,1):8,  (4,2):5, (4,3):3,
        (5,1):10, (5,2):8, (5,3):4
        }
c = {}
for i in I:
    for j in J:
        for k in produce[j]:
            c[i, j, k] = cost[i,j] * weight[k] # koszt transportu z magazynu j do klienta i

model = mctransp(I, J, K, c, d, M) # model
model.optimize() # optymalizacja
EPS = 1.e-6
x = model.data
print("Optimal value:", model.getObjVal())
for i,j,k in x:
    if model.getVal(x[i,j,k]) > EPS:
        print("Wysylka %10g sztuk %3d z magazynu %3d do klienta %3d" % (model.getVal(x[i,j,k]), k, j, i))
