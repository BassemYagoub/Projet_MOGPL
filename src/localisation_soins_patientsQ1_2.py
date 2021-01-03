#Binome (GRP3) :
#Anthea RICHAUME
#Bassem YAGOUB

from gurobipy import *
import numpy as np
from func_utils import *

if __name__ == "__main__":
    #valeurs et constantes necessaires au PL
    dist_matrice, populations, noms_villes = importCSV('../ressources/villes.csv')
    
    k = 3
    alpha = 0.2
    villes_soins = [i for i in range(0, k)] #indice des villes choisies arbitrairement

    gamma = gamma_val(alpha, k, populations)
    print("gamma =", gamma, "\nalpha =", alpha,", k =", k)

    n = len(dist_matrice) #nb villes
    
    #sous-matrice n*k car le reste est inintéressant pour le PL
    dist_sous_matrice = dist_matrice[:, villes_soins]
    
    m = Model("localisation_soins")     
    
    # Declaration variables de decision
    x_temp = []
    for i in range(n):
        x_temp.append([])
        for j in range(k):
            x_temp[i].append(m.addVar(vtype=GRB.BINARY, lb=0, ub=1, name="x"+str(i+1)+","+str(j+1)))
    
    x = np.array(x_temp)

    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    obj = LinExpr();
    obj = 0
    for i in range(n):
        for j in range(k):
            obj += dist_sous_matrice[i][j] * x[i][j] * populations[i]
    obj /= sum(populations)
            
    # Definition de l'objectif
    m.setObjective(obj,GRB.MINIMIZE)
    
    # Definition des contraintes  
    for j in range(k):
        m.addConstr(np.dot(x[:,j], populations) <= gamma, "Contrainte%d" % (j))
    
    for i in range(n):
        m.addConstr(np.sum(x[i,:]) == 1, "Contrainte%d" % (k+i))
    
    # Resolution
    m.optimize()
    
    # Affichage
    displayResultQ1(k, n, x, y, noms_villes, villes_soins, m)

