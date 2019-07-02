"""
Script de résolution d'une grille de Sudoku
Prend en entrée un grille de sudoku classique (pas numpy) et donne en sortie la grille remplie.
On utilise un algorithme de retour sur trace (backtracking)
"""


#-------------------- Fonctions auxilliaires

def ajout_possible_sur_ligne(grille,i,valeur):
    """
    Vérifie si la valeur existe déjà sur la i eme ligne
    """
    for j in range(9):
        if grille[i][j]==valeur: return False
    return True

def ajout_possible_sur_colonne(grille,j,valeur):
    """
    Vérifie si la valeur existe déjà sur la i eme ligne
    """
    for i in range(9):
        if grille[i][j]==valeur: return False
    return True

def ajout_possible_dans_bloc(grille,i,j,valeur):
    """
    Vérifie si la valeur existe déjà sur la i eme ligne
    """
    i0,j0=i//3,j//3
    for di in range(3):
        for dj in range(3):
            if grille[i0*3+di][j0*3+dj]==valeur: return False
    return True

def suivant(i,j):
    """
    Donne la case suivante pour parcourir la grille comme on la lirait
    """
    if j<8: return (i,j+1)
    return (i+1,0)


#-------------------- Fonction principale

def donner_solution(grille):
    """
    Fonction qui résoud le sudoku et renvoie la solution
    """
    # On copie la grille
    reponse=[ligne.copy() for ligne in grille]

    def backtracking(grille,i,j):
        """
        On cherche case par case les valeurs possibles.
        Dès qu'une case ne peut pas être remplie, on revient en arriere pour tester une autre valeur
        """
        global reponse
        if i==9 :# Si on a parcouru toute la grille c'est qu'on a réussi à la remplir
            reponse=[ligne.copy() for ligne in grille]
            return True
        if grille[i][j]!=0 :
            return backtracking(grille,*suivant(i,j)) # Si la case est déjà remplie, on passe à la suivante
        # On teste toute les valeurs possibles pour une case
        for valeur in range(1,10):
            # Si la valeur n'est pas encore dans la ligne, colonne ou bloc
            if ajout_possible_sur_ligne(grille,i,valeur) and ajout_possible_sur_colonne(grille,j,valeur) and ajout_possible_dans_bloc(grille,i,j,valeur):
                # On remplit la grille avec cette valeur
                grille[i][j]=valeur
                if backtracking(grille,*suivant(i,j)):
                    return True
                # On retire la valeur de la grille puisque si on en est ici du programme c'est qu'on n'a pas réussi à finir la grille
                grille[i][j]=0
        # Si on en est là c'est qu'on n'a pas réussi à trouver une valeur qui convient
        return False

    # On lance la recherche de solution en partant de la première case
    backtracking(reponse,0,0)

    return reponse



if __name__=="__main__": # Pour le debug
    grille=[[0, 1, 0, 0, 0, 0, 4, 3, 0], [7, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 5, 4, 9, 0, 0], [1, 7, 0, 0, 4, 0, 2, 0, 6], [0, 0, 0, 0, 9, 0, 0, 0, 3], [0, 0, 3, 0, 0, 6, 0, 8, 0], [0, 0, 1, 4, 7, 0, 0, 6, 0], [0, 0, 0, 5, 0, 8, 1, 2, 0], [0, 9, 0, 0, 6, 0, 3, 0, 4]]
    #grille=[[0, 0, 0, 8, 0, 5, 0, 1, 3], [0, 0, 0, 2, 0, 3, 6, 0, 0], [6, 0, 0, 0, 9, 0, 2, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 4, 0, 1, 0, 0, 7, 0, 6], [2, 5, 6, 3, 0, 4, 8, 9, 0], [5, 9, 0, 0, 0, 7, 1, 0, 2], [1, 0, 2, 0, 8, 0, 4, 7, 0], [0, 0, 4, 9, 1, 0, 0, 3, 8]]
    print(donner_solution(grille))







