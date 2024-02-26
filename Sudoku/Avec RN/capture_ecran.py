import os
import numpy as np
from PIL import ImageGrab # Pour faire la capture d'ecran


# ------------------------------- Constantes

# La liste des coordonnées du coin haut/gauche de chaque case
LISTE_COORDONNEES_CASES_X = [337,413,491,571,649,727,807,885,963]
LISTE_COORDONNEES_CASES_Y = [189,263,342,424,499,578,659,735,814]
DIM_CASE_X,DIM_CASE_Y = 72,70

CHEMIN_IMAGES_ENTRAINEMENT = "images/" # A créer s'il n'existe pas



# ----------------------------------------- Création des images d'entrainement

def creer_images_entrainement():
    """
    Crée dans le dossier images/ les images de chaque case
    Le nom d'enregistrement est de la forme : image_x_y.png
    """

    capture_ecran = ImageGrab.grab()
    for x in range(9):
        for y in range(9):
            # On capture la case à la y eme ligne et x ieme colonne
            image=capture_ecran.crop((LISTE_COORDONNEES_CASES_X[x], LISTE_COORDONNEES_CASES_Y[y], LISTE_COORDONNEES_CASES_X[x] + DIM_CASE_X, LISTE_COORDONNEES_CASES_Y[y] + DIM_CASE_Y))

            # --- Sauvegarde de l'image
            image.save(f"{CHEMIN_IMAGES_ENTRAINEMENT}image_{x}_{y}.png")

    # On crée les répertoires dans lesquels on va ranger les images
    for i in range(10):
        try :
            os.mkdir(f"{CHEMIN_IMAGES_ENTRAINEMENT}{i}")
        except : pass

# ----------------------------------------- Capturer les images

def capturer_images_cases():
    """
    Fait une capture d'écran et crée la liste des images des cases
    """

    liste_images_cases = []
    capture_ecran = ImageGrab.grab()
    for y in range(9):
        for x in range(9):
            # On capture la case à la y eme ligne et x ieme colonne
            image=capture_ecran.crop((LISTE_COORDONNEES_CASES_X[x], LISTE_COORDONNEES_CASES_Y[y], LISTE_COORDONNEES_CASES_X[x] + DIM_CASE_X, LISTE_COORDONNEES_CASES_Y[y] + DIM_CASE_Y))

            liste_images_cases.append(image)

    return liste_images_cases



if __name__ =="__main__" :
    pass