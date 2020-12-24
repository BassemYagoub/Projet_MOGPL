#Binome :
#Anthea RICHAUME
#Bassem YAGOUB

"""/!\ Le CSV a ete formate p/r a l'original"""

from gurobipy import *
import csv


if __name__ == "__main__":
    
    #matrice equivalente au csv
    dist_matrice = [ [ '-1' for i in range(16) ] for j in range(16) ]
    
    #dictionaire Ville : Population
    populations = {}
    
    #import csv
    i = 0
    with open('../ressources/villes.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            splitted_row = row[0].split(";")
            for j in range(0, len(splitted_row)-1):
                dist_matrice[i][j] = splitted_row[j]
                print(dist_matrice[i][j])
            i+= 1


for i in range(1, len(dist_matrice)):
    populations[dist_matrice[i][1]] = dist_matrice[i][0]


    
"""

#EXEMPLE GUROBI TME
-----------------------


nbcont=4 
nbvar=2

# Range of plants and warehouses
lignes = range(nbcont)
colonnes = range(nbvar)

# Matrice des contraintes
a = [[1,0],
     [0,1],
     [1,2],
     [2,1]]

# Second membre
b = [8, 6, 15, 18]

# Coefficients de la fonction objectif
c = [4, 10]

m = Model("mogplex")     
        
# declaration variables de decision
x = []
for i in colonnes:
    x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i+1)))

# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]
        
# definition de l'objectif
m.setObjective(obj,GRB.MAXIMIZE)

# Definition des contraintes
for i in lignes:
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)

# Resolution
m.optimize()


print("")                
print('Solution optimale:')
for j in colonnes:
    print('x%d'%(j+1), '=', x[j].x)
print("")
print('Valeur de la fonction objectif :', m.objVal)
"""
