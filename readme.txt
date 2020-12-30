Fichier qui sert de brouillon actuellement.

- n villes
- vi = population ville i
- k unités, k < n
- xij = 1 si hab.i traité par j si besoin
	  = 0 sinon
- plusieurs villes i possibles pour un secteur j
  mais pas l'inverse
- dij = distance moy de ville i à secteur(ville) j


Q1.1

min z = (sum(i,j) di,j * xi,j)/n            //min des distances moyennes pour qqun en ville i vers ville j
	| sum(i) vi*xij < gamma qqsoit j    //pop villes secteurs < gamma
	| sum(j)   xij    = 1               //chaque ville n'a qu'un secteur de soin

exemples : k=3, (les 3 premieres villes)
C1: 340K*x21+310K*x31+...+152K*x151 < gamma | pour chaque j <=> k contraintes
C2: x41+x42+x43 = 1                         | pour chaque ligne <=> 15 contraintes


k=3 alpha=0.1

-------
Méthode par flot max à cout min :
Impossible à réaliser.

C1 :
[
 [479553, 340017, 309346, 285121, 280966, 254436, 232787, 216815, 182460, 172565, 171953, 170147, 158454, 156920, 152960, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 479553, 340017, 309346, 285121, 280966, 254436, 232787, 216815, 182460, 172565, 171953, 170147, 158454, 156920, 152960, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 479553, 340017, 309346, 285121, 280966, 254436, 232787, 216815, 182460, 172565, 171953, 170147, 158454, 156920, 152960, 0, 0, 1]
]

C2:
n*k : 3 premieres villes = soins
Toulouse : 0,   562,  585
Nice :     562, 0,    1143
Nantes :   585, 1143, 0
