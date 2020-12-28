#Binome :
#Anthea RICHAUME
#Bassem YAGOUB

"""/!\ Le CSV a ete formate p/r a l'original"""

from gurobipy import *
import numpy as np

def importCSV(csv_name):
    """importe le csv d'un ensemble de villes et le retourne dans une matrice+vecteur"""
    dist_matrice = np.genfromtxt(csv_name, delimiter=';', dtype=int, filling_values=0)
    populations = dist_matrice[1:, 0]
    
    dist_matrice = dist_matrice[1:, 2:] #on enleve les nom de lignes/colonnes + la pop
    dist_matrice += dist_matrice.T      #on remplie les cases vides par symétrie
    
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
    alpha = 0.2
    villes_soins = [i for i in range(0, k)] #indice des villes choisies arbitrairement

    gamma = gamma_val(alpha, k, populations)
    print("gamma =", gamma, "\nalpha =", alpha,", k =", k)

    
    nbcont = k+len(dist_matrice)
    lignes = range(nbcont)
    
    nbvar = len(dist_matrice)*k
    colonnes = range(nbvar)
    
    #sous-matrice n*k car le reste est inintéressant pour le PL
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
            
    
    #Contrainte 2 (= toute la sous matrice n*k)
    for i in range(len(dist_sous_matrice)):
        a.append([0]*nbvar)
        for j in range(k):
            #i+k pour ne pas ecraser les k Contrainte1
            a[i+k][i+j*len(dist_sous_matrice)] = 1
    
    for row in a:
        print(row)
    
    # Second membre
    b = [gamma]*k+[1]*(nbcont-k)
    print("SM\n", b)
    
    # Coefficients de la fonction objectif
    #coefficients_dij = np.matrix(dist_sous_matrice).getA1()
    coefficients_dij = []
    for i in range(len(dist_sous_matrice)):
        for j in villes_soins:
            coefficients_dij.append(dist_sous_matrice[i][j])
        
    print("COEFFS\n", coefficients_dij, "\n")
    
    c = coefficients_dij
    
    
    m = Model("localisation_soins")     
    
    
    # declaration variables de decision
    x = []
    for i in range(nbvar):
        x.append(m.addVar(vtype=GRB.BINARY, lb=0, ub=1, name="x"+str(i)))

    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    obj = LinExpr();
    obj = 0
    for j in colonnes:
        obj += c[j] * x[j]
            
    # definition de l'objectif
    m.setObjective(obj,GRB.MINIMIZE)
    
    # Definition des contraintes  
    cpt = 0
    for i in lignes:
        if(cpt < k):
            m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d " % i)
        else:
            m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) == b[i], "Contrainte%d " % i)
        cpt+=1
    
    # Resolution
    m.optimize()
    
                    
    print('\nSolution optimale:')
    for j in colonnes:
        print('x%d'%(j+1), '=', x[j].x)
    print('\nValeur de la fonction objectif :', m.objVal/len(dist_sous_matrice))
    
