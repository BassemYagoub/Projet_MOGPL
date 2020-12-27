#Binome :
#Anthea RICHAUME
#Bassem YAGOUB

"""/!\ Le CSV a ete formate p/r a l'original"""

from gurobipy import *
import csv
import math
import numpy as np
import pandas

def importCSV(csv_name):
    """importe le csv d'un ensemble de villes et le retourne dans une matrice+vecteur"""
    dist_matrice = np.genfromtxt(csv_name, delimiter=';', dtype=int, filling_values=0)
    populations = dist_matrice[1:, 0]
    
    dist_matrice = dist_matrice[1:, 2:]
    dist_matrice += dist_matrice.T
    
    return dist_matrice, populations


def gamma_val(alpha, k, populations):
    """retourne la valeur gamma a partir d'alpha, k et le vecteur de population/ville"""    
    #print(((1+alpha)/k), sum(populations.values()))
    return ((1+alpha)/k) * (populations.sum())



if __name__ == "__main__":
    #valeurs et constantes necessaires au PL
    dist_matrice, populations = importCSV('../ressources/villes.csv')
    #print(dist_matrice.tolist(), populations.tolist())
    
    k = 3
    alpha = 0.1
    villes_soins = [i for i in range(0, k)] #indice des villes choisies arbitrairement

    gamma = gamma_val(alpha, k, populations)
    print("gamma =", gamma, "\nalpha =", alpha,", k =", k)

    
    nbcont = k+len(dist_matrice)
    lignes = range(nbcont)
    
    nbvar = len(dist_matrice)*k
    colonnes = range(nbvar)

    dist_sous_matrice = dist_matrice[:, :k]
    
    # Matrice des contraintes
    #Contrainte 1
    a = []
    incr = 0
    for i in range(k):
        a.append([0]*nbvar)
        for j in range(len(populations)):
            a[i][j+incr] = populations[j]
        incr += len(dist_sous_matrice)
            
    # #Contrainte 2 (= toute la sous matrice n*k)
    # cpt = 0
    # for i in range(k, len(dist_sous_matrice)):
    #     a.append([0]*nbvar)
    #     for j in range(k):
    #         a[i][i+j*len(dist_sous_matrice)] = 1
    #         #cpt+= 1
    
    #Contrainte 2 (= toute la sous matrice n*k)
    cpt = 0
    for i in range(len(dist_sous_matrice)):
        a.append([0]*nbvar)
        for j in range(k):
            a[i][i+j*len(dist_sous_matrice)] = 1
            #cpt+= 1

    for row in a:
        print(row)
    
    # Second membre
    b = [gamma]*k+[1]*(nbcont-k)
    
    # Coefficients de la fonction objectif
    #coefficients_dij = np.matrix(dist_sous_matrice).getA1()
    coefficients_dij = []
    for i in range(len(dist_sous_matrice)):
        for j in villes_soins:
            coefficients_dij.append(dist_sous_matrice[i][j])
        
    print(coefficients_dij)
    
    c = coefficients_dij
    
    
    m = Model("localisation_soins")     
    
    
    # declaration variables de decision
    x = []
    for i in range(len(dist_sous_matrice)):
        for j in range(len(dist_sous_matrice[i])):
            #print(i, "x"+str(i)+str(j-1), dist_matrice[i][j])
            x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x"+str(i)+str(j)))

    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    obj = LinExpr();
    obj = 0
    for j in colonnes:
        obj += c[j] * x[j]
            
    # definition de l'objectif
    m.setObjective(obj,GRB.MINIMIZE)
    
    # Definition des contraintes  
        
    for i in lignes:
        m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) == b[i], "Contrainte%d " % i)
    
    # Resolution
    m.optimize()
    
                    
    print('\nSolution optimale:')
    for j in colonnes:
        print('x%d'%(j+1), '=', x[j].x)
    print('\nValeur de la fonction objectif :', m.objVal)
    
    
    
    
    
    """
    #calcul des coefficients (dij)
    coefficients_dij = []
    for i in range(1, len(dist_matrice)):
        for j in range(2, len(dist_matrice[i])):
            coefficients_dij.append(int(dist_matrice[i][j]))

    
    nbcont=k+len(dist_matrice)
    lignes = range(nbcont)
    
    nbvar=len(dist_matrice)*k
    colonnes = range(nbvar)

    # Matrice des contraintes
    a = [
         [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
         [1,5,1,0,0,0,0,0,0,0,0,0,0,0,0],
         [1,4,1,0,0,0,0,0,0,0,0,0,0,0,0],
         ]

    contraintes1 = [ [0 for _ in range(len(dist_matrice[0])-2)] for _ in range(len(dist_matrice)-1)]
    for i in range(len(contraintes1)):
        for j in range(len(contraintes1[i])):
            if(j in villes_soins):
                contraintes1[i][j] = populations
                
    contraintes2 = [ [0 for _ in range(len(dist_matrice[0])-2)] for _ in range(len(dist_matrice)-1)]
    i = np.where(contrainte2 in villes_soin)
    for i in range(len(contraintes2)):
        for j in range(len(contraintes2[i])):
            if(j in villes_soins):
                contraintes2[i][j] = 1
            
        
    a = a+contraintes2
    for row in a:
        #print(row)
            
          
    a.append([1 for _ in range(k)])
    
    # Second membre
    b = [gamma, 1, 1]
    
    # Coefficients de la fonction objectif
    c = coefficients_dij
    
    
    m = Model("localisation_soins")     
   
    
    # declaration variables de decision
    x = []
    for i in range(1, len(dist_matrice)):
        for j in range(2, len(dist_matrice[i])):
            #print(i, "x"+str(i)+str(j-1), dist_matrice[i][j])
            x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x"+str(i)+str(j-1)))

    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    obj = LinExpr();
    obj = 0
    for j in colonnes:
        obj += c[j] * x[j]
            
    # definition de l'objectif
    m.setObjective(obj,GRB.MINIMIZE)
    
    # Definition des contraintes
    for i in lignes:
        m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte ", i)
    
    # Resolution
    m.optimize()
    
                    
    print('\nSolution optimale:')
    for j in colonnes:
        print('x%d'%(j+1), '=', x[j].x)
    print('\nValeur de la fonction objectif :', m.objVal)
"""