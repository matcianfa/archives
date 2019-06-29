"""
Pour ce jeu, on va parcourir la grille de lettre pour former des mots
mais par exemple si on commence par "wx", ca ne sert à rien d'explorer
plus de possibilités car aucun mot ne commence par ces lettres.
L'idée est donc de transformer le dictionnaire en une chaine de préfixes.
Tant que le mot qu'on a en parcourant notre grille fait parti des préfixes,
on peut continuer à chercher. Sinon on s'arrete.
Par exemple si notre dictionnaire est {mot, mots, motif},
on va le transformer en automate avec comme noeud le prefixe, comme fleche la lettre suivante possible.
On mettra "." pour signifier que le mot est complet.
Ca donnerait schematiquement :
                              "mots" -.-> Complet
                                 ^
                                 |
                                 s
                                 |
    "" -m-> "m" -o-> "mo" -t-> "mot" -i-> "moti" -f-> "motif" -.-> Complet
                                 |
                                 .
                                 |
                                 v
                            Complet


Ce script ne sert qu'une fois pour générer l'automate à partir d'un dictionnaire.
Après, on a juste à le charger avec la commande :
pickle.load(open('automate', 'rb'))
"""
import pickle #Pour sauvegarder des classes


class Noeud():
    def __init__(self,etiquette):
        self.etiquette=etiquette
        self.suivants=[]

    def ajouter(self,mot):
        """
        Ajoute le mot dans l'automate
        """
        if mot=="":
            self.suivants.append((".",Noeud(None)))
        else :
            for (lettre,suivant) in self.suivants: # On cherche si la première lettre du mot est déjà rentrée
                if lettre==mot[0]: # Si elle y est déjà, on passe à la suite
                    s=suivant
                    break
            else: # Si on ne l'a pas trouvé, on crée un nouveau noeud
                s=Noeud(self.etiquette+mot[0])
                self.suivants.append((mot[0],s))
            s.ajouter(mot[1:])

    def suivant(self,l):
        """
        Donne le noeud suivant avec la lettre l
        """
        if l=="":
            return None
        else:
            for (lettre,suivant) in self.suivants: # On cherche si la première lettre du mot est dans la liste des suivants
                if lettre==l: # Si elle y est, on donne le suivant
                    return suivant
            # Si on ne l'a pas trouvé, on renvoie None
            return None

    def est_dedans(self,mot):
        """
        renvoie si mot est un suffixe possible de ce noeud pour donner un mot du dictionnaire.
        A utiliser avec le noeud de départ pour savoir si le mot existe dans le dictionnaire
        """
        if mot=="":
            # Si "." est dans les suivants, le mot existe sinon non
            if self.suivant(".") is None: return False
            else: return True
        else :
            suivant=self.suivant(mot[0])
            if suivant is None : return False
            else : return suivant.est_dedans(mot[1:])


if __name__ == '__main__':
    # Comme on n'a pas le temps de faire tous les mots, on ne fait que ceux ayant plus du seuil comme nombre de lettre
    seuil_max = 8
    seuil_min = 5

    depart=Noeud("")
    # Création de l'automate à partir du dico.txt
    with open('dico.txt', 'r') as dico:
        for mot in dico:
            if seuil_min>len(mot.rstrip('\n')):
                depart.ajouter(mot.rstrip('\n')) # rstrip pour retirer le \n en trop
    # On enregistre notre automate
    pickle.dump(depart, open('automate_moins_de_{}_lettres'.format(4), 'wb'))




