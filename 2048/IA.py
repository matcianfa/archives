"""
Script d'IA pour le 2048
Prend en entrée une matrice (normale, pas numpy) de nombres qui correspondent à la puissance de 2 (donc entre 1 et 16).
Le 0 correspond à une case vide.
La sortie donne le mouvement à effectuer sous la forme de 0 pour la droite
puis on tourne dans le sens trigo : 1 pour le haut, 2 pour la gauche et 3 pour le bas.

Le principe de l'IA est en gros un algorithme à la Monte Carlo :
On teste au hasard des parties jusqu'à la fin et on compte quelle direction donne le meilleur score en moyenne
"""
from random import randint




#-------------------------- Fonctions auxiliaires

def suppr0(liste):
    """
    Supprime les 0 d'une liste
    """
    return [n for n in liste if n!=0]

def conc(liste):
    """
    Concatene les valeurs identiques selon la direction
    """
    for i in range(len(liste)-1,0,-1):
        if liste[i]==liste[i-1]:
            liste[i]+=1
            liste[i-1]=0
    return liste

def arranger(liste,renverser=False):
    if renverser: liste=liste[::-1]
    liste_reduite=suppr0(conc(suppr0(liste)))
    liste_reduite=[0]*(len(liste)-len(liste_reduite))+liste_reduite
    if renverser : liste_reduite.reverse()
    return liste_reduite


def appliquer_mvt(grille,mvt,N=4):
    """
    Fonction qui donne la grille obtenue après avoir effectué un mouvement.
    On fait chaque cas séparément pour optimiser en temps car les astuces risquent d'être gourmandes en temps
    (Il faut faire ENORMEMENT de test pour une méthode Monte Carlo donc il faut optimiser autant que faire se peut)
    Si j'ai bien compris : A chaque mouvement on pousse tout le monde, on regroupe les adjacentes identiques et on repousse.
    """
    # Si le mouvement ne fait rien, alors il n'apparait pas de nouvelle case
    au_moins_une_modif=False
    # On regarde les 4 cas
    if mvt==0: # A droite
        for i,ligne in enumerate(grille):
            arr=arranger(ligne)
            for j in range(N):
                if not au_moins_une_modif and grille[i][j]!=arr[j] : au_moins_une_modif=True
                grille[i][j]=arr[j]
    elif mvt==2: # A gauche
        for i,ligne in enumerate(grille):
            arr=arranger(ligne,True)
            for j in range(N):
                if not au_moins_une_modif and grille[i][j]!=arr[j] : au_moins_une_modif=True
                grille[i][j]=arr[j]
    elif mvt==1: # En haut
        for j in range(N):
            arr=arranger([grille[i][j] for i in range(N)],True)
            for i in range(N):
                if not au_moins_une_modif and grille[i][j]!=arr[i] : au_moins_une_modif=True
                grille[i][j]=arr[i]
    elif mvt==3: # En Bas
        for j in range(N):
            arr=arranger([grille[i][j] for i in range(N)])
            for i in range(N):
                if not au_moins_une_modif and grille[i][j]!=arr[i] : au_moins_une_modif=True
                grille[i][j]=arr[i]
    return au_moins_une_modif

def est_complete(grille):
    """
    Fonction qui renvoie true s'il n'y a plus de 0 dans la grille, false sinon
    """
    for ligne in grille:
        for n in ligne:
            if n==0 : return False
    return True


def ajouter_case(grille):
    """
    Fonction qui ajoute un 1 ou un 2 aléatoirement dans la grille (ce qui se passe après chaque mouvement)
    Modifie la grille directement
    """
    # S'il reste au moins un 0
    if not est_complete(grille):
        N=len(grille)
        # On cherche une case au hasard jusqu'à tomber sur 0
        l,c=randint(0,N-1),randint(0,N-1)
        while grille[l][c]!=0:
            l,c=randint(0,N-1),randint(0,N-1)
        grille[l][c]=randint(1,2)

def donner_score(grille):
    """
    Donne le score
    Surement optimisable avec du calcul bit à bit mais au final, elle ne sert que nb_essais fois
    """
    return sum([sum([2**n for n in ligne]) for ligne in grille])

def est_fini(grille,N=4):
    """
    Renvoie True si plus aucun mouvement est possible
    """
    # Si elle n'est pas complete, ce n'est pas fini
    if not est_complete(grille): return False
    # S'il y a deux nombres egaux à coté, ce n'est pas fini
    for ligne in range(N):
        for col in range(N):
            try:
                if grille[ligne][col]==grille[ligne][col+1]: return False
                if grille[ligne][col]==grille[ligne+1][col]: return False
            except : pass
    return True


def afficher_grille(grille):
    """
    pour debug : Affiche juste les nombres dans la grille
    """
    for ligne in grille:
        print(" ".join([str(n) for n in ligne]))

#------------------------- Fonction principale

def donner_direction(grille,nb_essais):
    """
    Fonction qui cherche la meilleur direction à prendre
    """
    # Liste des scores et du nombre d'essais effectués par direction
    scores=[0]*4
    essais=[0]*4

    compteur=0
    N=len(grille)

    while compteur<nb_essais :
        compteur+=1
        # Pour sortir de la boucle de recherche
        fini = False
        # On choisit la première direction (dont il faudra se souvenir pour le score)
        premiere_direction=randint(0,3)
        # On fait une copie de notre grille d'origine
        grille_temp=[ligne.copy() for ligne in grille]
        # On applique le changement.
        if appliquer_mvt(grille_temp,premiere_direction,N):
            fini=est_fini(grille_temp,N)
            ajouter_case(grille_temp)
            while not fini :
                # On joue au hasard tant qu'on n'a pas fini
                if appliquer_mvt(grille_temp,randint(0,3),N) :
                    ajouter_case(grille_temp)
                fini=est_fini(grille_temp,N)
            # On modifie le tableau des scores et du nombre d'essais
            scores[premiere_direction]+=donner_score(grille_temp)
            essais[premiere_direction]+=1

        #afficher_grille(grille_temp)

    # Maintenant qu'on a fait nos essais aleatoires, on choisit la direction ayant le plus gros score en moyenne
    maximum=0
    direction=-1
    for i in range(4):
        try:
            temp = scores[i]/essais[i]
            if temp > maximum:
                maximum = temp
                direction = i
        except: pass

    #print(scores)
    #print(essais)
    return direction





if __name__ == '__main__': # Pour le debug
    pass
    """
    # Simule une partie
    grille=[[0 for _ in range(4)] for __ in range(4)]
    ajouter_case(grille)
    ajouter_case(grille)
    afficher_grille(grille)
    print("------------------------")
    compteur = 0
    while not est_fini(grille):
        print("Coup n°",compteur)
        compteur+=1
        direction=donner_direction(grille,500)
        print(direction)
        appliquer_mvt(grille,direction)
        ajouter_case(grille)
        afficher_grille(grille)
        print("------------------------")
    """
