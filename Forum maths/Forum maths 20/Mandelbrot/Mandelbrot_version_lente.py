# -*- coding: utf-8 -*

import pygame
from pygame.locals import *
from PIL import Image, ImageDraw
from time import time
import numpy as np
from numba import jit #A installer avec conda. Permet d'optimiser enormément la vitesse de calcul

# Ma boite à outil (pour avoir les cases à cocher
from ma_bao_pygame import *

#----------------------- Constantes
MAX_ITER = 80
WIDTH,HEIGHT = 800,600 # Dim de la fenetre
X_MIN,Y_MIN,X_MAX = -2,-1,1 # Valeurs min et max pour les parties reelles et imaginaires
Y_MAX=Y_MIN+HEIGHT*(X_MAX-X_MIN)/WIDTH #Pour avoir un repère normé

#----------------------- Fonctions auxiliaires

def mandelbrot(c):
    """
    Renvoie le nombre d'itérations avant de s'éloigner de plus de 2 de l'origine
    """
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1
    return n

@jit
def mandelbrot_liste(c,max_iter=MAX_ITER):
    """
    Renvoie la liste des nombres complexes calculés
    """
    z = 0
    n = 0
    liste=[z]
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
        liste.append(z)
    return liste

def convertir_complexes_to_points(liste):
    """
    Converti la liste des complexes en liste de points dans la fenetre
    """
    return [(int((z.real-X_MIN)*WIDTH/(X_MAX-X_MIN)),int((z.imag-Y_MIN)*HEIGHT/(Y_MAX-Y_MIN))) for z in liste]

def convertir_point_to_complexe(point):
    """
    converti les coordonnées d'un point de l'image en complexe associé
    """
    x,y=point
    return complex(X_MIN+x*(X_MAX-X_MIN)/WIDTH,Y_MIN+y*(Y_MAX-Y_MIN)/HEIGHT)

#------------- Versions optimisées
# En utilisant numpy et numba
@jit
def mandelbrot_opti(cr,ci,max_iter=MAX_ITER):
    """
    Renvoie le rang à partir duquel on depasse 2 en module
    Prend en entrée la partie réelle et imaginaire de c
    """
    r,i=0,0
    for n in range(max_iter):
        r2 = r*r
        i2 = i*i
        if r2 + i2 > 4.0:
            return n
        i = 2* r*i + ci
        r = r2 - i2 + cr
    return max_iter


#------------- Fonctions auxiliaires graphiques

def tracer_ligne_brisee(liste_points,fenetre,afficher_ligne=True):
    """
    Pour tracer la ligne brisée des differents points de la liste
    """
    try:
        # Constantes modifiables
        COULEUR = (125,125,125)
        EPAISSEUR = 2
        pt0=liste_points[0]
        # pygame.draw.circle(fenetre,COULEUR , pt0,EPAISSEUR) # LE premier point étant toujours O, on ne le trace pas
        for i in range(1,len(liste_points)):
            # On trace le point
            pt1=liste_points[i]
            pygame.draw.circle(fenetre,COULEUR , pt1,EPAISSEUR)
            if afficher_ligne :
                # On trace la ligne entre le point précédent et celui qu'on vient de tracer
                pygame.draw.line(fenetre,COULEUR,pt0,pt1)
            pt0=pt1
    except TypeError :
        print("Erreur dans tracer_ligne_brisee",pt0)

def tracer_axes(fenetre):
    """
    Trace les axes
    """
    pass

@jit
def creer_image_NB():
    im = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    X = np.linspace(X_MIN, X_MAX, WIDTH)
    Y = np.linspace(Y_MIN, Y_MAX, HEIGHT)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if mandelbrot_opti(X[x],Y[y]) == MAX_ITER :
                draw.point((x, y), (0, 0, 0))
    im.save('outputNB.png', 'PNG')

@jit
def creer_image(max_iter=MAX_ITER):
    im = Image.new('HSV', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    X = np.linspace(X_MIN, X_MAX, WIDTH)
    Y = np.linspace(Y_MIN, Y_MAX, HEIGHT)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            n=mandelbrot_opti(X[x],Y[y],max_iter)
            #draw.point((x, y), (int(255 * n / max_iter), 255, 255 if n < max_iter else 0))
            draw.point((x, y), (n%255, 255, 255 if n < max_iter else 0))
    im.convert('RGB').save('output.png', 'PNG')


#----------------------- Fonction principale

def lancer():
    global X_MIN,Y_MIN,X_MAX,Y_MAX
    pygame.init()
    fenetre = pygame.display.set_mode((WIDTH,HEIGHT))
    # Afficher un fond blanc
    fond = pygame.Surface(fenetre.get_size())
    fond = fond.convert()
    fond.fill((255,255,255))
    fenetre.blit(fond,(0,0))
    font=pygame.font.SysFont("Arial",10,bold=False,italic=False)

    # Variables utiles
    liste_points=[]
    objet_cliqué = False # Pour savoir si on a cliqué sur une case ou pas. Si c'est le cas, on ne fait rien d'autre
    position_depart=None # Pour selectionner la zone à zoomer
    # Les objets à afficher
    cases_a_cocher = []
    # les cases à cocher
    cases_a_cocher.append(Case_a_cocher((10,10),"Afficher les lignes",cochee=True))
    cases_a_cocher.append(Case_a_cocher((10,30),"Afficher points de convergence",cochee=False,fonction=creer_image_NB))
    cases_a_cocher.append(Case_a_cocher((10,50),"Afficher vitesse de divergence (couleur)",cochee=False,fonction=creer_image))
    cases_a_cocher.append(Case_a_cocher((10,70),"Afficher vitesse de divergence (HD)",cochee=False,fonction=lambda :creer_image(2000)))



    continuer=1
    while continuer :
        #On efface l'écran
        fenetre.fill((255,255,255))
        pygame.time.Clock().tick(15) # Pour éviter de trop rafraichir
        # On reinitialise ce qui doit l'etre
        objet_cliqué = False
        # On gere les evenements
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT :     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle
            if event.type == KEYDOWN :
                if event.key == K_ESCAPE : # On réinitialise le zoom
                    X_MIN,Y_MIN,X_MAX = -2,-1,1
                    Y_MAX=Y_MIN+HEIGHT*(X_MAX-X_MIN)/WIDTH
                    # On réaffiche l'image
                    for case in  cases_a_cocher[3:0:-1]:
                        if case.cochee :
                            case.cochee = False
                            case.cliqué()
                            break

            if event.type== MOUSEBUTTONUP: # quand je relache le bouton
                if event.button == 1: # 1= clique gauche
                    for case in cases_a_cocher:
                        # Si on clique sur un des objets à afficher
                        if case.get_rectangle().collidepoint(event.pos):
                            objet_cliqué = True
                            case.cliqué()
                if event.button == 3 : # Si on relache le bouton droit
                    #On recrée la fenetre mise à jour avec les nouvelles coordonnées
                    a,b = position_depart
                    c,d = event.pos
                    X_MIN,Y_MIN,X_MAX = X_MIN+(X_MAX-X_MIN)*min(a,c)/WIDTH,Y_MIN+(Y_MAX-Y_MIN)*min(b,d)/HEIGHT,X_MIN+(X_MAX-X_MIN)*max(a,c)/WIDTH
                    Y_MAX = Y_MIN+HEIGHT*(X_MAX-X_MIN)/WIDTH
                    # On réaffiche l'image
                    for case in  cases_a_cocher[3:0:-1]:
                        if case.cochee :
                            case.cochee = False
                            case.cliqué()
                            break
                    position_depart=None


            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3 : # Si j'appuye sur le bouton droit
                    position_depart=event.pos
        # On trace les points de convergence
        if cases_a_cocher[2].cochee or cases_a_cocher[3].cochee :
            fenetre.blit(pygame.image.load("output.png").convert(),(0,0))
        elif cases_a_cocher[1].cochee :
            fenetre.blit(pygame.image.load("outputNB.png").convert(),(0,0))
        # On affiche les cases
        for case in cases_a_cocher:
            case.dessiner(fenetre,font)
        # On met à jour la liste des points lorqu'on tient le bouton gauche de la souris appuyé
        if (not objet_cliqué) and pygame.mouse.get_pressed()[0] :
            # Si on clique sur un complexe c, on affiche les points de la suite tel que c est le complexe qu'on ajoute dans la fonction de Mandelbrot
            liste_points=convertir_complexes_to_points(mandelbrot_liste(convertir_point_to_complexe(pygame.mouse.get_pos()),120))
        # On trace les points de la suite
        if liste_points:
            tracer_ligne_brisee(liste_points,fenetre,cases_a_cocher[0].cochee)
        tracer_axes(fenetre)
        # Pour selectionner la zone à zoomer
        if not position_depart is None :
            a,b=position_depart
            c,d=pygame.mouse.get_pos()
            pygame.draw.rect(fenetre,(125,125,125),Rect(min(a,c),min(b,d),abs(c-a),abs(d-b)),1)
        # Les textes à afficher :
        fenetre.blit(font.render("Appuyer sur Escape pour réinitialiser le zoom",1,(0,0,0)),(10,HEIGHT-30))
        fenetre.blit(font.render("Clic droit pour selectionner la zone à agrandir",1,(0,0,0)),(10,HEIGHT-50))
        fenetre.blit(font.render(str(convertir_point_to_complexe(pygame.mouse.get_pos())),1,(0,0,0)),(WIDTH//2,10))



        pygame.display.flip() # Pour rafraichir l'affichage

    pygame.quit()
    exit()


if __name__ == "__main__" :
    #lancer()
    
    t0=time()
    creer_image()
    print(time()-t0)
    

