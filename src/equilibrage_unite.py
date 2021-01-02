#Binome :
#Anthea RICHAUME
#Bassem YAGOUB

"""/!\ Le CSV a ete formate p/r a l'original"""

from gurobipy import *
import numpy as np

def importCSV(csv_name):
    """importe le csv d'un ensemble de villes et le retourne dans une matrice+vecteur"""
    dist_matrice = np.genfromtxt(csv_name, delimiter=';', dtype=int, filling_values=0)
    noms_villes = np.genfromtxt(csv_name, delimiter=';', dtype=str, filling_values=0)[0, 1:]
    populations = dist_matrice[1:, 0]
    #print(noms_villes)
    dist_matrice = dist_matrice[1:, 2:] #on enleve les nom de lignes/colonnes + la pop
    dist_matrice += dist_matrice.T      #on remplie les cases vides par symétrie
    
    return dist_matrice, populations, noms_villes


if __name__ == "__main__":
    #valeurs et constantes necessaires au PL
    dist_matrice, populations, noms_villes = importCSV('../ressources/villes.csv')
    
    # Matrice des coûts (distance entre unité i et unité j)
    d = dist_matrice[:5]
    n = 7
    b = [150, 150, 25, 150, 25]
    #b = [100, 100, 100, 100, 100]
    
    m = Model("equilibrage_uniteQ3_1")
    
    # declaration variables de decision
    x_temp = []
    ind = 0
    for i in range(5):
        x_temp.append([])
        for j in range(5):
            x_temp[i].append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x"+str(i)+str(j)))
            ind += 1
    
    x = np.array(x_temp)
    
    y_temp = []
    ind = 0
    for i in range(5):
        y_temp.append([])
        for j in range(5):
            y_temp[i].append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="y"+str(i)+str(j)))
            ind += 1
    
    y = np.array(y_temp)
    
    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    # definition de l'objectif
    obj = LinExpr();
    obj = 0
    for i in range(5):
        for j in range(5):
            obj += d[i][j] * x[i][j]

    m.setObjective(obj,GRB.MINIMIZE)
    
    #Definition des contraintes    
    for i in range(5):            
        m.addConstr(np.sum(x[i,:]) - np.sum(y[i,:]) == b[i])
        
    for i in range(5):
        m.addConstr(np.sum(y[i,:]) - np.sum(x[i,:]) == -100)
            
    
     # Resolution
    m.optimize()
    
    print('\nValeur de la fonction objectif :', m.objVal)
    
    for i in range(5):
        print('\n')
        for j in range(5):
            print(int(x[i][j].x), end=' ')
            
            
    for i in range(5):
        print('\n')
        for j in range(5):
            print(int(y[i][j].x), end=' ')
    
    