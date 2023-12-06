# -*- coding: utf-8 -*

import pygame
from pygame.locals import *
import numpy as np
from math import *

from ma_bao_pygame import *

# paramètres modifiables
dimension_fenetre = (800, 600)
vitesse = 0.25 # vitesse de l'animation ( 1 pour 10 images par anim, 0.5 pour 20...)
centre_x,centre_y = dimension_fenetre[0]//2, dimension_fenetre[1]//2
dim_x_max=dim_y_max = min(dimension_fenetre[0]//2 - 30,dimension_fenetre[1]//2 - 30) # Valeur maximale des x et y affichés

# Constantes :

OUVERTURE = 0
DECALAGE = 1
PI_2=np.math.pi/2

#------------------------------- Mes fonctions auxiliaires


def rotation(centre_x,centre_y,angle,x,y):
    """
    renvoie les coordonnées du résultat de la rotation du point de coordonnées (x,y) par la rotation d'angle et centre donnés
    """
    return ((x-centre_x)*cos(angle) - (y-centre_y)*sin(angle) + centre_x, (x-centre_x)*sin(angle)+(y-centre_y)*cos(angle)+centre_y)

def afficher(papier,fenetre,x_min,x_max,y_min,y_max):
    """
    papier est donné en coordonnées entières de segments de longueur 1
    Il faut donc le transformer en coordonnées pour l'écran
    """
    liste_points = (papier*min(dim_x_max/(max(abs(x_min),x_max)),dim_y_max/max(abs(y_min),y_max)))+np.array([centre_x,centre_y])
    pygame.draw.lines(fenetre,(0,0,200),False,liste_points)




#------------------------------- Fonction principale

def main():
    global vitesse
    #------------- Init
    pygame.init()
    fenetre = pygame.display.set_mode(dimension_fenetre)
    # Afficher un fond blanc
    fond = pygame.Surface(fenetre.get_size())
    fond = fond.convert()
    fond.fill((255,255,255))
    fenetre.blit(fond,(0,0))
    font=pygame.font.SysFont("Arial",12,bold=False,italic=False)
    font_victoire=pygame.font.SysFont("Arial",48,bold=True,italic=False)
    fontsmall=pygame.font.SysFont("Arial",10,bold=False,italic=False)
    #Pour gérer l'appuye répété sur une touche
    pygame.key.set_repeat(400,20)

    # papier_1 est le principal, papier_2 représente la partie que l'on déplie
    papier_1 = np.array([[0,0],[1,0]])
    papier_2 = np.array([[0,0],[0,0]])
    papier_cache = np.zeros((1,2))

    mode = OUVERTURE
    animation = False
    angle = 0
    decalage = np.array([0,0])
    n_decalage = 0
    nombre_pliages=0


    #------------- Boucle de jeu

    continuer=1
    while continuer:
        #On efface l'écran
        fenetre.fill((255,255,255))
        pygame.time.Clock().tick(30) # Pour éviter de trop rafraichir
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT :     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle
            if event.type == KEYUP :
                if event.key==K_ESCAPE :
                    continuer = 0
                if event.key==K_PLUS or event.key == K_KP_PLUS:
                    vitesse *=2
                if event.key==K_MINUS or event.key == K_KP_MINUS:
                    vitesse /=2
                if event.key == K_SPACE :
                    if mode == OUVERTURE and not animation:
                        animation = True
                        angle = 0
                        nombre_pliages+=1
                    if mode == DECALAGE and not animation :
                        animation = True
                        decalage = papier_2[-1]
                        n_decalage = 0
                        papier_1 = np.concatenate((np.flip(papier_2,axis=0),papier_1[1:,:]))
                        papier_2 = np.zeros((1,2))
                        papier_cache=papier_1-decalage
                if event.key==K_BACKSPACE:
                    papier_1 = np.array([[0,0],[1,0]])
                    papier_2 = np.array([[0,0],[0,0]])
                    mode = OUVERTURE
                    animation = False
                    angle = 0
                    decalage = np.array([0,0])
                    n_decalage = 0



        if animation :
            if mode == OUVERTURE:
                angle+= vitesse * 0.157
                if angle>PI_2 : # Anim terminée
                    angle = PI_2
                    animation=False
                    mode = DECALAGE
                papier_2 = np.dot(np.array([[cos(angle),sin(angle)],[-sin(angle),cos(angle)]]),papier_1.T).T
            elif mode == DECALAGE:
                n_decalage+=1
                if n_decalage*vitesse>10:
                    animation = False
                    mode = OUVERTURE
                    papier_1 = papier_cache
                else: papier_1 = papier_1 - decalage*vitesse*0.1
        papier = np.concatenate((papier_1,papier_2))
        x_min,y_min=papier.min(axis=0)
        x_max,y_max=papier.max(axis=0)
        if y_min==y_max==0 :
            y_min=-1
            y_max=1
        afficher(papier_1,fenetre,x_min,x_max,y_min,y_max)
        if papier_2.shape[0]>1:
            afficher(papier_2,fenetre,x_min,x_max,y_min,y_max)

        # Les textes
        text=font.render("Vitesse des animations = {}".format(vitesse),1,(0,0,0))
        fenetre.blit(text,(10,10))
        text=font.render("Nombre de pliages = {}".format(nombre_pliages),1,(0,0,0))
        fenetre.blit(text,(10,30))
        text=font.render("Nombre de segments = {}".format(2**nombre_pliages),1,(0,0,0))
        fenetre.blit(text,(10,50))




        pygame.display.flip() # Pour rafraichir l'affichage


    pygame.quit()
    exit()



#----------------------------------

if __name__ == "__main__":
    pass
    main()


# TODO : Rajouter le texte des touches