import pygame
from pygame.locals import *


from ma_bao_pygame import *
from classes import *
from joueurs import *


# --------------------------- Constantes
DIMENSION_FENETRE = (1200,800)
NB_LIGNES = 3
NB_COLS = 3
JOUEUR_BLANC = Joueur_humain(0)
JOUEUR_NOIR = Joueur_humain(1)

DIMENSION_CASE_PLATEAU = 50
DIMENSION_CASE_BOITE = 20
MARGE_ZONE_BOITES = 15
COEFF_REDUCTION_BOITES = 0.9
coefficient_reduction_droit = DIMENSION_CASE_BOITE/1400
coefficient_reduction_oblique = coefficient_reduction_droit  #DIMENSION_CASE_BOITE/1000

DIMENSION_BOUTONS = (150,30)







def main():
    # ---------------------------  Init
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
    image_fleche = pygame.image.load("images/fleche.png").convert_alpha()

    # --------------------------- Les objets cliquables et textes fixes

    LISTE_OBJETS_CLIQUABLES = []
    LISTE_TEXTES = []

    # ---------- bouton nouvelle partie
    position = (50,150)
    dimension = DIMENSION_BOUTONS

    def fonction_activation_nv_partie(*args,**kwargs):
        jeu,*args = args
        jeu.n_tick = 5
        jeu.entrainement_auto = False
        jeu.reset()

    bouton = Bouton(position, dimension,font, texte="Recommencer",couleur = GRIS_CLAIR,fonction_activation = fonction_activation_nv_partie)
    LISTE_OBJETS_CLIQUABLES.append(bouton)

    # ---------- bouton reset
    position = (50,200)
    dimension = DIMENSION_BOUTONS

    def fonction_activation_reset(*args,**kwargs):
        jeu,*args = args
        jeu.n_tick = 5
        jeu.score = [0]*2
        jeu.entrainement_auto = False
        for j in jeu.joueurs:
            if j.est_IA_boites: j.liste_boites = []
        jeu.reset()

    bouton = Bouton(position, dimension,font, texte="Reinitialiser",couleur = GRIS_CLAIR,fonction_activation = fonction_activation_reset)
    LISTE_OBJETS_CLIQUABLES.append(bouton)


    # ---------- bouton entrainement auto
    position = (50,250)
    dimension = DIMENSION_BOUTONS

    def fonction_activation_nv_partie_auto(*args,**kwargs):
        jeu,*args = args
        jeu.n_tick = 100
        jeu.compteur_partie = 200
        jeu.entrainement_auto = (not any([j.est_humain for j in jeu.joueurs])) and any([j.est_IA_boites for j in jeu.joueurs])
        jeu.reset()

    bouton = Bouton(position, dimension,font, texte="200 parties auto",couleur = GRIS_CLAIR,fonction_activation = fonction_activation_nv_partie_auto)
    LISTE_OBJETS_CLIQUABLES.append(bouton)

    # ----------- Choix dimensions grilles

    def fonction_activation_cols(valeur,jeu,*args,**kwargs):
        jeu.nb_cols = valeur
        jeu.entrainement_auto = False
        jeu.n_tick = 5
        jeu.score = [0]*2
        jeu.reset()

    def fonction_activation_lignes(valeur,jeu,*args,**kwargs):
        jeu.nb_lignes = valeur
        jeu.entrainement_auto = False
        jeu.n_tick = 5
        jeu.score = [0]*2
        jeu.reset()

    liste_fonctions = [fonction_activation_cols,fonction_activation_lignes]
    x0 = 50
    for i in range(2):
        text=font.render("Nombre de {} :".format(["colonnes","lignes"][i]),1,(255,255,255))
        rect_text = text.get_rect(midleft = (x0,45))
        LISTE_TEXTES.append((text,rect_text))
        text_input_box = Text_input_box(rect_text.right + 10,rect_text.y-5,20,font,text = "3",couleur=BLANC,fonction_activation = liste_fonctions[i])
        x0 = text_input_box.rect.right + 20
        LISTE_OBJETS_CLIQUABLES.append(text_input_box)



    # ----------- Choix joueurs

    def fonction_modif_choix_joueur(n_joueur):
        def f(menu,jeu):
            if menu.element_choisi == 0 : # joueur humain
                joueur = Joueur_humain(n_joueur)
            elif menu.element_choisi == 1: # joueur aleatoire
                joueur = Joueur_aleatoire(n_joueur)
            elif menu.element_choisi == 2: # Joueur IA boite
                joueur = Joueur_IA_boites(n_joueur)

            jeu.joueurs[n_joueur] = joueur
            jeu.entrainement_auto = False
            jeu.score = [0]*2
            jeu.n_tick = 5
            jeu.reset()
        return f

    liste_choix = ["Humain","Aleatoire","IA boites"]
    x0 = 50
    for i in range(2):
        text=font.render("Joueur {} :".format(["blanc","noir "][i]),1,(255,255,255))
        rect_text = text.get_rect(midleft = (x0,85))
        LISTE_TEXTES.append((text,rect_text))
        menu_deroulant = Menu_deroulant(rect_text.right + 10,rect_text.center[1]-13,80,26,GRIS_CLAIR,BLANC,font,liste_choix,element_choisi = 0, fonction_modif = fonction_modif_choix_joueur(i))
        x0 = menu_deroulant.rect.right + 20
        LISTE_OBJETS_CLIQUABLES.append(menu_deroulant)

    # ---------------------------  Init jeu

    jeu = Jeu(JOUEUR_BLANC,JOUEUR_NOIR,NB_LIGNES,NB_COLS,DIMENSION_CASE_BOITE,coefficient_reduction_droit,coefficient_reduction_oblique)
    ligne_case_selectionnee, col_case_selectionnee = -1,-1

    # ---------------------------  Boucle de jeu

    continuer=1
    while continuer:
        #On efface l'écran
        fenetre.fill((35,35,35))
        pygame.time.Clock().tick(jeu.n_tick) # Pour éviter de trop rafraichir

        joueur_en_cours = jeu.joueurs[jeu.n_joueur_en_cours]
        joueur_humain_a_joue = False
        # --------- Gestion des évènements
        event_list = pygame.event.get()
        for event in event_list:                    # On parcours la liste de tous les événements reçus
            if event.type == QUIT :                 # Si un de ces événements est de type QUIT
                continuer = 0                       # On arrête la boucle
            if event.type == pygame.VIDEORESIZE:    # Pour redimensionner la fenetre
                fenetre = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == MOUSEBUTTONUP and event.button == 1 :
                m_x,m_y=event.pos
                if not jeu.partie_terminee and joueur_en_cours.est_humain: # On regarde où on a cliqué
                    ligne, col = (m_y-y0_grille)//DIMENSION_CASE_PLATEAU, (m_x-x0_grille)//DIMENSION_CASE_PLATEAU
                    if 0<=ligne< jeu.nb_lignes and 0<=col<jeu.nb_cols:
                        if ligne_case_selectionnee == -1 and any([ligne==l and col==c for l,c,ll,cc in jeu.deplacements_possibles]): # Si on n'avait pas de case selectionnée et qu'elle fait partie des coups possibles
                            ligne_case_selectionnee, col_case_selectionnee = ligne, col
                        elif (ligne_case_selectionnee != -1 and (ligne_case_selectionnee, col_case_selectionnee, ligne, col) in jeu.deplacements_possibles) :
                            jeu.jouer(ligne_case_selectionnee, col_case_selectionnee, ligne, col)
                            ligne_case_selectionnee, col_case_selectionnee = -1,-1
                            joueur_humain_a_joue = True
                        else:
                            ligne_case_selectionnee, col_case_selectionnee = -1,-1


        # --------- Tour de l'IA
        joueur_en_cours = jeu.joueurs[jeu.n_joueur_en_cours]
        if not jeu.partie_terminee and not joueur_en_cours.est_humain and not joueur_humain_a_joue :
            deplacement_propose = joueur_en_cours.jouer(jeu)
            jeu.jouer(*deplacement_propose)

        if  not jeu.partie_terminee and (not jeu.deplacements_possibles or jeu.grille.est_gagnante()): # Si la partie est terminée
            gagnant = 1-jeu.n_joueur_en_cours
            jeu.score[gagnant] += 1
            for j in jeu.joueurs:
                j.maj_fin_partie(gagnant)
            jeu.compteur_partie -= 1
            if (not jeu.entrainement_auto) or jeu.compteur_partie==0:
                jeu.partie_terminee = True
            else:
                jeu.reset()

        fenetre_x,fenetre_y = fenetre.get_size()
        # --------- Affichage du plateau de jeu
        x0_grille = (fenetre_x-jeu.nb_cols*DIMENSION_CASE_PLATEAU)//2
        y0_grille = 100
        jeu.grille.afficher(fenetre,x0_grille,y0_grille,DIMENSION_CASE_PLATEAU,ligne_case_selectionnee, col_case_selectionnee)

        # --------- Affichage des boites
        liste_boites = []
        for n,joueur in enumerate(jeu.joueurs):
            if joueur.est_IA_boites:
                liste_boites += joueur.liste_boites

        x0_boites = MARGE_ZONE_BOITES
        y0_boites = y0_grille + DIMENSION_CASE_PLATEAU*(jeu.nb_lignes) + 40

        # On calcule la place qu'il va falloir
        jeu.dimension_case_boite = DIMENSION_CASE_BOITE
        jeu.coefficient_reduction_droit =coefficient_reduction_droit
        jeu.coefficient_reduction_oblique = coefficient_reduction_oblique
        delta_x_boites = jeu.dimension_case_boite * (jeu.nb_cols) +jeu.dimension_case_boite//2
        delta_y_boites = jeu.dimension_case_boite * (jeu.nb_lignes +1)
        n_lignes = len(liste_boites)//((fenetre_x-2*MARGE_ZONE_BOITES)//delta_x_boites)
        while n_lignes*delta_y_boites +jeu.dimension_case_boite > fenetre_y-y0_boites-MARGE_ZONE_BOITES-32: # Si on sortde l'écran, on diminue la taille des boites
            jeu.dimension_case_boite *= COEFF_REDUCTION_BOITES
            jeu.coefficient_reduction_droit *= COEFF_REDUCTION_BOITES
            jeu.coefficient_reduction_oblique *= COEFF_REDUCTION_BOITES
            delta_x_boites = jeu.dimension_case_boite * (jeu.nb_cols) +jeu.dimension_case_boite//2
            delta_y_boites = jeu.dimension_case_boite * (jeu.nb_lignes +1)
            n_lignes = len(liste_boites)//((fenetre_x-2*MARGE_ZONE_BOITES)//delta_x_boites)
            if jeu.dimension_case_boite < 10 : break


        x,y = x0_boites, y0_boites
        for indice_boite,boite in enumerate(liste_boites):
            boite.afficher(fenetre,x,y,image_fleche,jeu)
            x += delta_x_boites
            if x +delta_x_boites > fenetre_x - MARGE_ZONE_BOITES:
                x = x0_boites
                y += delta_y_boites


        # --- Les textes à afficher
        if jeu.partie_terminee:
            text=font_victoire.render("Le gagnant est le joueur {}".format(["BLANC","NOIR"][gagnant]),1,(255,255,255))
            rect_text = text.get_rect(center = (fenetre_x//2,y0_grille+DIMENSION_CASE_PLATEAU*(jeu.nb_lignes) + 10))
            fenetre.blit(text,rect_text)

        # le score
        text=font.render("Victoires joueur blanc : {}         Victoires joueur noir : {}".format(*jeu.score),1,(255,255,255))
        rect_text = text.get_rect(center = (fenetre_x//2,35))
        fenetre.blit(text,rect_text)

        for txt in LISTE_TEXTES:
            fenetre.blit(*txt)

        # --- Les objets_cliquables
        for obj_clic in LISTE_OBJETS_CLIQUABLES:
            obj_clic.update(event_list,args_fonction = [jeu])
            obj_clic.dessiner(fenetre)


        pygame.display.flip()

    pygame.quit()
    exit()

if __name__=="__main__" :
    main()




#TODO :