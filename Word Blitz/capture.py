"""
Script de capture et de lecture automatique des lettres
Pour que cela fonctionne il faut que les lettres soient correctement lues.
Il faudra donc surement modifier les valeurs des coordonnées de base.
Il va de soi qu'il faut selectionner une bonne fois pour toute la position de la grille de jeu (par exemple en mettant la fenetre en mode fenetre agrandie)
Pour obtenir les coordonnées, j'ai pris un screenshot de mon ecran et j'ai ouvert avec paint qui donne les coordonnées de la souris
"""


import numpy as np
from PIL import Image, ImageGrab, ImageEnhance, ImageFilter # Pour faire la capture d'ecran
#import cv2 # Pour afficher les captures d'ecran #pip install opencv-python
import pytesseract # OCR à  installer à part aussi

# Préciser le chemin à  suivre pour le fichier tesseract.exe
pytesseract.pytesseract.tesseract_cmd = 'c:\\Program Files\\Tesseract-OCR-2\\tesseract'

# 0 pour Word blitz
# 1 pour Boggle
jeu = 0

#----------------------- Constantes modifiables ( selon la position du jeu)
if jeu == 0:
    # Coordonnées de l'angle haut gauche de la première lettre (prendre un peu large mais pas trop)
    x0_lettre,y0_lettre=530,310
    # Dimension lettres
    largeur_lettre,hauteur_lettre=43,40
    # Ecart entre les lettres
    ecart_x,ecart_y=81,82
    # centre de la première lettre
    centre_lettre_x,centre_lettre_y=x0_lettre+largeur_lettre//2,y0_lettre+hauteur_lettre//2
elif jeu == 1:
    # Coordonnées de l'angle haut gauche de la première lettre (prendre un peu large mais pas trop)
    x0_lettre,y0_lettre=510,207
    # Dimension lettres
    largeur_lettre,hauteur_lettre=40,45
    # Ecart entre les lettres
    ecart_x,ecart_y=90,90
    # centre de la première lettre
    centre_lettre_x,centre_lettre_y=x0_lettre+largeur_lettre//2,y0_lettre+hauteur_lettre//2

#---------------------- Fonctions

def capturer():
    """ Capture graphiquement les lettres de la grille et renvoie la grille """
    grille=[]
    # On capture lettre à lettre
    for j in range(4):
        ligne=[]
        for i in range(4):
            # On capture la lettre de la i eme ligne et j ieme colonne
            image=ImageGrab.grab(bbox=(x0_lettre+i*ecart_x,y0_lettre+j*ecart_y,x0_lettre+i*ecart_x + largeur_lettre,y0_lettre+j*ecart_y+hauteur_lettre))

            #  Prétraitement de l'image
            image = image.convert('L')    # Echelle de gris
            #image = image.filter(ImageFilter.MinFilter())       # a little blur
            image = image.point(lambda x: 0 if x < 140 else 255) # Noir et blanc

            # Sauvegarde de dee l'image pour debugguer
            image.save("capture{}-{}.png".format(j,i))

            # On récupère le texte sur l'image (--psm 10 pour préciser qu'il n'y a qu'une lettre à chercher)
            text = pytesseract.image_to_string(image,config='--psm 10')
            text=text[:1] # Des fois la lecture n'est pas très bonne, on ne prend que la première lettre
            print(text)

            # Modif connues en cas de mauvaise lecture :
            if text in "|l[]" : text="I"

            text=text.upper()
            # On ajoute la lettre dans la ligne
            ligne.append(text)


        # On met la ligne complète dans la grille
        grille.append(ligne)
    return grille




