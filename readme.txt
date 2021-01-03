Binome (GRP3) :
Anthea RICHAUME
Bassem YAGOUB
---------------


Fichiers :
    - src/ :
        -func_utils.py
            --> fonctions d'import de CSV, calcul de gamma et d'affichages réutilisées dans les différents fichiers
        - localisations_soins_patientsQX_Y.py
            --> fichiers contenant les programmes linéaires des Q1 et Q2
        - equilibrage_unite.py
            --> fichier contenant le programme linéaire répondant à la Q3
    - ressources/ :
        - fichiers utilisés pour extraire les données (seul le csv est utilisé dans le code)


Utilisation :
    - Q1_2 : Faire varier les variables k et alpha et modifier la liste "villes_soins" pour changer l'attribution des villes de soins
             Par défaut la valeur de villes_soins est la liste des k premiers nombres (à partir de 0)
    - Q2_X : Simplement faire varier les variables k et alpha pour tester différentes affectations
    - Fonction displayResultQ2(...) dans func_utils.py : le paramètre booléen en fin de fonction permet d'afficher les distances entre une ville j et ses villes i
                                                         ainsi que la distance max observée (pour comparer les résultats de la Q2_1 et Q2_2)
                                                         
    - Plus de détails sont en commentaires de code