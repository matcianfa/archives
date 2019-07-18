# -*- coding: utf-8 -*
# IMPORTANT : A executer en tant que script


import tkinter as tk
from tkinter import filedialog
import pygame
from pygame.locals import *
import numpy as np
from cmath import *
import subprocess as sp
import time
import os


# paramètres modifiables
dimension_fenetre = (800, 600)
epaisseur_points=2
pas_t = 0.005 # Pas du paramètre t du dessin



#-------------------------------

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
    #Pour gérer l'appuye répété sur une touche
    pygame.key.set_repeat(400,20)

    # Les constantes
    etape = 0
    liste_points=[]
    seuil_rayon_cercle=0.15 #Seuil en dessous duquel les cercles ne sont pas pris en compte dans le dessin
    nb_cercles = 2 # nb_cercles utilisés
    #-------------------------------

    def trace_cercle(centre,rayon):
        """
        Trace le cercle dont on donne le centre en complexe et le rayon
        """
        if rayon>=1 :
            pygame.draw.circle(fenetre, (0,0,255),
    (int(centre.real),int(centre.imag)),int(rayon),1)


    def trace_point(centre,color=(255,0,0),epaisseur=epaisseur_points):
        """
        Trace le point de coordonnées centre
        """
        x,y=centre
        pygame.draw.circle(fenetre,color , (int(x),int(y)),epaisseur)

    def trace_epicycloides(liste_coeff,t):
        centre = liste_coeff[0][1]
        for k,suivant in liste_coeff[1:]:
            trace_point((centre.real,centre.imag),(0,255,0),1)
            trace_cercle(centre,abs(suivant))
            centre += suivant*exp(complex(0,(k)*t))
        trace_point((centre.real,centre.imag),(255,0,0),epaisseur_points+2)
        # On renvoit le dernier point pour pouvoir le garder en mémoire
        return (centre.real,centre.imag)

    def trace_courbe(liste_coeff):
        t=0
        while t< 2*np.pi :
            centre = liste_coeff[0][1]
            for k,suivant in liste_coeff[1:]:
                centre+= suivant*exp(complex(0,(k)*t))
            trace_point((centre.real,centre.imag),(0,0,0),1)
            t+=pas_t

    #-------------------------------

    def Fourier(liste_points):
        """
        Renvoie la liste des coefficients de Fourier (par transformée rapide via numpy) des points de la liste (transformés en complexe).
        """
        return np.fft.fft(np.array([complex(x,y) for x,y in liste_points]))

    def epurer_liste(liste,nb_cercles,N):
        """
        renvoie une liste des "seuil" premiers coefficients rangés du plus grand au plus petit
        """
        def f(k):
            if k>N//2  : return k-N
            else : return k
        return sorted([(f(k),c) for k,c in enumerate(liste)],reverse=True,key=lambda x:abs(x[1]))[:nb_cercles]


    #-------------------------------


    continuer=1
    while continuer:
        pygame.time.Clock().tick(30) # Pour éviter de trop rafraichir
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT :     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle
        # Les constantes
        nom_fichier = ""
        message_erreur=""
        afficher_image =False
        afficher_courbe=False
        sauter_etape_1=False

        # Etape 0 : On demande l'image à afficher ou un exemple préenregistré
        while etape == 0 :
            #On efface l'écran
            fenetre.fill((255,255,255))
            pygame.time.Clock().tick(30) # Pour éviter de trop rafraichir
            for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
                if event.type == QUIT :     #Si un de ces événements est de type QUIT
                    continuer = 0      #On arrête la boucle
                    etape=-1
                if event.type == KEYDOWN :
                    message_erreur=""
                    if event.key==K_RETURN :
                        try:
                            if nom_fichier :
                                image=pygame.image.load("./images/"+nom_fichier).convert()
                            else :
                                image=None
                            etape += 1
                            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                            # Chargement de la liste de points si elle a été enregistrée
                            with open("images/"+nom_fichier[:nom_fichier.find(".")]+".txt", "r") as mon_fichier :
                                liste_points=eval(mon_fichier.read())
                                #Si on presse CTRL en plus, on va directement à l'étape 2
                                if pygame.key.get_mods() & pygame.KMOD_CTRL: sauter_etape_1=True
                        except :
                            message_erreur="Fichier introuvable"
                    elif event.key==K_BACKSPACE:
                        nom_fichier=nom_fichier[:-1]
                        break
                    # Boite pour entrer le nom du fichier
                    else:
                        nom_fichier+=event.dict['unicode']
                if event.type == MOUSEBUTTONUP: # quand je relache le bouton
                    if event.button == 1: # 1= clique gauche
                        if bouton_ouvrir.collidepoint(event.pos):
                            popup=tk.Tk()
                            chemin =  filedialog.askopenfilename(initialdir = "images/",title = "Select file",filetypes = (("images","*.jpg *.jpeg *.png *.bmp *.gif"),("all files","*.*")))
                            nom_fichier=chemin.split("/")[-1]
                            popup.destroy()
            #On affiche les textes
            text=font.render("Etape N° {} : Choix de l'image".format(etape),1,(0,0,0))
            fenetre.blit(text,(15,15))
            text=fontsmall.render("Entrée : passer à l'étape suivante",1,(0,0,0))
            fenetre.blit(text,(15,30))
            text=fontsmall.render("CTRL + Entrée : Passer directement aux épicycloides",1,(0,0,0))
            fenetre.blit(text,(15,45))
            # affichage du nom du fichier
            text=font.render("Entrer le nom de l'image (avec l'extension) : {}".format(nom_fichier),1,(0,0,0))
            fenetre.blit(text,(270,270))
            # Message d'erreur si besoin
            text=font.render(message_erreur,1,(255,0,0))
            fenetre.blit(text,(300,240))
            # Bouton ouvrir
            text=font.render("Ouvrir",1,(0,0,0))
            marge=20
            w,h=text.get_size()
            bouton_ouvrir=Rect((380,300),(w+20,h+20))
            fond_bouton=pygame.Surface(bouton_ouvrir.size)
            fond_bouton.fill((200,200,200))
            fenetre.blit(fond_bouton,bouton_ouvrir)
            fenetre.blit(text,text.get_rect(center=bouton_ouvrir.center))
            


            pygame.display.flip() # Pour rafraichir l'affichage

        # Etape 1 : On demande les points
        while etape == 1 :
            #On efface l'écran
            fenetre.fill((255,255,255))
            pygame.time.Clock().tick(30) # Pour éviter de trop rafraichir
            for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
                if event.type == QUIT :     #Si un de ces événements est de type QUIT
                    continuer = 0      #On arrête la boucle
                    etape=-1
                if event.type == KEYDOWN or sauter_etape_1 :
                    if (sauter_etape_1 or event.key==K_RETURN) and liste_points:
                        # On calcule les coefficients de Fourier de la liste des points avant de passer à l'étape suivante
                        N=len(liste_points)
                        liste_coeff=[c/N for c in Fourier(liste_points)]
                        if nb_cercles<=2:
                            nb_cercles=len([c for c  in liste_coeff if abs(c)>seuil_rayon_cercle]) # On choisit comme base de travail le nombre de cercles tels que le plus petit ait un rayon supérieur à un seuil donné (a priori 0.1 ou 0.2)

                        liste_coeff_epuree=epurer_liste(liste_coeff,nb_cercles,N)
                        # Les constantes pour l'étape 2
                        trace=set([])
                        animation = False
                        t=0
                        pygame.mouse.set_cursor(*pygame.cursors.arrow)
                        etape += 1
                    elif event.key==K_BACKSPACE :
                        etape -= 1
                        liste_points=[]
                    elif event.key==K_SPACE:
                        liste_points=[]
                    elif event.key==K_c and liste_points:
                        afficher_courbe=not afficher_courbe
                        # On calcule les coefficients de Fourier de la liste des points pour créer la courbe
                        nb_cercles=1
                        N=len(liste_points)
                        liste_coeff=[c/N for c in Fourier(liste_points)]
                        liste_coeff_epuree=epurer_liste(liste_coeff,nb_cercles,N)
                    # + ou - pour augmenter ou diminuer le nombres de coefficients conservés
                    elif afficher_courbe:
                        if event.key==K_PLUS or event.key==K_KP_PLUS:
                            if pygame.key.get_mods() & pygame.KMOD_SHIFT: nb_cercles=min(N,10+nb_cercles)
                            else : nb_cercles=min(N,1+nb_cercles)
                            liste_coeff_epuree=epurer_liste(liste_coeff,nb_cercles,N)
                        if event.key==K_MINUS or event.key==K_KP_MINUS:
                            if pygame.key.get_mods() & pygame.KMOD_SHIFT: nb_cercles=max(2,nb_cercles-10)
                            else :nb_cercles=max(2,nb_cercles-1)
                            liste_coeff_epuree=epurer_liste(liste_coeff,nb_cercles,N)
                        #Touche F pour afficher la fonction en passant par Latex puis un pdf
                        if event.key==K_f :
                            texte_latex=""
                            with open("Latex/preambule.tex", "r") as texte :
                                texte_latex+=texte.read()
                            #On rajoute la formule entre le préambule latex et la conclusion
                            for k,coeff in liste_coeff_epuree:
                                if k==0 : texte_latex+= "{0:.5g}".format(coeff).replace("j","i")
                                else :
                                    texte_latex+="("+"{0:.3g}".format(coeff).replace("j","i")+")\\textbf{e}^{"+"-"*(k==-1)+str(k)*(k!=1 and k!=-1)+"it}"
                                texte_latex+="+"
                            texte_latex=texte_latex[:-1]
                            with open("Latex/conclusion.tex", "r") as texte :
                                texte_latex+=texte.read()
                            with open("FonctionFourier.tex","w") as mon_fichier:
                                mon_fichier.write(texte_latex)
                            sp.Popen("pdflatex --interaction=batchmode FonctionFourier.tex")
                            time.sleep(5)
                            os.startfile("FonctionFourier.pdf")
                    # Touche S pour sauvegarder
                    elif event.key==K_s and nom_fichier :
                        with open("images/"+nom_fichier[:nom_fichier.find(".")]+".txt", "w") as mon_fichier :
                            mon_fichier.write(str(liste_points))
                    # Touche suppr pour supprimer le dernier point ajouté
                    elif event.key==K_DELETE:
                        liste_points=liste_points[:-1]
                if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                    liste_points.append(event.pos)
            #On affiche l'image si elle existe
            if image is not None:
                rect = image.get_rect()
                rect.center=(dimension_fenetre[0]//2,dimension_fenetre[1]//2)
                fenetre.blit(image,(rect.x,rect.y))
            # On affiche les points enregistrés
            for point in liste_points :
                trace_point(point)
            #On affiche les textes
            text=font.render("Etape N° {} : Placer les points".format(etape),1,(0,0,0))
            fenetre.blit(text,(15,15))
            text=fontsmall.render("Entrée : passer à l'étape suivante",1,(0,0,0))
            fenetre.blit(text,(15,30))
            text=fontsmall.render("Retour arrière : revenir à l'étape précédente",1,(0,0,0))
            fenetre.blit(text,(15,45))
            text=fontsmall.render("Espace : réinitialiser la liste des points",1,(0,0,0))
            fenetre.blit(text,(15,60))
            text=fontsmall.render("Touche S : Sauvegarder les points",1,(0,0,0))
            fenetre.blit(text,(15,75))
            text=fontsmall.render("Touche supprimer : Supprime le dernier point ajouté",1,(0,0,0))
            fenetre.blit(text,(15,90))
            text=fontsmall.render("Touche C : Affiche/Retire la courbe obtenue après transformée de Fourier",1,(0,0,0))
            fenetre.blit(text,(15,105))
            text=font.render("Nombres de points : {}".format(len(liste_points)),1,(0,0,0))
            fenetre.blit(text,(15,120))
            # Si on est en mode : afficher courbe :
            if afficher_courbe:
                trace_courbe(liste_coeff_epuree)
                text=fontsmall.render("Touche + ou - [+Shift] : Augmenter le nombre de coefficients conservés",1,(0,0,0))
                fenetre.blit(text,(15,135))
                text=fontsmall.render("Touche F : Créer un pdf contenant la fonction qui approxime",1,(0,0,0))
                fenetre.blit(text,(15,150))
                text=font.render("Nombres de coefficients conservés : {}".format(len(liste_coeff_epuree)),1,(0,0,0))
                fenetre.blit(text,(15,165))


            pygame.display.flip() # Pour rafraichir l'affichage

        # Etape 2 : On affiche les epicycloides et on dessine.
        while etape == 2 :
            #On efface l'écran
            fenetre.fill((255,255,255))
            pygame.time.Clock().tick(100) # Pour éviter de trop rafraichir
            for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
                if event.type == QUIT :     #Si un de ces événements est de type QUIT
                    continuer = 0      #On arrête la boucle
                    etape=-1
                if event.type == KEYDOWN :
                    if event.key==K_RETURN :
                        animation = not animation
                    if event.key==K_BACKSPACE :
                        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                        etape -= 1
                        sauter_etape_1=False
                    if event.key==K_SPACE:
                        trace=set([])
                    if event.key==K_q:
                        afficher_image= not afficher_image
                    if event.key==K_PLUS or event.key==K_KP_PLUS:
                        nb_cercles=min(N,nb_cercles+1)
                        liste_coeff_epuree=epurer_liste(liste_coeff,nb_cercles,N)
                    if event.key==K_MINUS or event.key==K_KP_MINUS:
                        nb_cercles=max(1,nb_cercles-1)
                        liste_coeff_epuree=epurer_liste(liste_coeff,nb_cercles,N)
            # On affiche l'image si a est pressé
            if afficher_image and image is not None :
                rect = image.get_rect()
                rect.center=(dimension_fenetre[0]//2,dimension_fenetre[1]//2)
                fenetre.blit(image,(rect.x,rect.y))
            # On affiche la trace
            for p in trace :
                trace_point(p,(0,0,0))
            if animation :
                 trace.add(point)
                 t+=pas_t
            # On affiche les epicloides
            point=trace_epicycloides(liste_coeff_epuree,t)
            #On affiche les textes
            text=font.render("Etape N° {} : Dessiner avec des cercles".format(etape),1,(0,0,0))
            fenetre.blit(text,(15,15))
            text=fontsmall.render("Entrée : lancer ou arreter l'animation",1,(0,0,0))
            fenetre.blit(text,(15,30))
            text=fontsmall.render("Retour arrière : revenir à l'étape précédente",1,(0,0,0))
            fenetre.blit(text,(15,45))
            text=fontsmall.render("Espace : réinitialiser la trace",1,(0,0,0))
            fenetre.blit(text,(15,60))
            text=fontsmall.render("Touche A : Afficher/retirer l'image de départ",1,(0,0,0))
            fenetre.blit(text,(15,75))
            text=fontsmall.render("Touche + ou - : Augmenter ou diminuer le nombre de cercles",1,(0,0,0))
            fenetre.blit(text,(15,90))
            text=font.render("Nombres de cercles utilisés : {}".format(len(liste_coeff_epuree)-1),1,(0,0,0))
            fenetre.blit(text,(15,105))
            text=font.render("Rayon du plus petit cercle : {}".format(abs(liste_coeff_epuree[-1][1])),1,(0,0,0))
            fenetre.blit(text,(15,120))




            pygame.display.flip() # Pour rafraichir l'affichage

    pygame.quit()
    exit()










#----------------------------------

if __name__ == "__main__":
    pass
    main()