# -*- coding: utf-8 -*

import pygame
from pygame.locals import *
import subprocess as sp
import os
from random import randint
import time
# Mes modules perso
from classes import *
from pivot import *

# paramètres
dimension_fenetre = (800, 600)

#----------------------------------------------
# Les règles :
nb_regles=4
# Règle 0 : Changement en croix
def donner_liste_0(i,j,dim_plateau):
    return [(k,l) for k,l in [(i,j),(i-1,j),(i+1,j),(i,j-1),(i,j+1)] if 0<=k<dim_plateau and 0<=l<dim_plateau]

# Règle 1 : Changement de toute la ligne et toute la colonne
def donner_liste_1(i,j,dim_plateau):
    return [(k,j) for k in range(dim_plateau) if k!=i]+[(i,k) for k in range(dim_plateau) if k!=j]+[(i,j)]



# Fonction qui modifie les cases en fonction de la regle
def appliquer_regle(numero_regle,liste_cases,i,j,dim_plateau,modulo) :
    """
    Modifie la couleur des cases situées sur la croix centrée sur la case dont on donne le numero
    """
    def inverser(i,j):
        if 0<=i<dim_plateau and 0<=j<dim_plateau :
            liste_cases[j*dim_plateau+i].inverser(modulo)

    for k,l in eval("donner_liste_"+str(numero_regle%2)+"(i,j,dim_plateau)"):
        inverser(k,l)

# Fonction qui permet de transformer la liste des coordonnées dans le tableau en liste de numéro de case
def coord_to_numero(liste,dim_plateau):
    return [j*dim_plateau + i for i,j in liste]


#--------------------------------------------
def main():
    pygame.init()
    fenetre = pygame.display.set_mode(dimension_fenetre)
    # Afficher un fond blanc
    fond = pygame.Surface(fenetre.get_size())
    fond = fond.convert()
    fond.fill((255,255,255))
    fenetre.blit(fond,(0,0))
    font=pygame.font.SysFont("Arial",12,bold=False,italic=False)
    fontsmall=pygame.font.SysFont("Arial",10,bold=False,italic=False)
    font_chiffres=pygame.font.SysFont("Arial",16,bold=False,italic=False)
    Case.fontsmall=fontsmall
    #Pour gérer l'appuye répété sur une touche
    pygame.key.set_repeat(400,20)

    #Les variables
    etape="Debut" # Etapes possibles : Debut , Jeu



    continuer=1
    while continuer:
        pygame.time.Clock().tick(30) # Pour éviter de trop rafraichir
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT :     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle

        # init pour l'étape Debut
        if etape == "Debut" :
            texte=""
            ss_etape=0
            max_ss_etape = 3
            liste_reponses=[""]*4

        # Etape 0 : On demande l'image à afficher ou un exemple préenregistré
        while etape == "Debut" :
            #On efface l'écran
            fenetre.fill((255,255,255))
            pygame.time.Clock().tick(30) # Pour éviter de trop rafraichir
            # Pour passer à l'étape suivante
            if ss_etape == max_ss_etape:
                try:
                    regle=int(liste_reponses[1])
                    if regle not in list(range(nb_regles)) or not liste_reponses[0].isdigit() or not liste_reponses[2].isdigit() or int(liste_reponses[2])<2:
                        ss_etape=0
                    else :
                        etape = "Init"
                        dim_plateau=int(liste_reponses[0])
                        modulo=int(liste_reponses[2])
                except:
                    ss_etape-=1
                break
            for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
                if event.type == QUIT :     #Si un de ces événements est de type QUIT
                    continuer = 0      #On arrête la boucle
                    etape=""
                if event.type == KEYDOWN :
                    if event.key==K_RETURN or event.key==K_KP_ENTER :
                        if ss_etape==1 and int(liste_reponses[1])<=1 :
                            liste_reponses[2]="2"
                            ss_etape+=1
                        ss_etape+=1
                        texte=""
                        break
                    elif event.key==K_BACKSPACE:
                        if not texte :
                            ss_etape=max(0,ss_etape-1)
                            texte=liste_reponses[ss_etape]
                        else : texte=texte[:-1]
                        break
                    # Boite pour entrer le nom du fichier
                    else:
                        texte+=event.dict['unicode']
            # On sauvegarde le texte dans la variable selon l'étape
            liste_reponses[ss_etape]=texte
            #On affiche les textes
            text=font.render("Entrer la dimension du tableau : {}".format(liste_reponses[0]),1,(0,0,0))
            fenetre.blit(text,(300,200))
            if ss_etape>=1 :
                text=font.render("Entrer la règle utilisée : {}".format(liste_reponses[1]),1,(0,0,0))
                fenetre.blit(text,(300,230))
                if ss_etape==1:
                    text=fontsmall.render("Règle 0 : On inverse les couleurs selon une croix autour de la case choisie",1,(0,0,0))
                    fenetre.blit(text,(330,260))
                    text=fontsmall.render("Règle 1 : On inverse les couleurs sur toute la ligne et la colonne de la case choisie",1,(0,0,0))
                    fenetre.blit(text,(330,275))
                    text=fontsmall.render("Règle 2 : Comme la règle 0 mais avec plusieurs couleurs",1,(0,0,0))
                    fenetre.blit(text,(330,290))
                    text=fontsmall.render("Règle 3 : Comme la règle 1 mais avec plusieurs couleurs",1,(0,0,0))
                    fenetre.blit(text,(330,305))
            if ss_etape>=2 :
                text=font.render("Entrer le nombre de couleurs : {}".format(liste_reponses[2]),1,(0,0,0))
                fenetre.blit(text,(300,260))

            pygame.display.flip() # Pour rafraichir l'affichage

        if etape == "Init":
            # On initialise la classe Case
            Case.init(dim_plateau,dimension_fenetre)
            etape="Jeu"
            # On crée un le plateau
            plateau= [Case(0,k,dim_plateau) for k in range(dim_plateau**2)]
            message_central="Appuyer sur R pour choisir une coloration au hasard"
        if etape == "Relancer" :
            etape="Jeu"
            message_central="But du jeu : colorer toutes les cases en noir"
            # On crée un le plateau
            plateau= [Case(randint(0,modulo-1),k,dim_plateau) for k in range(dim_plateau**2)]
        # initialisation de la phase de Jeu
        if etape == "Jeu":
            # Les constantes
            resolu=False
            resolu_inv=False
            mode_solution=False
            afficher_numeros=False
            # Creation de la matrice associée au plateau
            matrice=[[0]*(dim_plateau**2) for _ in range(dim_plateau**2)]
            for i in range(dim_plateau):
                for j in range(dim_plateau):
                    liste=coord_to_numero(eval("donner_liste_"+str(regle%2)+"(i,j,dim_plateau)"),dim_plateau)
                    ligne=j*dim_plateau+i
                    for col in liste :
                        matrice[ligne][col]=1

        while etape == "Jeu" :
            #On efface l'écran
            fenetre.fill((255,255,255))
            pygame.time.Clock().tick(30) # Pour éviter de trop rafraichir
            for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
                if event.type == QUIT :     #Si un de ces événements est de type QUIT
                    continuer = 0      #On arrête la boucle
                    etape=""
                if event.type == KEYDOWN :
                    if event.key==K_BACKSPACE:
                        etape="Debut"
                    if event.key==K_RETURN or event.key==K_KP_ENTER:
                        etape="Relancer"

                    if event.key==K_n:
                        afficher_numeros=True
                    if event.key==K_r:
                        #On résout le problème
                        vecteur=[(-case.couleur)%modulo for case in plateau]
                        M_triangulaire,V_triangulaire=triangularisation(matrice,vecteur,modulo)
                        resolu=remonter_triang_opti(M_triangulaire,V_triangulaire,modulo)
                        if resolu is not None :
                            M_remonte,V_remonte=resolu[0]
                            if modulo>=2 :
                                #resolu_inv = inv_diagonale(M_remonte,V_remonte,modulo)
                                resolu_inv = inv_diagonale_opti(resolu,modulo)
                                if resolu_inv is not None :
                                    M_resolu,V_resolu,rg=resolu_inv
                                    solution=V_resolu
                                    M_remonte,V_remonte=resolu[rg]
                                    message_central="On peut résoudre en cliquant {} fois".format(sum(V_resolu))
                                else:message_central="Il n'y a pas de solution"
                            else :
                                message_central="On peut résoudre en cliquant {} fois".format(sum(V_remonte))
                        else  :message_central="Il n'y a pas de solution"
                    if event.key==K_f:
                        try:
                            vecteur=[case.couleur for case in plateau]
                            # Créer un pdf contenant les formules
                            texte_latex=""
                            with open("Latex/preambule.tex", "r") as texte :
                                texte_latex+=texte.read()
                            # Le texte provenant des calculs
                            # Affichage du systeme de départ
                            texte_latex+=titre_latex("Système d'équations réduit issu de notre problème")
                            texte_latex+= to_latex_reduit(matrice,vecteur)
                            texte_latex+=r"\newpage"
                            texte_latex+=titre_latex("Système d'équations issu de notre problème")
                            texte_latex+= to_latex(matrice,vecteur)
                            texte_latex+=r"\newpage"
                            # Affichage du systeme triangulaire
                            texte_latex+=titre_latex("Système d'équations triangularisé réduit issu de notre problème")
                            texte_latex+= to_latex_reduit(M_triangulaire,V_triangulaire)
                            texte_latex+=r"\newpage"
                            texte_latex+=titre_latex("Système d'équations triangularisé issu de notre problème")
                            texte_latex+= to_latex(M_triangulaire,V_triangulaire)
                            texte_latex+=r"\newpage"
                            if resolu:
                                # Affichage du systeme résolu avec facteur devant les inconnues
                                texte_latex+=titre_latex("Système d'équations presque résolu issu de notre problème")
                                texte_latex+= to_latex_reduit(M_remonte,V_remonte)
                                texte_latex+=r"\newpage"
                                if modulo>=2 and resolu_inv is not None:
                                    # Affichage du systeme résolu final si possible
                                    texte_latex+=titre_latex("Système d'équations résolu issu de notre problème")
                                    texte_latex+= to_latex_reduit(M_resolu,V_resolu)
                                    texte_latex+=r"\newpage"

                            #La fin en latex
                            with open("Latex/conclusion.tex", "r") as texte :
                                texte_latex+=texte.read()
                            with open("Formules.tex",encoding='utf-8',mode="w") as mon_fichier:
                                mon_fichier.write(texte_latex)
                            sp.Popen("pdflatex --interaction=batchmode Formules.tex")
                            time.sleep(10)
                            os.startfile("Formules.pdf")
                        except:
                            pass
                    if event.key==K_s and resolu:
                        mode_solution=True
                        #Affiche les points rouges sur les cases à cliquer pour gagner
                        for k,val in enumerate(solution ):
                            if val :
                                plateau[k].point_rouge=True
                                if modulo==2 : plateau[k].texte_sol=1
                            if modulo>2 and resolu_inv is not None:
                                plateau[k].texte_sol=solution[k]
                if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                    m_x,m_y=event.pos
                    # On  regarde sur quelle case on a cliqué et on applique la regle pour changer les couleurs
                    if Case.x_0<m_x<Case.x_1 and Case.y_0<m_y<Case.y_1 :
                        i = (m_x-Case.x_0)//Case.dim_case
                        j = (m_y-Case.y_0)// Case.dim_case
                        case=plateau[j*dim_plateau+i]
                        if mode_solution:
                            case.texte_sol=(case.texte_sol-1)%modulo
                        if not case.texte_sol or not mode_solution:
                            case.point_rouge=False
                        else :
                            case.point_rouge=True
                        resolu=False
                        appliquer_regle(regle,plateau,i,j,dim_plateau,modulo)
            # On affiche le plateau
            for case in plateau :
                case.dessiner(fenetre,modulo)
                # On affiche les numeros
                if afficher_numeros :
                    case.afficher_numero(fenetre,font_chiffres)

            # Les textes à afficher
            text=fontsmall.render("N : Afficher le numéro des cases",1,(0,0,0))
            fenetre.blit(text,(15,15))
            text=fontsmall.render("Entrée : Relancer au hasard",1,(0,0,0))
            fenetre.blit(text,(15,25))
            text=fontsmall.render("R : Lancer la résolution du problème",1,(0,0,0))
            fenetre.blit(text,(15,35))
            text=fontsmall.render("F : Ouvrir un pdf contenant les équations",1,(0,0,0))
            fenetre.blit(text,(15,45))
            if resolu:
                text=fontsmall.render("S : Afficher la solution",1,(0,0,0))
                fenetre.blit(text,(15,55))
            if message_central :
                text=font.render(message_central,1,(0,0,0))
                fenetre.blit(text,text.get_rect(center=(dimension_fenetre[0]//2, 30)))

            pygame.display.flip() # Pour rafraichir l'affichage


    pygame.quit()
    exit()



#----------------------------------

if __name__ == "__main__":
    pass
    main()



#---------------TODO---------------

