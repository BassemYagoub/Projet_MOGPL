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
    n = 5    
    d = dist_matrice[:n]

    #Instances à tester
    #b = [150, 150, 25, 150, 25]
    #b = [90, 50, 130, 60, 150]
    b = [40, 160, 100, 80, 50]
    
    m = Model("equilibrage_uniteQ3_1")
    
    # declaration variables de decision
    x_temp = []
    for i in range(n):
        x_temp.append([])
        for j in range(n):
            x_temp[i].append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x"+str(i)+str(j)))
    
    x = np.array(x_temp)
    
    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    # definition de l'objectif
    obj = LinExpr();
    obj = 0
    for i in range(n):
        for j in range(n):
            obj += d[i][j] * x[i][j]

    m.setObjective(obj,GRB.MINIMIZE)
    
    #Definition des contraintes       
    for i in range(n):            
        m.addConstr(np.sum(x[i,:]) == b[i])
        
    for i in range(n):
        m.addConstr(np.sum(x[:,i]) <= 100)
            
    
    # Resolution
    m.optimize()
    
    print('\nValeur de la fonction objectif :', m.objVal)
            
    res=[]
    tmp=[]
    
    for i in range(n):
        for j in range(n):
            tmp.append(x[i][j].x)

        res.append(tmp)
        tmp=[]
    np.set_printoptions(edgeitems=15)
    res=np.asmatrix(res)
    
    print("Répartition des patients : ")
    print(res.T)
    
    