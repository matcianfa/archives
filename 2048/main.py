"""
Script principal
"""
from  IA import * # module perso contenant l'IA du jeu
import capture # module perso contenant les fonctions permettant la recupération graphique des données
import pyautogui as ag # Gestion de la souris et du clavier
import time
from random import randint

#-------------- Constantes à modifier en fonction de la configuration graphique
# Pour obtenir ces valeurs on peut par exemple prendre un screenshot de la fenetre de jeu puis avec Paint, lire les coordonnées en placant la souris dessus
# Coordonnées de l'angle haut gauche de la grille (y compris rebord)
x0,y0= 515,250
# Coordonnées de l'angle bas droit de la grille (y compris rebord)
x1,y1= 842,578
# Distance entre les cases
intercase=7
# Décalage par rapport au bord de la case pour prélever la couleur
decalage=10
# Nombre de parties aléatoires qu'on teste avant de choisir la meilleur direction
nb_essais=5000
# Dimension de la grille
N=4
# Distance sur laquelle on fait bouger la souris pour jouer un coup
balayage_souris=100
# Temps d'attente entre le coup joué et la capture d'écran suivante (en seconde)
attente=0.3
# Pour traduire le nombre en direction (0 pour droite etc.)
trad_direction=["Droite","Haut","Gauche","Bas"]

#--------------------------- Gestion des mouvements

def jouer(direction):
    """
    Déplace la souris sur l'ecran dans la direction indiquée pour jouer
    """
    # On place la souris au centre
    ag.moveTo((x0+x1)//2,(y0+y1)//2)
    if direction==0: ag.drag(100,0)
    elif direction==2: ag.drag(-100,0)
    elif direction==1: ag.drag(0,-100)
    elif direction==3: ag.drag(0,100)


# -------------------------- Fonction aux

def est_vide(grille):
    for ligne in range(N):
            for col in range(N):
                if grille[ligne][col]!=0: return False
    return True

#--------------------------- Fonction principale

def lancer(grille=None,dim=N):
    """
    Fonction à lancer pour démarrer l'IA
    On peut rentrer une grille à la main comme point de départ pour reprendre une partie arretée par exemple
    dim est la dimension de la grille (de base 4)
    """
    if grille is None: grille=[[0]*N for _ in range(N)]

    while not est_fini(grille): # Tant qu'on peut jouer, on joue
        # On recupère graphique la grille (seulement les 2 et 4)
        grille_capturee=capture.capturer(x0,y0,x1,y1,intercase,decalage,N)

        #!!!
        print("Grille capturée")
        afficher_grille(grille_capturee)

        # Si il n'y a que des 0, on s'arrete
        if est_vide(grille_capturee):
            print("Grille vide, c'est fini")
            break

        compteur_de_0=0
        # On rajoute les 2 et les 4 présents
        for ligne in range(N):
            for col in range(N):
                if grille_capturee[ligne][col]!=0:
                    # Pour voir s'il y a un probleme:
                    if grille[ligne][col]>2 :
                        if grille[ligne][col]!=grille_capturee[ligne][col]  and grille[ligne][col]<13:
                            print("Problème !!!!!!!!!!!!!!!!!!!")
                    else:
                        grille[ligne][col]=grille_capturee[ligne][col]
                if grille[ligne][col]==0: compteur_de_0+=1

        print("Grille utilisée")
        afficher_grille(grille)
        # On cherche le coup à jouer
        # Version à nombre d'essais fixe :
        direction_a_jouer=donner_direction(grille,nb_essais)

        # Seconde version : moins il y a de zéros dans la grille, plus on fait d'essais
        #direction_a_jouer=donner_direction(grille,5000-332*compteur_de_0)


        # Et on le joue virtuellement pour mettre à jour notre grille
        appliquer_mvt(grille,direction_a_jouer,N)

        print("Direction jouée :",trad_direction[direction_a_jouer])


        # On joue le coup
        jouer(direction_a_jouer)

        #On attend un peu le temps que la grille se stabilise
        time.sleep(attente)


