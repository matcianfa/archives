"""
Script à lancer pour jouer automatiquement à Word Blitz ou à Boggle
Il faudra surement modifier les valeurs des coordonnées des lettres dans le fichier capture.py
Un conseil : Lancer le script une première fois à vide pour charger le dictionnaire puis
ensuite lancer la fonction lancer() dans la console.
Il faut lancer dès que la grille est lisible (c'est à dire sans pertubation devant
La lecture graphique est un peu longue donc compter 10-15 sec avant le réel début de l'automatisation.

!!! IMPORTANT !!!
Comme l'ordinateur n'a pas le temps de faire tous les mots, il va continuer même quand le temps est écoulé
Pour arreter la souris, il faut aller très rapidement dans le coin haut gauche de l'écran,
ca arretera le script.
Vous pouvez aussi mettre le temps (en seconde) comme argument de lancer() pendant lequel le script va s'executer
"""

import pyautogui as ag
from time import time

import capture # Perso : Pour capturer les données à l'écran
import IA # Perso : permet de générer les réponses possibles sur la grille

import pickle #Pour sauvegarder des classes
from Generer_automate import Noeud # La classe qui a permis de faire le dictionnaire sous forme d'automate. Indispensable de l'importer pour pouvoir réouvrir sa sauvegarde

# On charge le dictionnaire (sauvegardé sous forme d'automate (cf le fichier Generer_automate.py))
# !!!! Un peu long à charger
dico=pickle.load(open('automate', 'rb')) # dico avec tous les mots
# On va découper la recherche en 2 : Les mots de plus de 8 lettres puis si il reste du temps, les mots entre 5 et 7 lettres
#dico=pickle.load(open('automate_plus_de_8_lettres', 'rb'))  # dico avec tous les mots de plus de 5 lettres pour faire plus de points
#dico2=pickle.load(open('automate_entre_5_et_7_lettres', 'rb'))
#dico3=pickle.load(open('automate_moins_de_4_lettres', 'rb'))



def cliquer(liste):
    """
    Fonction qui, à une liste de coordonnées dans la grille (donc entre 0 et 3),
    clique sur l'écran le long du chemin donné.
    """
    if liste:
        # On clique sur la première lettre
        i,j=liste.pop(0)
        ag.mouseDown(x=capture.centre_lettre_x+j*capture.ecart_x, y=capture.centre_lettre_y+i*capture.ecart_y)
        for i,j in liste :
            ag.moveTo(x=capture.centre_lettre_x+j*capture.ecart_x, y=capture.centre_lettre_y+i*capture.ecart_y)
        ag.mouseUp()

def lancer(temps=125):
    t0=time()
    # On récupère les données
    grille=capture.capturer()

    # On cherche dans le dictionnaire
    for mot in IA.donner_mot(grille,dico) :
        cliquer(mot)
        if time()-t0> temps : break # On s'arrete si on dépasse le temps.


"""
if __name__ == '__main__':




    grille=[["A","M","O","T"],["N","O","S","I"],["E","S","W","X"],["Z","S","E","J"]]
    for mot in IA.donner_mot(grille,dico) :
        cliquer(mot)
"""
