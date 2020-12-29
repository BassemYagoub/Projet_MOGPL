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

    gamma = gamma_val(alpha, k, populations)
    print("gamma =", gamma, "\nalpha =", alpha,", k =", k)

    
    nbcont = len(dist_matrice)*2+1
    lignes = range(nbcont)
    
    nbvar = (len(dist_matrice)*len(dist_matrice))+len(dist_matrice)
    colonnes = range(nbvar)
    
    for row in dist_matrice:
        print(row.tolist())
    print(populations,"\n")
    
    # Matrice des contraintes
    #Contrainte 1
    a = []
    for i in range(len(dist_matrice)):
        a.append([0]*nbvar)
        for j in range(len(populations)):
            a[i][j+(i*len(dist_matrice))] = populations[j]
    
    
    #Contrainte 2 (= toute la matrice)
    for i in range(len(dist_matrice)):
        a.append([0]*nbvar)
        for j in range(len(dist_matrice)):
            #i+k pour ne pas ecraser les k Contrainte1
            a[i+len(dist_matrice)][i+j*len(dist_matrice)] = 1
    
    
    #Contrainte 3 yj = k
    a.append([0]*nbvar)
    for i in range(nbvar-len(dist_matrice), nbvar):
        print(i)
        a[nbcont-1][i] = 1
        
    
    for row in a:
        print(row)
    
    # Second membre
    b = [gamma]*len(dist_matrice)+[1]*len(dist_matrice)+[k]
    print("SM\n", b)
    
    # Coefficients de la fonction objectif
    coefficients_dij = dist_matrice.flatten().tolist()
    coefficients_dij += [0]*len(dist_matrice)
        
    print("COEFFS\n", coefficients_dij, "\n")
    
    c = coefficients_dij
    
    m = Model("localisation_soinsQ2_1")     
    
    # declaration variables de decision
    x = []
    for i in range(nbvar-len(dist_matrice)):
        x.append(m.addVar(vtype=GRB.BINARY, lb=0, ub=1, name="x"+str(i)))
    for j in range(len(dist_matrice)):
        x.append(m.addVar(vtype=GRB.BINARY, lb=0, ub=1, name="y"+str(j)))
    
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
        elif(cpt < len(lignes)-1):
            m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) == b[i], "Contrainte%d " % i)
        cpt+=1
    
    # Resolution
    m.optimize()
    
                    
    print('\nSolution optimale:')
    """
    for i in range(int(nbvar/k)):
        for j in range(k):
            print(int(x[i+(j*len(dist_matrice))].x), end=' ')
        print("\n", end='')
        
    print('\nValeur de la fonction objectif :', m.objVal/len(dist_matrice))
    
    res = []
    tmp = []
    for i in range(len(populations)*k):
        tmp.append(x[i].x)
        if len(tmp)==len(populations):
            res.append(tmp)
            tmp=[]
    
    di=0
    for i in range(len(res)):
        for j in range(len(res[0])):
            di+=dist_matrice[j][i]*res[i][j]*populations[j]
    di/=sum(populations)
    
    print(di)"""