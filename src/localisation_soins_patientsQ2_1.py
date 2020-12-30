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
    print(noms_villes)
    dist_matrice = dist_matrice[1:, 2:] #on enleve les nom de lignes/colonnes + la pop
    dist_matrice += dist_matrice.T      #on remplie les cases vides par symétrie
    
    return dist_matrice, populations, noms_villes


def gamma_val(alpha, k, populations):
    """retourne la valeur gamma a partir d'alpha, k et le vecteur de population/ville"""    
    #print(((1+alpha)/k), sum(populations.values()))
    return ((1+alpha)/k) * (populations.sum())



if __name__ == "__main__":
    #valeurs et constantes necessaires au PL
    dist_matrice, populations, noms_villes = importCSV('../ressources/villes.csv')
    
    k = 3
    alpha = 0.2

    gamma = gamma_val(alpha, k, populations)
    print("gamma =", gamma, "\nalpha =", alpha,", k =", k)

    n = len(dist_matrice)
    
    for row in dist_matrice:
        print(row.tolist())
    print(populations,"\n")
    
    m = Model("localisation_soinsQ2_1")     
    
    # declaration variables de decision
    x_temp = []
    ind = 0
    for i in range(n):
        x_temp.append([])
        for j in range(n):
            x_temp[i].append(m.addVar(vtype=GRB.BINARY, lb=0, ub=1, name="x"+str(ind)))
            ind += 1
    
    x = np.array(x_temp)
            
    y = []
    for j in range(n):
        y.append(m.addVar(vtype=GRB.BINARY, lb=0, ub=1, name="y"+str(j)))
    
    # maj du modele pour integrer les nouvelles variables
    m.update()
    
            
    # definition de l'objectif
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
        m.addConstr(np.sum(x[i,:]) == 1, "Contrainte%d" % (k+i))
        
    m.addConstr(np.sum(y) == k) 
    
    # Resolution
    m.optimize()
    
             
    print('\Affectation optimale:\n')
    for j in range(n):
        if(int(y[j].x) == 1):
            print("Secteur",noms_villes[j+1], end=':\n\t')
            for i in range(n):
                if(int(x[:, j][i].x)) == 1:
                    print(noms_villes[i+1], end=', ')
            print("\n")
    
    print('\nValeur de la fonction objectif :', m.objVal)
    