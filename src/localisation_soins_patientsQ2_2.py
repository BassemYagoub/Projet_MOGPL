#Binome (GRP3) :
#Anthea RICHAUME
#Bassem YAGOUB

"""/!\ Le CSV a ete formate p/r a l'original"""

from gurobipy import *
import numpy as np
import func_utils

if __name__ == "__main__":
    #valeurs et constantes necessaires au PL
    dist_matrice, populations, noms_villes = importCSV('../ressources/villes.csv')
    
    k = 5
    alpha = 0.2

    gamma = gamma_val(alpha, k, populations)
    print("gamma =", gamma, "\nalpha =", alpha,", k =", k)

    n = len(dist_matrice)
    
    m = Model("localisation_soinsQ2_2")     
    
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
        
    max_d_vi_fi = m.addVar(vtype=GRB.INTEGER, lb=0, name="max_d_vi_fi")
    
    # maj du modele pour integrer les nouvelles variables
    m.update()
    
            
    # Definition de l'objectif
    obj = LinExpr();
    obj = max_d_vi_fi

    m.setObjective(obj,GRB.MINIMIZE)
    
    # Definition des contraintes  (de C1 à C4)
    for j in range(n):
        m.addConstr(np.dot(x[:,j], populations) <= (y[j]*gamma), "Contrainte%d" % (j))
    
    for i in range(n):
        m.addConstr(np.sum(x[i,:]) == 1, "Contrainte%d" % (k+i))
    
    
    for i in range(n):
        print(max(dist_matrice[i, :]))
    
    ind = 0
    for i in range(n):
        for j in range(n):
            m.addConstr(dist_matrice[i][j] * x[i][j] <= max_d_vi_fi, "Contrainte%d" % (n*2+ind))
            ind+=1
        
    m.addConstr(np.sum(y) == k, "Contrainte%d" % (n*3+ind+1)) 
    
    # Resolution
    m.optimize()
    
    # Affichage
    displayResultQ2(n, n, x, y, noms_villes, m, dist_matrice, False)
    