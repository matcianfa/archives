# -*- coding: utf-8 -*

import pygame
from pygame.locals import *
import numpy as np
from math import *

from ma_bao_pygame import *

# paramètres modifiables
dimension_fenetre = (800, 600)
vitesse = 2 # vitesse de la souris
rapport_vit = 4 # La valeur du rapport vitesse_chat/vitesse_souris
dim_souris,coeff_larg_souris = 7, 0.6

#------------------------------- Mes fonctions auxiliaires

def distance2(xa,ya,xb,yb):
    """
    Renvoie la distance euclidienne au carré entre A et B
    """
    return (xb-xa)**2 + (yb-ya)**2

def rotation(centre_x,centre_y,angle,x,y):
    """
    renvoie les coordonnées du résultat de la rotation du point de coordonnées (x,y) par la rotation d'angle et centre donnés
    """
    return ((x-centre_x)*cos(angle) - (y-centre_y)*sin(angle) + centre_x, (x-centre_x)*sin(angle)+(y-centre_y)*cos(angle)+centre_y)

#------------------------------- Mes classes

class Piscine:

    def __init__(self,x,y,rayon):
        self.x = x
        self.y = y
        self.rayon = rayon

    def dessiner(self,fenetre):
        pygame.draw.circle(fenetre, (0, 163, 255) , (self.x,self.y), self.rayon)  # L'intérieur
        pygame.draw.circle(fenetre, (0, 0, 0) , (self.x,self.y), self.rayon,1)    # Le rebord


class Chat:

    def __init__(self,piscine,angle):
        self.angle = angle
        self.vitesse = rapport_vit*vitesse
        self.x = int(piscine.x + piscine.rayon*cos(angle))
        self.y = int(piscine.y - piscine.rayon*sin(angle))

    def dessiner(self,piscine,fenetre,font):
        # On dessine le chat comme un point
        pygame.draw.circle(fenetre, (0, 0, 0) , (int(self.x),int(self.y)), 4)
        # Le texte
        text=font.render("C",1,(0,0,0))
        fenetre.blit(text,text.get_rect(center=(int(self.x+ (self.x-piscine.x)*0.05),int(self.y+ (self.y-piscine.y)*0.05))))

    def bouger(self,piscine,souris):
        """
        Bouge en direction de la souris le long de la piscine.
        """
        # u, v resp vecteur centre, souris et centre, chat
        ux,uy = souris.x-piscine.x,souris.y-piscine.y
        vx,vy = self.x - piscine.x, self.y - piscine.y
        determinant = (souris.x-self.x)*vy-(souris.y-self.y)*vx
        norme_u, norme_v =sqrt(ux**2+uy**2),sqrt(vx**2+vy**2)
        if norme_u!=0 and norme_v!=0 :
            angle = acos(max(-1,min(1,(ux*vx+uy*vy)/(norme_u*norme_v)))) # L'angle entre la souris et le chat par rapport au centre de la piscine
        else:
            angle = 7
        self.angle+= copysign(min(self.vitesse/piscine.rayon,angle),determinant)
        self.x = piscine.x+piscine.rayon*cos(self.angle)
        self.y = piscine.y-piscine.rayon*sin(self.angle)




class Souris:

    def __init__(self,piscine):
        self.x = piscine.x
        self.y = piscine.y
        self.vitesse = vitesse

    def dessiner(self,chat,fenetre,font,cible):
        """
        # On dessine la souris comme un point
        pygame.draw.circle(fenetre, (100, 100, 100) , (int(self.x),int(self.y)), 4)
        """
        # On dessine la souris comme un triangle
        cible_x,cible_y=cible
        norme = sqrt((cible_x-self.x)**2 + (cible_y-self.y)**2)
        if norme !=0 :
            ux =dim_souris*(cible_x-self.x)/norme
            uy = dim_souris*(cible_y-self.y)/norme
            # Le triangle
            x_1 = self.x + ux
            y_1 = self.y + uy
            x_2 = self.x + coeff_larg_souris*( - ux - sqrt(3)*uy)/2
            y_2 = self.y + coeff_larg_souris*(sqrt(3)*ux- uy)/2
            x_3 = self.x + coeff_larg_souris*( - ux + sqrt(3)*uy)/2
            y_3 = self.y + coeff_larg_souris*(-sqrt(3)*ux- uy)/2
            pygame.draw.polygon(fenetre, (100, 100, 100) , ((x_1,y_1),(x_2,y_2),(x_3,y_3)))
        else : # Si la norme vaut 0 on dessine un point (car pas de cible)
            pygame.draw.circle(fenetre, (100, 100, 100) , (int(self.x),int(self.y)), 4)
        # Le texte
        text=font.render("S",1,(0,0,0))
        dx,dy=self.x-chat.x,self.y-chat.y
        n = sqrt(dx**2+dy**2)
        fenetre.blit(text,text.get_rect(center=(int(self.x + dx/n*15.),int(self.y + dy/n*15))))

    def bouger(self,x,y):
        if not (x is  None or ( x==self.x and y==self.y)):
            norme = sqrt((x-self.x)**2+(y-self.y)**2)
            self.x += (x-self.x)*min(vitesse,norme)/norme
            self.y += (y-self.y)*min(vitesse,norme)/norme


#------------------------------- Fonction principale

def main():
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

    #---- Les constantes et variables
    # Pour la piscine :
    centre_x,centre_y = dimension_fenetre[0]//2+50,dimension_fenetre[1]//2
    rayon = min(centre_x,centre_y)-50
    animation = False
    cible_souris_x, cible_souris_y = (0,0) # La position ciblée pour la souris

    #---- Les éléments
    piscine = Piscine(centre_x,centre_y,rayon)
    chat = Chat(piscine,pi/4)
    souris = Souris(piscine)
    trace=[] # La trace laissée par la souris
    liste_points_favorables = []

    #---- Les cases à cocher
    cases_a_cocher = []
    cases_a_cocher.append(Case_a_cocher((10,10),"Stratégie n°1",groupe = 1))
    cases_a_cocher.append(Case_a_cocher((10,30),"Stratégie n°2",groupe = 1))
    cases_a_cocher.append(Case_a_cocher((10,50),"Stratégie n°3",groupe = 1))
    cases_a_cocher.append(Case_a_cocher((20,70),"Afficher cas favorables"))
    cases_a_cocher.append(Case_a_cocher((10,90),"Stratégie n°4",groupe = 1))
    cases_a_cocher.append(Case_a_cocher((20,110),"Afficher cas favorables"))

    #------------- Boucle de jeu

    continuer=1
    while continuer:
        #On efface l'écran
        fenetre.fill((255,255,255))
        pygame.time.Clock().tick(30) # Pour éviter de trop rafraichir
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT :     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle
            if event.type == KEYDOWN :
                if event.key==K_SPACE:
                    animation = not animation
                    liste_points_favorables = []
                    cases_a_cocher[3].cochee = False # On decoche
            if event.type == MOUSEBUTTONDOWN :
                trace=[] # On efface la trace dès qu'on appuie sur un bouton
                if event.button == 3 : # Click droit de la souris
                    animation = False
                    m_x,m_y = event.pos
                    # Si on clique à l'intérieur de la piscine avec le bouton droit, on y déplace la souris
                    if (m_x-piscine.x)**2 + (m_y-piscine.y)**2 < piscine.rayon**2 :
                        souris.x,souris.y = m_x,m_y
            if event.type== MOUSEBUTTONUP: # quand je relache le bouton
                if event.button == 1: # 1= clique gauche

                    for case in cases_a_cocher:
                        # Si on clique sur un des objets à afficher
                        if case.get_rectangle().collidepoint(event.pos):
                            case.cliqué(cases_a_cocher)


        # On affiche ce qui doit l'être
        piscine.dessiner(fenetre)

        # ------- Les stratégies
        # ------- Affichage des cas favorables de la strategie 3
        if cases_a_cocher[3].cochee:
            animation = False
            if not liste_points_favorables:
                for x in range(piscine.x-piscine.rayon,piscine.x+piscine.rayon+1):
                    for y in range(piscine.y-piscine.rayon,piscine.y+piscine.rayon+1):
                        if distance2(x,y,piscine.x,piscine.y)< piscine.rayon**2: # Si on est dans la piscine
                            u_x,u_y = x-piscine.x,y-piscine.y
                            v_x,v_y = chat.x-piscine.x,chat.y-piscine.y
                            norme_u = sqrt(u_x**2 + u_y**2)
                            if norme_u !=0 :
                                cible_x = piscine.x + piscine.rayon*(x-piscine.x)/norme_u
                                cible_y = piscine.y + piscine.rayon*(y-piscine.y)/norme_u
                            else : continue
                            #print(x,y,4*(piscine.rayon-norme_u),piscine.rayon*acos((u_x*v_x + u_y*v_y)/(norme_u*sqrt(v_x**2+v_y**2))))
                            if 4*(piscine.rayon-norme_u) < piscine.rayon*acos(min(1,max(-1,(u_x*v_x + u_y*v_y)/(norme_u*sqrt(v_x**2+v_y**2)))) ):
                                liste_points_favorables.append((x,y))
            for point in liste_points_favorables:
                fenetre.set_at(point,(100, 163, 255))
        # ------- Affichage cas favorables de la strategie 4
        if cases_a_cocher[5].cochee :
            pygame.draw.circle(fenetre,(255,0,0),(piscine.x,piscine.y),piscine.rayon//4,1)


        # ------- Gestion de la direction à suivre par la souris (prioritaire sur les strategies)
        if pygame.mouse.get_pressed()[0] : # Si bouton gauche enfoncé de la souris, la souris s'y dirige (Prioritaire sur la stratégie choisie
            m_x,m_y = pygame.mouse.get_pos()
            if (m_x-piscine.x)**2 + (m_y-piscine.y)**2 < (piscine.rayon+ 50)**2  : # Si on click pas trop loin de la piscine, on dit à la souris d'y aller
               cible_souris_x,cible_souris_y = m_x,m_y
        # ------ Strategie 1 : on fait toujours dos au chat
        elif cases_a_cocher[0].cochee:
            alpha = 2 *atan2((chat.y-souris.y),(chat.x-souris.x))
            cible_souris_x = int(-cos(alpha) * (chat.x-piscine.x) - sin(alpha) * (chat.y-piscine.y) + piscine.x)
            cible_souris_y = int(-sin(alpha) * (chat.x-piscine.x) + cos(alpha) * (chat.y-piscine.y) + piscine.y)
            # On dessine le trait
            pygame.draw.line(fenetre,(160,60,40),(chat.x,chat.y),(cible_souris_x,cible_souris_y))
            trace.append((int(souris.x),int(souris.y)))
        # ------ Strategie 2 : On vise toujours le point diametralement opposé au chat
        elif cases_a_cocher[1].cochee:
            cible_souris_x = 2 * piscine.x - chat.x
            cible_souris_y = 2 * piscine.y - chat.y
            pygame.draw.line(fenetre,(160,60,40),(chat.x,chat.y),(cible_souris_x,cible_souris_y))
            trace.append((int(souris.x),int(souris.y)))
        # ------ Strategie 3 : On va au plus proche du bord
        elif cases_a_cocher[2].cochee :
            norme = sqrt((piscine.x-souris.x)**2 + (piscine.y-souris.y)**2)
            if norme !=0 :
                cible_souris_x = piscine.x + piscine.rayon*(souris.x-piscine.x)/norme
                cible_souris_y = piscine.y + piscine.rayon*(souris.y-piscine.y)/norme
            else : # Si la norme est nulle on va à l'opposé du chat
                cible_souris_x = 2 * piscine.x - chat.x
                cible_souris_y = 2 * piscine.y - chat.y
            trace.append((int(souris.x),int(souris.y)))
            pygame.draw.line(fenetre,(160,60,40),(piscine.x,piscine.y),(cible_souris_x,cible_souris_y))
        # ------ Strategie 4 : On tourne en rond
        elif cases_a_cocher[4].cochee :
            ux,uy=souris.x-piscine.x,souris.y-piscine.y
            vy,vx=chat.y-piscine.y,chat.x-piscine.x
            determinant = ux*vy-uy*vx
            norme_u, norme_v =sqrt(ux**2+uy**2),sqrt(vx**2+vy**2)
            if norme_u!=0 and norme_v!=0 :
                angle = acos(max(-1,min(1,(ux*vx+uy*vy)/(norme_u*norme_v)))) # L'angle entre la souris et le chat par rapport au centre de la piscine
                cible_souris_x,cible_souris_y=rotation(piscine.x,piscine.y,-copysign(vitesse/norme_u,determinant),souris.x,souris.y)
                if abs(angle-pi)<0.01 : animation = False
            pygame.draw.line(fenetre,(160,60,40),(piscine.x,piscine.y),(chat.x,chat.y))
            pygame.draw.line(fenetre,(160,60,40),(piscine.x,piscine.y),(souris.x,souris.y))


        # Si on est en mode animation, on fait bouger
        if animation :
            chat.bouger(piscine,souris)
            souris.bouger(cible_souris_x,cible_souris_y)


        # On affiche ce qui doit l'être
        for p in trace : # On affiche la trace
            pygame.draw.circle(fenetre, (200, 200, 200) , p, 1)
        fenetre.set_at((centre_x,centre_y),(0,0,0))
        chat.dessiner(piscine,fenetre,font)
        souris.dessiner(chat,fenetre,font,(cible_souris_x,cible_souris_y))


        # Affichage des cases
        for case in cases_a_cocher:
            case.dessiner(fenetre,font)



        if distance2(souris.x,souris.y,piscine.x,piscine.y)>= piscine.rayon**2-1: # Si la souris a touché le bord, c'est gagné
                    animation = 0
                    if distance2(souris.x,souris.y,chat.x,chat.y)>16 :
                        text=font_victoire.render("Gagné !",1,(0,0,255))
                        fenetre.blit(text,text.get_rect(center=(centre_x,centre_y)))
                    else :
                        text=font_victoire.render("Perdu !",1,(255,0,0))
                        fenetre.blit(text,text.get_rect(center=(centre_x,centre_y)))



        pygame.display.flip() # Pour rafraichir l'affichage


    pygame.quit()
    exit()



#----------------------------------

if __name__ == "__main__":
    pass
    main()