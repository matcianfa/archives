"""
Les différentes classes de joueurs (Random, humain, IA...)
"""
import random
from classes import Boite

# -------------------------- Classe générale Joueur

class Joueur:

    def __init__(self,numero):
        self.numero = numero
        self.couleur = (-1)**numero
        self.est_humain = False
        self.est_IA_boites = False

    def jouer(self,jeu,*args,**kwargs):
        """
        Renvoie le deplacement choisi sous la forme (ligne_depart,col_depart,ligne_arrivee,col_arrivee)
        """
        pass

    def maj_fin_partie(self,*args,**kwargs):
        pass

# -------------------------- Joueur Random

class Joueur_aleatoire(Joueur):

    def __init__(self,numero):
        super().__init__(numero)

    def jouer(self,jeu):
        return random.choice(jeu.deplacements_possibles)


# -------------------------- Joueur IA humain


class Joueur_humain(Joueur):

    def __init__(self,numero):
        super().__init__(numero)
        self.est_humain = True

    def jouer(self,jeu,*args,**kwargs):
        """
        Renvoie le deplacement choisi sous la forme (ligne_depart,col_depart,ligne_arrivee,col_arrivee)
        """
        pass


# -------------------------- Joueur IA Boites

class Joueur_IA_boites(Joueur):

    def __init__(self,numero):
        super().__init__(numero)
        self.liste_boites = []
        self.liste_coups_joues = [] # sous la forme (indice_boite,(ligne_depart,col_depart,ligne_arrivee,col_arrivee))
        self.est_IA_boites = True

    def jouer(self,jeu):
        """
        On cherche la boite correspondant à la grille en cours et on choisit une bille
        """
        for indice_boite,boite in enumerate(self.liste_boites):
            if boite.grille == jeu.grille:
                choix = boite.choisir_deplacement()
                break
        else:
            # Si on ne l'a pas trouvé, on crée une nouvelle boite
            nouvelle_boite = Boite(jeu.grille,self.couleur)
            indice_boite = len(self.liste_boites)
            self.liste_boites.append(nouvelle_boite)
            choix= nouvelle_boite.choisir_deplacement()
        self.liste_coups_joues.append((indice_boite,choix))
        return choix

    def maj_fin_partie(self,gagnant,*arg,**kwargs):
        """
        On retire les billes sur le dernier coup qui nous a fait perdre
        """
        if gagnant != self.numero : # Si on a perdu
            for indice_boite,coup_joue in self.liste_coups_joues[::-1] : # On les parcourt à l'envers
                for indice_coup,coup in enumerate(self.liste_boites[indice_boite].deplacements_possibles): # On cherche la bille à retirer
                    if coup == coup_joue :
                        self.liste_boites[indice_boite].billes_presentes[indice_coup] -= 1
                        break
                if not self.liste_boites[indice_boite].fonc_est_vide(): # Si la boite n'est pas vide, on arrete de retirer des billes
                    break
        self.liste_coups_joues = []


    def est_entraine(self):
        return ( self.liste_boites) and (sum(self.liste_boites[0].billes_presentes)<=0)