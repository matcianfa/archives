import pygame
from pygame.locals import *




class Case:
    """ 
    Classe pour les cases du jeu :
    Couleur : 0 (Noir) ou 1 (Blanc)
    numero : un nombre entre 0 et dimension_plateau²
    x et y : coordonnées du coin en haut à gauche
    point_rouge : Vrai si on dessine un point rouge pour désigner la solution
    """
    
    marge=200 # Espace entre le bord de l'écran et le bord du plateau
    x_0=y_0 = 0 # Le coin en haut à gauche du plateau
    dim_case = 0 # La dimension des cases
    x_1=y_1=0 # Le coin en bas à droite
    fontsmall=None
    
    def init(cls,dimension_plateau,dim_ecran):
        cls.dim_case=(min(dim_ecran)-cls.marge)//dimension_plateau
        cls.x_0=(dim_ecran[0]-dimension_plateau*cls.dim_case)//2
        cls.y_0=(dim_ecran[1]-dimension_plateau*cls.dim_case)//2
        cls.x_1=(dim_ecran[0]+dimension_plateau*cls.dim_case)//2
        cls.y_1=(dim_ecran[1]+dimension_plateau*cls.dim_case)//2
        

    init = classmethod(init)
    
    def __init__(self,couleur,numero,dimension_plateau):
        self.couleur = couleur
        self.numero = numero
        self.x = Case.x_0+(numero%dimension_plateau)*Case.dim_case
        self.y = Case.y_0 +(numero//dimension_plateau)*Case.dim_case
        self.point_rouge=False
        self.texte_sol=0
        
        
    def dessiner(self,fenetre,modulo):
        """
        Fonction pour afficher la case
        """
        pygame.draw.rect(fenetre, (255*self.couleur//(modulo-1), 255*self.couleur//(modulo-1), 255*self.couleur//(modulo-1)), (self.x, self.y, Case.dim_case, Case.dim_case))
        #Créer un cadre gris autour:
        pygame.draw.rect(fenetre, (150, 150, 150), (self.x, self.y, Case.dim_case, Case.dim_case),2)
        if self.point_rouge : 
            pygame.draw.circle(fenetre,(255,0,0) , (self.x+Case.dim_case//2,self.y+Case.dim_case//2),5)
        if self.texte_sol:
            text=Case.fontsmall.render(str(self.texte_sol),1,(255,255,255))
            fenetre.blit(text,text.get_rect(center=(self.x+Case.dim_case//2, self.y+Case.dim_case//2)))
        
    def afficher_numero(self,fenetre,font):
        """
        Fonction pour afficher le numero de la case
        """
        text=font.render(str(self.numero),1,(150,150,150))
        fenetre.blit(text,text.get_rect(center=(self.x+Case.dim_case//2, self.y+Case.dim_case//2)))
        
    def inverser(self,modulo):
        self.couleur=(self.couleur+1)%modulo