"""
Script principal pour résoudre graphiquement des sudokus
On s'est basé sur un jeu de Sudoku sur un emulateur Android (Memu Play) nommé simplement Sudoku.
Pour jouer, il faut cliquer sur la case puis cliquer sur le numéro que l'on souhaite mettre dans cette case en dessous de la grille
"""
import pyautogui as ag # Permet la gestion de la souris
import capture # Perso : Pour capturer les données à l'écran
import IA # Perso : permet de générer les réponses possibles sur la grille
import time

#----------------------- Constantes modifiables ( selon la position du jeu)
x0,y0,x1,y1=500,133,857,491
dim_case_x,dim_case_y=(x1-x0)//9,(y1-y0)//9

# Liste donnant les positions des cases sur lesquelles il faut cliquer pour rentrer la valeur
positions_x_chiffres=[None,523,562,601,639,678,717,757,796,835]
positions_y_chiffres=628

def cliquer(i,j,valeur):
    """
    Fonction qui rentre la valeur dans la case se trouvant à la ligne i et colonne j
    """
    # On selectionne la case à remplir
    ag.click(x0+j*dim_case_x + dim_case_x//2,y0+i*dim_case_y+dim_case_y//2)

    # On clique sur la valeur
    ag.click(positions_x_chiffres[valeur],positions_y_chiffres)


def lancer():
    t0=time.time()
    # On récupère les données
    grille=capture.capturer(x0,y0,x1,y1)
    t1=time.time()
    print("Capture effectuée en {} s".format(round(t1-t0,1)))
    print("Recherche de la solution")
    # On détermine la solution
    solution = IA.donner_solution(grille)
    print("Solution trouvée en {} s".format(round(time.time()-t1,1)))
    # On remplit la grille sur l'emulateur
    for i in range(9):
        for j in range(9):
            if grille[i][j]==0: # Si la case etait vide au début, on la remplit
                cliquer(i,j,solution[i][j])
