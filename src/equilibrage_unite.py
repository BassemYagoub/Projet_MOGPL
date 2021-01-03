#Binome :
#Anthea RICHAUME
#Bassem YAGOUB


from gurobipy import *
import numpy as np
from func_utils import *

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
    
    