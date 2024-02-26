"""
Pour plus de détails et voir même comment générer des grilles de sudoku, voir :
https://colab.research.google.com/drive/1E-fuCydQBLS34MEneOE-QGC_yv4_9iv2?usp=sharing#scrollTo=zpnROSnSV1gp
"""
import numpy as np


def est_rajoutable(grille,ligne,col,valeur):
    """
    Vérifie si on peut rajouter la valeur dans la grille
    """
    # On cherche si la valeur est dans la ligne
    for nombre in grille[ligne]:
        if nombre == valeur:
            return False

    # On cherche si la valeur est dans la colonne
    for nombre in grille[:, col]:
        if nombre == valeur:
            return False

    # On cherche si la valeur est dans le sous-carré 3x3
    ligne_premiere_case = 3*(ligne//3)
    col_premiere_case = 3*(col//3)
    for l in range(ligne_premiere_case, ligne_premiere_case+3):
        for c in range(col_premiere_case, col_premiere_case+3):
            if grille[l,c] == valeur:
                return False

    # sinon on peut rajouter une valeur
    return True

def resoudre(grille):
    """
    Resout la grille
    """
    cases_modifiables = grille == 0 # On garde en mémoire les cases qui sont à remplir (qui ont un 0 à l'origine)
    resolu = False
    au_suivant = True
    ligne,col = 0,0 # Les coordonnées de la case qu'on considère
    while not resolu:
        if cases_modifiables[ligne,col]:
            au_suivant = False # Pour savoir si on peut passer au suivant car on a réussi à placer une valeur dans la case en cours

            # On essaye la valeur suivante de la case en cours
            for valeur in range(grille[ligne,col]+1,10):
                if est_rajoutable(grille,ligne,col,valeur):
                    grille[ligne,col] = valeur
                    au_suivant = True
                    break

        # Si on a réussi à modifier une case:
        if au_suivant :
            if (ligne,col) == (8,8): # Si c'est fini
                resolu = True

            # On avance
            col = (col+1)%9
            if col == 0:
                ligne +=1

        else :
            if cases_modifiables[ligne,col]:
                grille[ligne,col] = 0

            # On recule
            col = (col-1)%9
            if col == 8:
                ligne -=1