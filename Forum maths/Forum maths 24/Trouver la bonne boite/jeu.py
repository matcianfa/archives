"""
Un chat se cache dans une boite parmi 5 alignées. Tous les jours, il se déplace d'une case vers la droite ou la gauche (si possible). Trouver une stratégie pour trouver le chat à coup sûr (en 6 jours).
"""

import pygame
from pygame.locals import *


from ma_bao_pygame import *


# ---------- CONSTANTES
NOMBRE_BOITES = 5
NOMBRE_ESSAIS_MAX = 6

DIMENSION_FENETRE = (1200,800)
DIMENSION_BOITES = 100
DIMENSION_MINI_BOITES = 40
ESPACEMENT_BOITES = 75
ESPACEMENT_MINI_BOITES = 30
DELTA_MINI = DIMENSION_MINI_BOITES+ESPACEMENT_MINI_BOITES


# ---------- Fonctions

def jeu(nb_boites = NOMBRE_BOITES,nb_essais_max = NOMBRE_ESSAIS_MAX):
    pygame.init()
    fenetre = pygame.display.set_mode(DIMENSION_FENETRE, pygame.RESIZABLE)
    pygame.display.set_caption("Hexapawn")
    # Afficher un fond blanc
    fond = pygame.Surface(fenetre.get_size())
    fond = fond.convert()
    fond.fill((255,255,255))
    fenetre.blit(fond,(0,0))
    font=pygame.font.SysFont("Arial",12,bold=False,italic=False)
    font_victoire=pygame.font.SysFont("Arial",25,bold=True,italic=False)
    fontsmall=pygame.font.SysFont("Arial",10,bold=False,italic=False)
    #Pour gérer l'appuye répété sur une touche
    pygame.key.set_repeat(400,20)

    # ------ Fonctions

    def donner_liste_boites():
        x,y = (fenetre.get_width()-(nb_boites-1)*(DIMENSION_BOITES+ESPACEMENT_BOITES))//2,150
        liste_boites = []
        for k in range(nb_boites):
            liste_boites.append(Image_cliquable(x,y,[boite_fermee,boite_vide,chat],dimension = (DIMENSION_BOITES,DIMENSION_BOITES)))
            x+= DIMENSION_BOITES + ESPACEMENT_BOITES
        return liste_boites

    # ------ Images
    boite_fermee = pygame.image.load("images/boite_fermee.png").convert_alpha()
    boite_vide = pygame.image.load("images/boite_vide.png").convert_alpha()
    chat = pygame.image.load("images/chat.png").convert_alpha()
    croix = pygame.image.load("images/croix.png").convert_alpha()
    cercle = pygame.image.load("images/cercle.png").convert_alpha()
    mini_boite_fermee = pygame.transform.scale(boite_fermee,(DIMENSION_MINI_BOITES,DIMENSION_MINI_BOITES))
    mini_boite_vide = pygame.transform.scale(boite_vide,(DIMENSION_MINI_BOITES,DIMENSION_MINI_BOITES))
    mini_chat = pygame.transform.scale(chat,(DIMENSION_MINI_BOITES,DIMENSION_MINI_BOITES))
    mini_croix = pygame.transform.scale(croix,(DIMENSION_MINI_BOITES,DIMENSION_MINI_BOITES))
    mini_cercle = pygame.transform.scale(cercle,(DIMENSION_MINI_BOITES,DIMENSION_MINI_BOITES))


    # ------ init
    nombre_essais = 0
    numero_boite_cliquee = -1
    boites_proposees = []
    # -1 = impossible, 0 = possible, 1 = case_choisie
    grille_possibilites = [[-1 if i%(nb_boites+1) == 0 else 0 for i in range(nb_boites+2)] for __ in range(nb_essais_max+1)]


    LISTE_OBJETS_CLIQUABLES = []
    LISTE_OBJETS_AFFICHES = []
    LISTE_BOITES = donner_liste_boites()

    mode_jeu = "JEU"

    continuer=1
    while continuer:
        #On efface l'écran
        fenetre.fill((35,35,35))
        pygame.time.Clock().tick(10) # Pour éviter de trop rafraichir


        # --------- Gestion des évènements
        event_list = pygame.event.get()
        for event in event_list:                    # On parcours la liste de tous les événements reçus
            if event.type == QUIT :                 # Si un de ces événements est de type QUIT
                continuer = 0                       # On arrête la boucle
            if event.type == pygame.VIDEORESIZE:    # Pour redimensionner la fenetre
                fenetre = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                LISTE_BOITES = donner_liste_boites()

            if event.type == MOUSEBUTTONUP and event.button == 1 :
                m_x,m_y=event.pos
                if mode_jeu == "JEU":
                    # On cherche si on a cliqué sur une boite
                    for numero_boite,boite in enumerate(LISTE_BOITES) :
                        if boite.rect.collidepoint((m_x,m_y)):
                            numero_boite_cliquee = numero_boite

                            nombre_essais += 1
                            # --- MaJ grille_possibilites
                            grille_possibilites[nombre_essais][numero_boite_cliquee+1] = 1

                            if all([b!=0 for b in grille_possibilites[nombre_essais]]):
                                mode_jeu = "GAGNE"
                                print("Gagné !")
                            elif nombre_essais == nb_essais_max:
                                mode_jeu = "PERDU"
                                # --- Recherche chemin possible
                                i_chat = -1
                                for e in range(nombre_essais,0,-1):
                                    if i_chat == -1 :
                                        i_chat = grille_possibilites[e].index(0)
                                    elif grille_possibilites[e][i_chat-1] == 0:
                                        i_chat -= 1
                                    elif grille_possibilites[e][i_chat+1] == 0:
                                        i_chat += 1
                                    else :
                                        print("Bug recherche chat")
                                    grille_possibilites[e][i_chat] = 2

                            else :
                                for i in range(1,nb_boites+1):
                                    if grille_possibilites[nombre_essais][i-1] != 0 and grille_possibilites[nombre_essais][i+1] != 0:
                                        grille_possibilites[nombre_essais+1][i] = -1

        # -------------------- Affichage des objets
        # --------- Les boites
        if numero_boite_cliquee>=0 :
            for numero_boite,boite in enumerate(LISTE_BOITES) :
                if numero_boite == numero_boite_cliquee :
                    boite.changer_image(1 + (mode_jeu=="GAGNE"))
                else :
                    boite.changer_image(0)

        for objet in LISTE_BOITES :
            objet.dessiner(fenetre)

        # --------- Les coups joués
        x0, y = (fenetre.get_width()-(nb_boites-1)*(DELTA_MINI) - DIMENSION_MINI_BOITES)//2,150 + DIMENSION_BOITES
        for ligne in range(1,NOMBRE_ESSAIS_MAX+1):
            x=x0
            for col in range(1,nb_boites+1):
                if grille_possibilites[ligne][col] ==1 : #♣ Si on a cliqué
                    fenetre.blit(mini_cercle,(x,y))
                elif   grille_possibilites[ligne][col] ==2 : # Si on a un chat
                    fenetre.blit(mini_chat,(x,y))
                elif grille_possibilites[ligne][col] == -1 : # Si on ne sait pas
                    fenetre.blit(mini_croix,(x,y))
                else :
                    fenetre.blit(mini_boite_fermee,(x,y))
                x += DELTA_MINI
            y += DELTA_MINI





        pygame.display.flip()

    pygame.quit()
    exit()

def jeu_console(nb_boites = NOMBRE_BOITES,nb_essais_max = NOMBRE_ESSAIS_MAX):
    """
    Version console du jeu
    """
    # ------ Init
    boites_proposees = []
    nb_essais = 0
    # -1 = impossible, 0 = possible, 1 = case_choisie
    grille_possibilites = [[-1 if i%(nb_boites+1) == 0 else 0 for i in range(nb_boites+2)] for __ in range(nb_essais_max+1)]
    # ------ Boucle jeu
    while nb_essais < nb_essais_max:
        nb_essais += 1
        # --- MaJ grille_possibilites
        for i in range(1,nb_boites+1):
            if grille_possibilites[nb_essais-1][i-1] != 0 and grille_possibilites[nb_essais-1][i+1] != 0:
                grille_possibilites[nb_essais][i] = -1

        reponse = int(input(f"Choisir une boite (entre 1 et {nb_boites}) : "))
        if not (0<reponse <= nb_boites) : continue
        grille_possibilites[nb_essais][reponse] = 1

        if all([b!=0 for b in grille_possibilites[nb_essais]]):
            print("Gagné !!")
            break
    else:
        print("Perdu")

        # --- Recherche chemin possible
        i_chat = -1
        for e in range(nb_essais,0,-1):
            if i_chat == -1 :
                i_chat = grille_possibilites[e].index(0)
            elif grille_possibilites[e][i_chat-1] == 0:
                i_chat -= 1
            elif grille_possibilites[e][i_chat+1] == 0:
                i_chat += 1
            else :
                print("Bug recherche chat")
            grille_possibilites[e][i_chat] = 2

        for e in range(1,nb_essais+1):
            print(f"Tu as choisis la boite {grille_possibilites[e].index(1)} alors que le chat était dans la boite {grille_possibilites[e].index(2)}")




if __name__ == "__main__" :
    jeu()