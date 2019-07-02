"""
Fonction de capture graphique de la grille. On fait une capture d'ecran case par case et on le dechiffre avec Tesseract
"""


import numpy as np
from PIL import Image, ImageGrab, ImageEnhance, ImageFilter # Pour faire la capture d'ecran
import cv2 # Pour afficher les captures d'ecran #pip install opencv-python
import pytesseract # OCR à  installer à part aussi

# Préciser le chemin à  suivre pour le fichier tesseract.exe
pytesseract.pytesseract.tesseract_cmd = 'c:\\Program Files\\Tesseract-OCR-2\\tesseract'





#---------------------- Fonctions

def capturer(x0,y0,x1,y1):
    """ Capture graphiquement les nombres de la grille et renvoie la grille """

    dim_case_x,dim_case_y=(x1-x0)//9,(y1-y0)//9
    grille=[]
    print("Lecture de la grille:")
    print("+---+---+---+")
    for i in range(9):
        ligne=[]
        print("|",end="")
        for j in range(9):

            # On capture le chiffre de la i eme ligne et j ieme colonne
            image=ImageGrab.grab(bbox=(x0+j*dim_case_x,y0+i*dim_case_y,x0+(j+1)*dim_case_x,y0+(i+1)*dim_case_y))

            #  Prétraitement de l'image
            image = image.convert('L')    # Echelle de gris
            image = image.filter(ImageFilter.MinFilter())       # a little blur
            image = image.point(lambda x: 0 if x <80 else 255) # Noir et blanc avec seuil bas pour faire disparaitre la grille

            # Sauvegarde de l'image pour debugguer
            image.save("capture{}-{}.png".format(j,i))

            # On récupère le texte sur l'image
            text = pytesseract.image_to_string(image,config='--psm 10')
            if text=="": text="0"
            print(text,end="")
            if j%3==2 : print("|",end="")
            ligne.append(int(text))
        print("")
        if i%3==2: print("+---+---+---+")
        grille.append(ligne)
    return grille



if __name__ == '__main__':
    pass
    print(capturer(500,133,857,491))
    """
    while 1:
        capturer()
        if cv2.waitKey(500) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    """

