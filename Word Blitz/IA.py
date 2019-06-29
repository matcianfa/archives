"""
L'idée de cette IA est assez simple :
On teste tous les mots valides qu'on peut créer cases après cases.
Pour gagner du temps, on génère les mots valides au fur et à mesure en créant un générateur (en utilisant yield au lieu de return)
Toujours pour gagner du temps, on n'utilise pas directement le dictionnaire pour voir si le mot existe
mais on teste au fur et à mesure si le début du mot correspond bien au début d'un mot existant.
Pour cela on modifie notre dictionnaire pour qu'il contienne tous les préfixes possibles. (Voir Generer_automate.py)
De manière pratique :
    En entrée, on reçoit la grille de lettre
    En sortie, on renvoie au fur et à mesure les mots sous forme de liste de couples (ligne,colonne)
    des cases à selectionner pour former un mot valide.


Optimisation possible : Cette IA ne prend pas en compte du tout les points de chaque lettre
(c'est clair qu'il vaudrait mieux commencer la recherche par les lettres donnant le plus de points)
ni les lettres ou mots qui comptent double ou triple.
"""





class Case():
    """
    Pour gagner du temps, on crée une bonne fois pour toute les cases adjacentes de chaque case.
    """
    def __init__(self,ligne,colonne,lettre):
        self.ligne=ligne
        self.colonne=colonne
        self.lettre=lettre
        self.voisins=[]

    def distance(self,case):
        """
        Donne la distance du sup pour obtenir les cases adjacentes dans les 8 directions
        """
        return max(abs(self.ligne-case.ligne),abs(self.colonne-case.colonne))

    def __str__(self):
        """
        Pour debug : Permet d'afficher avec print les éléments intéressants d'une case (ici coordonnées et lettres)
        """
        return str((str(self.ligne),str(self.colonne),self.lettre))

def init(grille):
    """
    Transforme la grille en liste de Case
    """
    # On commence par créer nos cases
    liste=[]
    for i,ligne in enumerate(grille):
        for j,lettre in enumerate(ligne):
            liste.append(Case(i,j,lettre))

    # Maintenant, on chercher pour chaque case les voisins (ce sont ceux dont le max(abs(i-i0),abs(j-j0))==1)
    for case0 in liste:
        for case in liste:
            if case0.distance(case)==1:
                case0.voisins.append(case)

    return liste

def donner_mot(grille,dico):
    """
    Générateur qui donne le mot valide suivant dans la grille sous forme de liste des coordonnées à suivre
    """
    # On modifie la grille sous forme de liste de cases
    cases= init(grille)

    # ensemble des mots déjà trouvés pour éviter de faire plusieurs fois le même
    trouves=set([])

    # La liste des cas à regarder sous la forme (Noeud dans l'automate des mots, liste des cases du chemin déjà parcouru)
    a_explorer=[[dico.suivant(case.lettre),[case]] for case in cases]

    while a_explorer:
        noeud,chemin=a_explorer.pop()
        # En cas de mauvaise lecture dans la capture, le noeud peut etre vide. Tant pis, on continue
        if noeud is None : continue
        # Pour chaque voisin qu'on n'a pas encore utilisé, on teste si on peut faire un mot valide plus long
        for voisin in [v for v in chemin[-1].voisins if v not in chemin]:
            suivant=noeud.suivant(voisin.lettre)
            if  suivant is not None:
                a_explorer.append([suivant,chemin+[voisin]])
        if noeud.suivant(".") is not None and noeud.etiquette not in trouves : # Si on a un mot valide non encore trouvé
            trouves.add(noeud.etiquette)
            #print(noeud.etiquette)
            yield [(case.ligne,case.colonne) for case in chemin]

if __name__ == '__main__':
    grille=[["A","M","O","T"],["N","O","S","I"],["E","S","W","X"],["Z","S","E","J"]]
    cases=init(grille)