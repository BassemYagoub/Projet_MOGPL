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
    
    k = 3
    alpha = 0.2

    gamma = gamma_val(alpha, k, populations)
    print("gamma =", gamma, "\nalpha =", alpha,", k =", k)

    n = len(dist_matrice)
    nbcont = len(dist_matrice)*2+1
    lignes = range(nbcont)
    
    nbvar = (n*n)+n
    colonnes = range(nbvar)
    
    for row in dist_matrice:
        print(row.tolist())
    print(populations,"\n")

    # Second membre
    b = [gamma]*n+[1]*n+[k]
    print("SM\n", b)
    
    # Coefficients de la fonction objectif
    coefficients_dij = dist_matrice.flatten().tolist()
    coefficients_dij += [0]*n
        
    print("COEFFS\n", coefficients_dij, "\n")
    
    c = coefficients_dij
    
    m = Model("localisation_soinsQ2_1")     
    
    # declaration variables de decision
    x_temp = []
    for i in range(n):
        x_temp.append([])
        for j in range(n):
            x_temp[i].append(m.addVar(vtype=GRB.BINARY, lb=0, ub=1, name="x"+str(i)))
    
    x = np.array(x_temp)
            
    y = []
    for j in range(n):
        y.append(m.addVar(vtype=GRB.BINARY, lb=0, ub=1, name="y"+str(j)))
    
    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    obj = LinExpr();
    obj = 0
    cpt=0
    for i in range(n):
        for j in range(n):
            obj += c[cpt] * x[i][j]
            cpt+=1
            
    for j in range(n):
        obj += c[cpt] * y[j]
        cpt+=1
            
    # definition de l'objectif
    m.setObjective(obj,GRB.MINIMIZE)
    
    # Definition des contraintes  
    
    m.addConstr(np.sum(y) == k)
    for j in range(n):
        m.addConstr(np.dot(x[:,j], populations) <= (y[j]*((1+alpha)/k)*np.sum(populations)))
    
    for i in range(n):
        m.addConstr(np.sum(x[i,:]) == 1, "Contrainte%d" % (k+i))
    
    # Resolution
    m.optimize()
    
             
    print('\nSolution optimale:')
    
    for i in range(n):
        for j in range(n):
            print(int(x[i][j].x), end=' ')
        print("\n", end='')
    
    print("y :")
    for j in range(n):
        print(int(y[j].x), end=' ')
    
    print('\nValeur de la fonction objectif :', m.objVal)
    
    res = []
    tmp = []
    for i in range(n):
        for j in range(n):
            tmp.append(x[i][j].x)
            if len(tmp)==len(populations):
                res.append(tmp)
                tmp=[]
    
    di=0
    for i in range(len(res)):
        for j in range(len(res[0])):
            di+=dist_matrice[j][i]*res[i][j]*populations[j]
    di/=sum(populations)
    print(di)