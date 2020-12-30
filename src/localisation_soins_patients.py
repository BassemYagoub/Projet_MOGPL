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

    n = len(dist_matrice) #nb villes
    
    nbcont = k+n
    lignes = range(nbcont)
    
    nbvar = n*k
    colonnes = range(nbvar)
    
    #sous-matrice n*k car le reste est inintéressant pour le PL
    dist_sous_matrice = dist_matrice[:, :k]
    
    for row in dist_sous_matrice:
        print(row.tolist())
    print(populations,"\n")
    # Matrice des contraintes
    #Contrainte 1
    a = []
    for i in range(k):
        a.append([0]*nbvar)
        for j in range(n):
            a[i][j+(i*n)] = populations[j]
            
    
    #Contrainte 2 (= toute la sous matrice n*k)
    for i in range(n):
        a.append([0]*nbvar)
        for j in range(k):
            #i+k pour ne pas ecraser les k Contrainte1
            a[i+k][i+j*n] = 1
    
    for row in a:
        print(row)
    
    # Second membre
    b = [gamma]*k+[1]*(nbcont-k)
    print("SM\n", b)
    
    # Coefficients de la fonction objectif
    coefficients_dij = []
    for ville in villes_soins:
        coefficients_dij += dist_sous_matrice[:, ville:ville+1].flatten().tolist()
        
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
    for i in lignes:
        if(b[i] != 1):
            m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d " % i)
        else:
            m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) == b[i], "Contrainte%d " % i)
    
    # Resolution
    m.optimize()
    
                    
    print('\nSolution optimale:')
    for i in range(int(nbvar/k)):
        for j in range(k):
            print(int(x[i+(j*n)].x), end=' ')
        print("\n", end='')
        
    print('\nValeur de la fonction objectif :', m.objVal)
    
res = []
tmp = []
for i in range(n*k):
    tmp.append(x[i].x)
    if len(tmp)==n:
        res.append(tmp)
        tmp=[]

di=0
for i in range(len(res)):
    for j in range(len(res[0])):
        di+=dist_sous_matrice[j][i]*res[i][j]*populations[j]
di/=sum(populations)

print(di)
    
