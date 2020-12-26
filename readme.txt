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

min z = sum(i,j) di,j * xi,j 	  //min des distances moyennes pour qqun en ville i vers ville j
	| sum(i,j) vj*xij < gamma qqsoit j    //pop villes secteurs < gamma
	| sum(i) xij = 1 	          //chaque unité est dans une seule ville (à un moment donné)


C2 : si c'est seulement vj, vj < gamma sera toujours  vrai même avec k=5 t alpha=0.1

k=3 alpha=0.1

-------
Méthode par flot max à cout min :
Impossible à réaliser.