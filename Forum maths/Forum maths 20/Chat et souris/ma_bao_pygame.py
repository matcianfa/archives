# -*- coding: utf-8 -*

"""
Ma boite à outil pour pygame
"""

import pygame
from pygame.locals import *

#-------------------------------- Cases à cocher

class Case_a_cocher:

    dimension = 10
    decalage_case_texte = 8

    def __init__(self,position, texte = "",dim = dimension,cochee=False,fonction=None,groupe=None):
        """
        Indiquer la position, la dimension, le texte à afficher à coté, si la case est cochée ou pas,
        la fonction à lancer quand on la coche, et le numéro du groupe de la case (une seule case d'un même groupe cochée à la fois)
        """
        self.position = position
        self.dimension = dim
        self.texte = texte
        self.cochee = cochee
        self.fonction=fonction
        self.groupe = groupe


    def get_rectangle(self):
        """
        Donne le rectangle dans lequel est la case à cocher
        """
        return Rect(self.position,(self.dimension,self.dimension))

    def dessiner(self,fenetre,font,couleur=(0,0,0)):
        """
        Affiche la case et le texte à coté dans la fenetre, la police et la couleur précisées
        """
        # La case :
        pygame.draw.rect(fenetre,couleur,self.get_rectangle(),int(not self.cochee))
        # Le texte
        fenetre.blit(font.render(self.texte,1,couleur),(self.position[0]+self.dimension+self.decalage_case_texte,self.position[1]))

    def cliqué(self,liste_cases=[]):
        """
        Ce qu'il faut faire quand l'objet est cliqué
        """
        if not self.fonction is None and not self.cochee:
            self.fonction()
        if self.groupe is None or self.cochee:
            self.cochee = not self.cochee
        else:
            self.cochee = True
            for case in liste_cases :
                if case!= self and case.groupe == self.groupe:
                    case.cochee= False






