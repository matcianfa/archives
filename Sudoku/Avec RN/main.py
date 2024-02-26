from capture_ecran import *
from reconnaissance_chiffres import *
from resolution_sudoku import *

import time
import pyautogui as ag # Permet la gestion de la souris (pip install pyautogui si besoin)

# ---------------------------------- Constantes

POSITIONS_CHIFFRES_A_CLIQUER_X = [-1,372,446,524,608,685,767,846,925,1002]
POSITIONS_CHIFFRES_A_CLIQUER_Y = 962

# On charge le modèle
modele = tf.keras.models.load_model(NOM_MODELE)


# ---------------------------------- gestion de la souris

def cliquer(i,j,valeur,valeur_precedente):
    """
    Fonction qui rentre la valeur dans la case se trouvant à la ligne i et colonne j
    """

    # On clique sur la valeur si elle est differente de la précédente
    if valeur != valeur_precedente :
        ag.click(POSITIONS_CHIFFRES_A_CLIQUER_X[valeur],POSITIONS_CHIFFRES_A_CLIQUER_Y)

    # On selectionne la case à remplir
    ag.click(LISTE_COORDONNEES_CASES_X[j] + DIM_CASE_X//2,LISTE_COORDONNEES_CASES_Y[i] + DIM_CASE_X//2)


# ---------------------------------- fonction principale

def lancer():
    """
    Fonction qui lance la résolution automatique
    1 - Capture de la grille et reconnaissance des chiffres
    2 - On la résout
    3 - On gère la souris pour remplir la grille automatiquement
    """
    t_0 = time.time()

    # ag.hotkey('alt', 'tab')  # Fait un alt+ tab. A mettre en commentaire si ce n'est pas necessaire (par exemple si on a deux ecrans)


    grille = reconnaitre_grille(modele)

    est_vide = grille == 0  # Une grille avec True si la case est vide (contient 0)

    resoudre(grille)

    print("La grille résolue est :")
    print(grille)

    # On clique une fois pour rien sur la fenetre pour l'activer
    ag.click(100,100)

    valeur_precedente = -1 # On est obligé de garder la valeur precedente car si on clique 2 fois sur le  même chiffre ca annule le choix...

    for ligne in range(9):
        for col in range(9):
            if est_vide[ligne,col]:
                cliquer(ligne, col, grille[ligne, col],valeur_precedente)
                valeur_precedente = grille[ligne, col]

    print(f"Résolu en {time.time()-t_0} s")