#Binome :
#Anthea RICHAUME
#Bassem YAGOUB

"""/!\ Le CSV a ete formate p/r a l'original"""

from gurobipy import *
import csv


def importCSV(csv_name):
    """importe le csv d'un ensemble de ville et le retourne dans une matrice+dict"""
    
    #import csv
    i = 0
    with open(csv_name, newline='') as csvfile:
        #matrice equivalente au csv
        dist_matrice = [ [ '-1' for i in range(16) ] for j in range(16) ]
        
        #dictionaire Ville : Population vi
        populations = {}
    
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            splitted_row = row[0].split(";")
            for j in range(0, len(splitted_row)-1):
                if(splitted_row[j] != ""):
                    dist_matrice[i][j] = splitted_row[j]
                print(dist_matrice[i][j])
            i+= 1

    
    for i in range(1, len(dist_matrice)):
        populations[dist_matrice[i][1]] = int(dist_matrice[i][0])
    
    return dist_matrice, populations
        
        
def gamma_val(alpha, k, populations):
    """retourne la valeur gamma a partir d'alpha, k et le vecteur de population/ville"""    
    print(((1+alpha)/k), sum(populations.values()))
    return ((1+alpha)/k) * (sum(populations.values()))



if __name__ == "__main__":
    dist_matrice, populations = importCSV('../ressources/villes.csv')
    k = 3
    alpha = 0.1
    gamma = gamma_val(alpha, k, populations)
    print("gamma = ", gamma, "alpha = ", alpha,", k = ", k)
    
    #calcul des coefficients (dij)
    coefficients_dij = []
    for i in range(1, len(dist_matrice)):
        print("--------------------------------")
        for j in range(2, len(dist_matrice[i])):
            if(dist_matrice[i][j] != "-1" and dist_matrice[i][j] != "0"):
                coefficients_dij = dist_matrice[i][j]
    
    nbcont=2 
    lignes = range(nbcont)
    
    nbvar=len(dist_matrice)*len(dist_matrice[0]) #x1,1 a x15,15
    colonnes = range(nbvar)
    
    # Matrice des contraintes
    a = [[1,0],
         [0,1],
         [1,2],
         [2,1]]
    
    # Second membre
    b = [gamma, 1]
    
    # Coefficients de la fonction objectif
    c = coefficients_dij
    
    m = Model("localisation_soins")     
"""           
    # declaration variables de decision
    x = []
    for i in colonnes:
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i+1)))
    
    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    obj = LinExpr();
    obj =0
    for j in colonnes:
        obj += c[j] * x[j]
            
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    
    # Definition des contraintes
    for i in lignes:
        m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
    
    # Resolution
    m.optimize()
    
    
    print("")                
    print('Solution optimale:')
    for j in colonnes:
        print('x%d'%(j+1), '=', x[j].x)
    print("")
    print('Valeur de la fonction objectif :', m.objVal)
"""