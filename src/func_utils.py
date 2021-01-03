#Binome (GRP3) :
#Anthea RICHAUME
#Bassem YAGOUB
import numpy as np

"""/!\ Le CSV a ete formate p/r a l'original"""

def importCSV(csv_name):
    """importe le csv d'un ensemble de villes et le divise en 3 ensembles
       une matrice des distances, un vecteur de populations et un vecteur de noms de villes
    """
    #division du csv en 3 listes differentes
    dist_matrice = np.genfromtxt(csv_name, delimiter=';', dtype=int, filling_values=0)
    noms_villes = np.genfromtxt(csv_name, delimiter=';', dtype=str, filling_values=0)[0, 1:]
    populations = dist_matrice[1:, 0]
    
    dist_matrice = dist_matrice[1:, 2:] #on enleve les nom de lignes/colonnes + la pop
    dist_matrice += dist_matrice.T      #on remplit les cases vides par symétrie
    
    return dist_matrice, populations, noms_villes


def gamma_val(alpha, k, populations):
    """retourne la valeur gamma a partir d'alpha, k et le vecteur de population/ville"""    
    #print(((1+alpha)/k), sum(populations.values()))
    return ((1+alpha)/k) * (populations.sum())

#l'affichage dans Q1 et Q2 sont un peu différents d'ou les 2 fonctions (pour eviter un tas de if)
def displayResultQ1(k, n, x, y, noms_villes, villes_soins, m):    
    """affiche l'affectation secteur j : ville_i_secteur_j pour chaque ville et chaque secteur
       et affiche la valeur de la fonction objectif
    """
    
    print('\Affectation optimale:\n')
    for j in range(k):
        print("Secteur",noms_villes[villes_soins[j]+1], end=' :\n\t')
        for i in range(n):
            if(int(x[:, j][i].x)) == 1:
                print(noms_villes[i+1], end=', ')
        print("\n")
    
    print('\nValeur de la fonction objectif :', m.objVal)
    
    
def displayResultQ2(range1, range2, x, y, noms_villes, model, dist_matrice, showMax=False):
    """affiche l'affectation secteur j : ville_i_secteur_j pour chaque ville et chaque secteur
       et affiche la valeur de la fonction objectif
       ----
       si showMax=True : affiche la distance maximale entre un des secteurs et une des villes
                         dans l'affectation trouvée
    """
    
    max_dij = 0    #utile pour comparer avec les resultats du PL en Q2.2 
    print('\Affectation optimale:\n')
    for j in range(range1):
        if(int(y[j].x) == 1):
            print("Secteur", noms_villes[j+1], end=' :\n\t')
            for i in range(range2):
                if(int(x[:, j][i].x)) == 1:
                    if(showMax):
                        print(noms_villes[i+1], dist_matrice[i][j], end=', ')
                    else:
                        print(noms_villes[i+1], end=', ')
                        
                    if(max_dij < dist_matrice[i][j]):
                        max_dij = dist_matrice[i][j]
            print("\n")
            
    if(showMax):
        print("max_dij=", max_dij)
        
    print('\nValeur de la fonction objectif :', model.objVal)
