

"""
Ma boite à outil pour pygame
"""

import pygame
from pygame.locals import *

import time

# -------------------------------- Constantes
GRIS = (145,145,145)
NOIR = (0,0,0)
BLANC= (255,255,255)
GRIS_CLAIR = (100,100,100)

# -------------------------------- Cases à cocher

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

    def fonction_activation(self,liste_cases=[]):
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


# -------------------------------- Boutons

class Bouton:

    def __init__(self,position,dimension,font, texte = "",couleur = GRIS,fonction_activation = None,  afficher = True):
        self.position = position
        self.texte = texte
        self.rect = pygame.Rect(position,dimension)
        self.dimension = dimension
        self.fonction_activation = fonction_activation
        self.font = font
        self.couleur = couleur
        self.afficher = afficher


    def dessiner(self,fenetre):
        """
        Affiche le bouton et le texte à coté dans la fenetre, la police et la couleur précisées
        """
        if self.afficher:
            # Le bouton :
            pygame.draw.rect(fenetre,self.couleur,self.rect)
            # Le texte
            text = self.font.render(self.texte,1,NOIR)
            rect_text = text.get_rect(center = self.rect.center)
            fenetre.blit(text,rect_text)

    def update(self,event_list,*args,**kwargs):
        if "args_fonction" in kwargs: args_fonction = kwargs["args_fonction"]
        else : args_fonction = []
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mpos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mpos):
                    self.fonction_activation(*args_fonction)



# --------------------------------- Menu déroulant

class Menu_deroulant():

    def __init__(self, x, y, w, h, couleur, couleur_selection, font, options, element_choisi = 0,fonction_modif=None):
        self.couleur = couleur                          # La couleur de fond
        self.couleur_selection = couleur_selection      # La couleur si on passe la souris dessus
        self.rect = pygame.Rect(x, y, w, h)             # Le rectangle qui l'entoure
        self.font = font                                # La police de caractère
        self.options = options                          # La liste des intitulés du menu
        self.element_choisi = element_choisi            # Le numero de l'element choisi
        self.afficher_menu = False                      # Si on déroule le menu
        self.menu_actif = False                         # Si le menu est survolé avec la souris
        self.option_activee = -1                        # L'option survolee avec la souris
        self.fonction_modif = fonction_modif            # La fonction à lancer si on a modifié le choix

    def dessiner(self, surf):
        pygame.draw.rect(surf, self.couleur_selection if self.menu_actif else self.couleur, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.options[self.element_choisi], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.afficher_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.couleur_selection if i == self.option_activee else self.couleur, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.options))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list,*args,**kwargs):
        if "args_fonction" in kwargs: args_fonction_modif = kwargs["args_fonction"]
        else : args_fonction_modif = []
        mpos = pygame.mouse.get_pos()
        self.menu_actif = self.rect.collidepoint(mpos)

        self.option_activee = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.option_activee = i
                break

        if not self.menu_actif and self.option_activee == -1:
            self.afficher_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_actif:
                    self.afficher_menu = not self.afficher_menu
                elif self.afficher_menu and self.option_activee >= 0:
                    if self.element_choisi != self.option_activee and self.fonction_modif is not None :
                        self.element_choisi = self.option_activee
                        self.fonction_modif(self,*args_fonction_modif)
                    self.element_choisi = self.option_activee
                    self.afficher_menu = False
                    return self.option_activee
        return -1

# ----------------------------------- Text input

class Text_input_box():
    def __init__(self, x, y, w, font, text = "",couleur = BLANC,fonction_activation = None):
        self.couleur = couleur
        self.x = x
        self.y = y
        self.width = w
        self.rect = pygame.Rect(x,y,w,20)
        self.font = font
        self.fonction_activation = fonction_activation
        self.active = False
        self.text = text

    def dessiner(self,fenetre):
        texte = self.font.render(self.text, True, NOIR)
        self.rect = pygame.Rect(self.x,self.y,max(self.width, texte.get_width()+10), texte.get_height()+10)
        pygame.draw.rect(fenetre,self.couleur,self.rect)
        fenetre.blit(texte,(self.x+5,self.y+5))

    def update(self, event_list,*args,**kwargs):
        if "args_fonction" in kwargs: args_fonction = kwargs["args_fonction"]
        else : args_fonction = []
        valider_choix = False
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.active:
                    self.active = self.rect.collidepoint(event.pos)
                elif not self.rect.collidepoint(event.pos):
                    valider_choix = True
                    self.active = False
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    valider_choix = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        if valider_choix and self.text.isdigit():
            self.fonction_activation(int(self.text),*args_fonction)

# ----------------------------------- Image cliquable

class Image_cliquable():
    def __init__(self,x,y,liste_image,dimension = None):
        self.x = x
        self.y = y
        self.liste_image = []
        if dimension is not None :
            for im in liste_image :
                self.liste_image.append(pygame.transform.scale(im,(dimension)))
        self.image = self.liste_image[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def dessiner(self,fenetre):
        fenetre.blit(self.image,self.rect)

    def changer_image(self,numero):
        self.image = self.liste_image[numero]