"""
Les pions blancs sont désignés par 1, noirs par -1, case vide par 0

"""

import random
import pygame
from pygame.locals import *


# -------------------- Constantes
PION_BLANC = 1
PION_NOIR = -1
VIDE = 0
VERT_CLAIR = (158,240,156)
VERT_FONCE = (98,198,95)
NOIR = (0,0,0)
BLANC = (255,255,255)
JAUNE = (255,255,0)
ROUGE = (255,0,0)
VERT = (0,255,0)
BLEU = (0,0,205)
ORANGE = (255,165,0)
FUCHSIA = (255,0,255)
VIOLET = (148,0,211)
BLEU_CLAIR = (0,255,255)
ECREVISSE = (255,228,196)
ROSE = (255,105,180)
GRIS = (192,192,192)
GRIS_CLAIR = (100,100,100)

LISTE_COULEURS = [JAUNE,ROUGE,VERT,BLEU,ORANGE,FUCHSIA,VIOLET,BLEU_CLAIR,ECREVISSE,ROSE]



# -------------------- Classe représentant le plateau du jeu

class Grille:

    def __init__(self,nb_lignes,nb_cols,blanc_en_bas = True):
        self.nb_lignes = nb_lignes
        self.nb_cols = nb_cols
        self.blanc_en_bas = blanc_en_bas
        self.pions = self.nouvelle_grille()


    def nouvelle_grille(self):
        grille = []
        couleurs = [-1]+([0]*(self.nb_lignes-2))+[1] if self.blanc_en_bas else [1]+([0]*(self.nb_lignes-2))+[-1]
        for ligne,couleur in enumerate(couleurs):
            ligne_pions = []
            for col in range(self.nb_cols):
                ligne_pions.append(couleur)
            grille.append(ligne_pions)
        return grille


    def deplacements_possibles_par_case(self,ligne,col):
        """
        Renvoie les cases (un couple (ligne,col)) vers lesquelles un déplacement est possible
        """
        couleur = self.pions[ligne][col]
        if couleur==0 : return []
        direction =-couleur if self.blanc_en_bas else couleur # sens du déplacement
        deplacements_possibles = []
        # Si on peut avancer
        try : # Pour esquiver les verifications sur la dimension de la grille
            if self.pions[ligne+direction][col] == VIDE:
                deplacements_possibles.append((ligne+direction,col))
        except IndexError:
            pass

        # Si on peut manger en diagonale
        for delta_col in [-1,1]:
            try :
                if col + delta_col>=0 and self.pions[ligne + direction][col + delta_col] == - couleur:
                    deplacements_possibles.append((ligne+direction,col+delta_col))
            except IndexError:
                pass
        return deplacements_possibles

    def deplacements_possibles_par_couleur(self,couleur):
        """
        Renvoie la listes des déplacements possibles sous la forme (ligne_depart,col_depart,ligne_arrivee,col_arrivee)
        """
        deplacements_possibles =[]
        for ligne in range(self.nb_lignes):
            for col in range(self.nb_cols):
                if self.pions[ligne][col] == couleur:
                    for (ligne_arrivee,col_arrivee) in self.deplacements_possibles_par_case(ligne,col):
                        deplacements_possibles.append((ligne,col,ligne_arrivee,col_arrivee))
        return deplacements_possibles


    def deplacer(self,ligne_depart,col_depart,ligne_arrivee,col_arrivee):
        """
        On suppose que le mouvement est possible
        """
        self.pions[ligne_arrivee][col_arrivee]=self.pions[ligne_depart][col_depart]
        self.pions[ligne_depart][col_depart] = VIDE


    def afficher_console(self):
        """
        Pour un affichage dans la console pour debug
        """
        for ligne in range(self.nb_lignes):
            print(*[self.pions[ligne][col] for col in range(self.nb_cols)])

    def copy(self):
        """
        Renvoie une deepcopy de la grille
        """
        nouvelle_grille = Grille(self.nb_lignes,self.nb_cols,self.blanc_en_bas)
        nouvelle_grille.pions = [ligne[:] for ligne in self.pions] #deepcopy
        return nouvelle_grille

    def est_gagnante(self):
        """
        Renvoie si un pion est arrivé chez l'adversaire
        """
        return any([self.pions[0][col] == -(-1)**self.blanc_en_bas for col in range(self.nb_cols)]) or any([self.pions[-1][col] == (-1)**self.blanc_en_bas for col in range(self.nb_cols)])

    def __eq__(self, grille2):
        """
        Deux grilles sont égales si la liste des pions est la même (le reste ne changeant pas de la partie)
        """
        return self.pions == grille2.pions




    # --------- Affichage

    def afficher(self,fenetre,x0,y0,dimension_case,ligne_case_selectionnee, col_case_selectionnee):
        """
        Affichage de la grille de jeu
        """
        x,y=x0,y0
        for ligne in range(self.nb_lignes):
            for col in range(self.nb_cols):
                couleur = VERT_CLAIR if (ligne+col)%2==0 else VERT_FONCE
                pygame.draw.rect(fenetre, couleur, (x, y, dimension_case, dimension_case)) # l'intérieur de la case
                pygame.draw.rect(fenetre, NOIR, (x, y, dimension_case, dimension_case),1) # Le bord de la case
                if self.pions[ligne][col] == PION_BLANC :
                    pygame.draw.circle(fenetre,BLANC , (x+dimension_case//2,y+dimension_case//2),dimension_case//3)
                elif self.pions[ligne][col] == PION_NOIR :
                    pygame.draw.circle(fenetre,NOIR , (x+dimension_case//2,y+dimension_case//2),dimension_case//3)
                if ligne == ligne_case_selectionnee and col == col_case_selectionnee and self.pions[ligne][col]!= VIDE: # On surligne la case selectionnee
                    pygame.draw.circle(fenetre,JAUNE , (x+dimension_case//2,y+dimension_case//2),dimension_case//3,3)

                x+= dimension_case
            x=x0
            y+=dimension_case



# -------------------- Classe Boite d'allumettes

class Boite():



    def __init__(self,grille,couleur_joueur):
        self.grille = grille.copy()                                                                 # La grille que la boite représente
        self.couleur_joueur = couleur_joueur                                                        # La couleur du joueur qui doit jouer
        self.deplacements_possibles = grille.deplacements_possibles_par_couleur(couleur_joueur)
        self.billes_presentes = [1]*len(self.deplacements_possibles)
        self.est_vide = False                              # Le nombre de billes correspondant aux deplacements possibles
        self.indice_derniere_bille_tiree = None


    def choisir_deplacement(self):
        """
        Tire une bille restante de la boite et renvoie le deplacement associé sous la forme (ligne_depart,col_depart,ligne_arrivee,col_arrivee)
        """
        if all([v<=0 for v in self.billes_presentes]):
            poids = None
        else:
            poids = self.billes_presentes
        indice = random.choices(range(len(self.deplacements_possibles)), weights=poids, k=1)[0]
        self.indice_derniere_bille_tiree = indice
        return self.deplacements_possibles[indice]

    def retirer_deplacement(self,deplacement):
        """
        Retire une bille correspondant au déplacement donné
        """
        for i,depl in enumerate(self.deplacements_possibles):
            if depl == deplacement:
                self.billes_presentes[i] = max(0,self.billes_presentes[i]-1)
                break

    def fonc_est_vide(self):
        reponse = sum(self.billes_presentes) <= 0
        self.est_vide = reponse
        return reponse

    # --------- Affichage

    def afficher(self,fenetre,x0,y0,image_fleche,jeu):
        """
        Affichage des boites
        """
        # --- Affichage des grilles
        x,y=x0,y0
        for ligne in range(self.grille.nb_lignes):
            for col in range(self.grille.nb_cols):
                couleur = VERT_CLAIR if (ligne+col)%2==0 else VERT_FONCE
                pygame.draw.rect(fenetre, couleur, (x, y, jeu.dimension_case_boite, jeu.dimension_case_boite)) # l'intérieur de la case
                pygame.draw.rect(fenetre, NOIR, (x, y, jeu.dimension_case_boite, jeu.dimension_case_boite),1) # Le bord de la case
                if self.grille.pions[ligne][col] == PION_BLANC :
                    pygame.draw.circle(fenetre,BLANC , (x+jeu.dimension_case_boite//2,y+jeu.dimension_case_boite//2),jeu.dimension_case_boite//3)
                elif self.grille.pions[ligne][col] == PION_NOIR :
                    pygame.draw.circle(fenetre,NOIR , (x+jeu.dimension_case_boite//2,y+jeu.dimension_case_boite//2),jeu.dimension_case_boite//3)
                x+= jeu.dimension_case_boite
            x=x0
            y+=jeu.dimension_case_boite

        # --- Affichage des flèches
        indice_couleur = 0
        for indice_depl,(ligne_depart,col_depart,ligne_arrivee,col_arrivee) in enumerate(self.deplacements_possibles):
            angle = 0
            coeff = jeu.coefficient_reduction_droit
            if col_depart == col_arrivee :
                if ligne_depart<ligne_arrivee :
                    angle = 180
                    coeff = jeu.coefficient_reduction_droit
                else:
                    angle = 0
                    coeff = jeu.coefficient_reduction_droit
            elif col_depart < col_arrivee:
                if ligne_depart<ligne_arrivee :
                    angle = -135
                    coeff = jeu.coefficient_reduction_oblique
                else:
                    angle = -45
                    coeff = jeu.coefficient_reduction_oblique
            else :
                if ligne_depart<ligne_arrivee :
                    angle = 135
                    coeff = jeu.coefficient_reduction_oblique
                else:
                    angle = 45
                    coeff = jeu.coefficient_reduction_oblique

            couleur = LISTE_COULEURS[indice_couleur] if self.billes_presentes[indice_depl]>0 else GRIS
            indice_couleur = (indice_couleur+ 1)%len(LISTE_COULEURS)
            img = pygame.transform.rotozoom(image_fleche,angle,coeff)
            img.fill(couleur, special_flags = pygame.BLEND_MULT)
            rect = img.get_rect()
            rect.center = x0+((col_depart+col_arrivee+1)*jeu.dimension_case_boite)//2,y0+((ligne_depart+ligne_arrivee+1)*jeu.dimension_case_boite)//2
            fenetre.blit(img,rect)

        # --- Affichage de la bille tirée au dernier coup
        if self.indice_derniere_bille_tiree is not None:
            x = x0 + (jeu.dimension_case_boite*self.grille.nb_cols)//2
            y = y0 + int(jeu.dimension_case_boite*(self.grille.nb_lignes+0.5))
            pygame.draw.circle(fenetre,LISTE_COULEURS[self.indice_derniere_bille_tiree%len(LISTE_COULEURS)] , (x,y),jeu.dimension_case_boite//3)



# -------------------- Classe représentant le jeu

class Jeu:

    def __init__(self,joueur_blanc,joueur_noir,nb_lignes,nb_cols,dimension_case_boite,coefficient_reduction_droit,coefficient_reduction_oblique):
        self.joueurs = [joueur_blanc,joueur_noir]
        self.nb_lignes = nb_lignes
        self.nb_cols = nb_cols
        self.blanc_en_bas = True
        self.dimension_case_boite = dimension_case_boite
        self.coefficient_reduction_droit = coefficient_reduction_droit
        self.coefficient_reduction_oblique = coefficient_reduction_oblique
        self.entrainement_auto = False
        self.n_tick = 5 # Le rafraichissement de l'ecran
        self.score = [0,0]
        self.compteur_partie = 1
        self.reset()

    def reset(self,total = False):
        if self.joueurs[1].est_humain: self.blanc_en_bas = False
        else :  self.blanc_en_bas = True
        self.grille = Grille(self.nb_lignes,self.nb_cols,self.blanc_en_bas)
        self.n_joueur_en_cours = 0                              # Le numero du joueur qui doit jouer
        self.deplacements_possibles = self.grille.deplacements_possibles_par_couleur((-1)**self.n_joueur_en_cours) # Pour garder en mémoire les déplacements possibles du coup en cours
        self.partie_terminee = False



        # Si un joueur est une boite, on reset tous les derniers coups joués mémorisés dans les boites
        for joueur in self.joueurs:
            if joueur.est_IA_boites:
                if total :
                    joueur.liste_boites = []
                else:
                    for boite in joueur.liste_boites:
                        boite.indice_derniere_bille_tiree  = None


    def lancer_console(self):
        self.reset()
        self.grille.afficher_console()
        while self.deplacements_possibles and not self.grille.est_gagnante():
            deplacement_propose = (-1,-1,-1,-1)
            while deplacement_propose not in self.deplacements_possibles :
                deplacement_propose = self.joueurs[self.n_joueur_en_cours].jouer(self)
            print("Le joueur {} déplace le pion ({},{}) vers ({},{})".format(self.n_joueur_en_cours,*deplacement_propose))
            self.jouer(*deplacement_propose)
            self.grille.afficher_console()

        gagnant = 1-self.n_joueur_en_cours
        for j in self.joueurs:
            j.maj_fin_partie(gagnant)
        print("Le gagnant est le joueur {}".format(["BLANC","NOIR"][gagnant]))



    def jouer(self, ligne_depart,col_depart,ligne_arrivee,col_arrivee):
        """
        On joue le coup et met à jour
        """
        self.grille.deplacer(ligne_depart,col_depart,ligne_arrivee,col_arrivee)
        self.n_joueur_en_cours = 1- self.n_joueur_en_cours
        self.deplacements_possibles = self.grille.deplacements_possibles_par_couleur((-1)**self.n_joueur_en_cours)








# -------------------- Pour Debug

if __name__=="__main__" :
    pass





