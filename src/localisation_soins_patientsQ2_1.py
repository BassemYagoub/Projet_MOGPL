#Binome (GRP3) :
#Anthea RICHAUME
#Bassem YAGOUB

from gurobipy import *
import numpy as np
from  func_utils import *

if __name__ == "__main__":
    #valeurs et constantes necessaires au PL
    dist_matrice, populations, noms_villes = importCSV('../ressources/villes.csv')
    
    k = 3
    alpha = 0.2

    gamma = gamma_val(alpha, k, populations)
    print("gamma =", gamma, "\nalpha =", alpha,", k =", k)

    n = len(dist_matrice)
    
    m = Model("localisation_soinsQ2_1")     
    
    # Declaration variables de decision
    x_temp = []
    for i in range(n):
        x_temp.append([])
        for j in range(n):
            x_temp[i].append(m.addVar(vtype=GRB.BINARY, lb=0, ub=1, name="x"+str(i+1)+","+str(j+1)))
    
    x = np.array(x_temp)
            
    y = []
    for j in range(n):
        y.append(m.addVar(vtype=GRB.BINARY, lb=0, ub=1, name="y"+str(j)))
    
    # maj du modele pour integrer les nouvelles variables
    m.update()
    
            
    # Definition de l'objectif
    obj = LinExpr();
    obj = 0
    for i in range(n):
        for j in range(n):
            obj += dist_matrice[i][j] * x[i][j] * populations[i]
    obj /= sum(populations)

    m.setObjective(obj,GRB.MINIMIZE)
    
    # Definition des contraintes  (de C1 à C3)
    for j in range(n):
        m.addConstr(np.dot(x[:,j], populations) <= (y[j]*gamma))
    
    for i in range(n):
        m.addConstr(np.sum(x[i,:]) == 1, "Contrainte%d" % (n+i))
        
    m.addConstr(np.sum(y) == k, "Contrainte%d" % (n+n+1)) 
    
    # Resolution
    m.optimize()
         
    # Affichage
    displayResultQ2(n, n, x, y, noms_villes, m, dist_matrice, True)
    