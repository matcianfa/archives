"""
Script de capture graphique des données pour le 2048
Le principe est simple, on regarde la couleur d'un seul pixel par case pour savoir à quelle valeur il correspond.
"""

from PIL import Image, ImageGrab # Pour faire la capture d'ecran

# Couleur qu'il faudra peut-être modifier selon la version utilisée
# Il faut au moins les couleurs des cases vides, 1 et 2. Le reste sert uniquement à pouvoir reprendre une partie en cours
couleur_to_valeur={(214, 205, 196):0,(238, 228, 218):1,(237, 224, 200):2,(242, 177, 121):3,(245, 149, 99):4,(246, 124, 95):5,(246, 94, 59):6,(237, 207, 114):7,(237, 204, 97):8,(237, 200, 80):9,(237, 197, 63):10}

def capturer(x0,y0,x1,y1,intercase,decalage,N=4):
    """
    Fait la capture d'ecran entre les points de coordonnées (x0,y0) et (x1,y1). Attention à bien prendre la zone autour des cases (pas au ras)
    Calcule automatiquement les coordonnées des pixels à regarder (c'est pour ca qu'il faut l'intercase entre les cases)
    decalage correspond à quelle distance de l'angle haut gauche de chaque case se trouve le pixel qu'on souhaite observer pour la couleur
    N correspond à la dimension de la grille (4 de base)
    Donne en sortie une grille contenant les puissances de 2
    Comme les couleurs pour des puissances élevées sont les mêmes, il faut sauvegarder les cases déjà connues.
    Du coup, on ne va chercher en réalité que les cases contenant des 2 ou des 4

    """


    # On capture l'image dans la zone
    image =ImageGrab.grab(bbox=(x0,y0,x1,y1))

    # Sauvegarde de l'image pour debugguer
    image.save("capture.png")

    #  Prétraitement de l'image
    #image = image.convert('L')    # Echelle de gris

    grille=[]
    # On prélève les couleurs
    delta =(x1-x0-intercase)//N
    for i in range(N):
        ligne=[]
        for j in range(N):
            couleur=image.getpixel((intercase+decalage+j*delta,intercase+decalage+i*delta))
            if couleur in couleur_to_valeur:
                ligne.append(couleur_to_valeur[couleur])
            else:
                print("Nouvelle couleur",couleur)
                ligne.append(0)

        grille.append(ligne)
    return grille

if __name__ == '__main__': # Pour le debug
    print(capturer(515,250,842,578,7,10))