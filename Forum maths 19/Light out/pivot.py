# -*- coding: utf-8 -*

"""
Ce module regroupe les fonctions pour résoudre modulo p un systeme en utilisant le pivot de gauss
Pour détailler on coupe en 2 étapes : On triangularise le systeme puis on le résout
"""

modulo = 2

#------------------------------

def inv_mod(a,p):
    """
    Fonction qui donne l'inverse de a modulo p en utilisant l'algorithme d'euclide pour trouver le u et v du theoreme de bezout
    renvoie None si impossible

    """

    def euclide_inverse(a,b):
        """
        renvoie le pgcd,u,v du th. de Bezout a.u+b.v=1
        """
        if a==0: return (b,0,1)
        else:
            d,v,u= euclide_inverse(b%a,a)
            return (d,u-(b//a)*v,v)

    d,u,v=euclide_inverse(a,p)
    if d!= 1 : return None
    else: return u%p

def pgcd(a,b):
    if b==0 : return a
    return pgcd(b,a%b)

#------------------------------

def triangularisation(matrice,vecteur,modulo=2):
    # On copie la matrice et le vecteur pour ne pas la modifier
    M=[ligne[:] for ligne in matrice]
    V=vecteur[:]
    n=len(M)
    for l in range(n-1):
        #On cherche le coefficient non nul sur la colonne l
        l2=l
        while M[l2][l]==0 and l2<n-1:
            l2+=1
        # On echange la ligne l2 et l
        M[l],M[l2]=M[l2],M[l]
        V[l],V[l2]=V[l2],V[l]
        # Pour chaque ligne en dessous, on fait une combinaison lineaire pour retirer le l-ieme terme
        for k in range(l+1,n):
            if M[k][l]!=0 :
                V[k]=(M[k][l]*V[l]-M[l][l]*V[k])%modulo
                M[k]=[0]*(l+1)+[(M[k][l]*M[l][j]-M[l][l]*M[k][j])%modulo for j in range(l+1,n)]
    return M,V



#--------------------------------

def remonter_triang(matrice,vecteur,modulo=2):
    """
    A combiner absolument avec le résultat de triangularisation
    Renvoie None si un coefficient diagonal est nul (et donc pas de solution possible) et celui du vecteur non
    """
    # On copie la matrice et le vecteur pour ne pas la modifier
    M=[ligne[:] for ligne in matrice]
    V=vecteur[:]
    n=len(M)
    for l in range(n-1,0,-1):
        mll=M[l][l] # Pour eviter trop de recherche de ce nombre
        if mll==0 :
            if V[l]!=0: # Pas de solution
                return None
            else: # On peut choisir la valeur qu'on veut (donc 0) du coup on remplace toute la colonne par des 0
                for k in range(l):
                    M[k][l]=0
        else:
            for k in range(l):
                if M[k][l]!=0 :
                    V[k]=(mll*V[k]-M[k][l]*V[l])%modulo
                    M[k]=[(mll*c)%modulo for c in M[k] ]
                    M[k][l]=0
    return M,V

def remonter_triang_opti(matrice,vecteur,modulo=2):
    """
    A combiner absolument avec le résultat de triangularisation
    Renvoie None si un coefficient diagonal est nul (et donc pas de solution possible) et celui du vecteur non
    Recherche en plus la solution demandant le moins de coups possibles
    """
    # On copie la matrice et le vecteur pour ne pas la modifier
    M0=[ligne[:] for ligne in matrice]
    V0=vecteur[:]
    n=len(M0)
    liste_MV=[[M0,V0]]
    for l in range(n-1,0,-1):
        temp_liste_MV=[]
        for M,V in liste_MV:
            mll=M[l][l] # Pour eviter trop de recherche de ce nombre
            if mll==0 :
                if V[l]!=0: # Pas de solution
                    break
                else: # On peut choisir la valeur qu'on veut (donc entre 0 et modulo-1)
                    for val in range(modulo):
                        M_temp=[ligne[:] for ligne in M]
                        V_temp=V[:]
                        M_temp[l][l]=1
                        V_temp[l]=val
                        for k in range(l):
                            if M_temp[k][l]!=0 :
                                V_temp[k]=(V[k]-M[k][l]*val)%modulo
                                M_temp[k][l]=0
                        temp_liste_MV.append([M_temp,V_temp])
            else:
                for k in range(l):
                    if M[k][l]!=0 :
                        V[k]=(mll*V[k]-M[k][l]*V[l])%modulo
                        M[k]=[(mll*c)%modulo for c in M[k] ]
                        M[k][l]=0
                temp_liste_MV.append([M,V])
        liste_MV=temp_liste_MV
    if liste_MV:
        return liste_MV
    else:
        return None
#--------------------------------

def inv_diagonale(matrice,vecteur,modulo=2):
    """
    Inverse la matrice diagonale obtenue apres remonter_triang dans le cas où on ne serait pas modulo 2.
    Sinon on ne peut pas inverser et on renvoie None
    """

    # On copie la matrice et le vecteur pour ne pas la modifier
    M=[ligne[:] for ligne in matrice]
    V=vecteur[:]
    n=len(M)
    #On inverse les coefficients diagonaux si possible
    for l in range(n):
        mll=M[l][l] # Pour éviter trop de recherche de ce nombre
        if mll==0 :
            if V[l]!=0: # Pas de solution
                return None
        else:
            inv=inv_mod(M[l][l],modulo)
            if inv is not None:
                M[l][l]=1
                V[l]=(V[l]*inv)%modulo
            else :
                return None
    return M,V

def inv_diagonale_opti(liste_MV,modulo=2):
    """
    Inverse les matrices diagonales obtenues apres remonter_triang_opti dans le cas où on ne serait pas modulo 2.
    Si on ne peut pas inverser et on renvoie None
    Cette version cherche de plus la meilleurs solution (celle avec le moins de coups au final)
    """
    reponses=[]
    for rg,(matrice,vecteur) in enumerate(liste_MV):
        # On copie la matrice et le vecteur pour ne pas la modifier
        M=[ligne[:] for ligne in matrice]
        V=vecteur[:]
        n=len(M)
        #On inverse les coefficients diagonaux si possible
        for l in range(n):
            mll=M[l][l] # Pour éviter trop de recherche de ce nombre
            if mll==0 :
                if V[l]!=0: # Pas de solution
                    break
            else:
                # on divise M[l][l] et V[l] par leur pgcd avant d'inverser le coefficient
                d=pgcd(M[l][l],V[l])
                if d>1:
                    M[l][l]//=d
                    V[l]//=d
                inv=inv_mod(M[l][l],modulo)
                if inv is not None:
                    M[l][l]=1
                    V[l]=(V[l]*inv)%modulo
                else :
                    break
        else: # Si on a réussi a inverser, on rajoute à la liste des candidats
            reponses.append([M,V,rg])
    if reponses:
        i_min=0
        val_min=10000000
        for i,(M,V,rg) in enumerate(reponses):
            val=sum(V)
            if val<val_min:
                i_min=i
                val_min=val

        return reponses[i_min]
    else: return None
#-----------------------------------Affichage Latex des matrices précédentes

def to_latex_reduit(matrice,vecteur):
    """
    Prépare le texte latex pour afficher les systemes sous forme réduite (sans laisser les espaces vides si le coefficient est 0
    """
    n=len(matrice)
    #texte_latex=r"Les variables en \textcolor{red}{rouge} sont celles qui ont Ã©tÃ© choisies comme valant 0 (mais on aurait pu faire d'autres choix) ou bien qui n'ont pas de solution \\"+"\n"
    texte_latex=r"$\left\{\begin{array}{c c l}"
    for l in range(n):
        #On ajoute les coefficients non nuls
        temp=""
        for k,coeff in enumerate(matrice[l]):
            if coeff:
                if coeff!=1:
                    temp+=str(coeff)
                temp+="n_{"+str(k)+"} +"
        temp=temp[:-1]
        #if not temp : temp = r"\textcolor{red}{"+"0"*(vecteur[k]!=0)+"n_{"+str(l)+"}}"
        if not temp : temp = r"\textcolor{red}{"+"0.n_{"+str(l)+"}}"
        texte_latex+=temp+"&=& "+str(vecteur[l])+r"\\"
    texte_latex+=r"\end{array}\right.$"
    return texte_latex

def to_latex(matrice,vecteur):
    """
    Prépare le texte latex pour afficher les systemes sous forme non rÃ©duite (en laissant les espaces vides si le coefficient est 0
    """
    n=len(matrice)
    #texte_latex=r"Les variables en \textcolor{red}{rouge} sont celles qui ont Ã©tÃ© choisies comme valant 0 (mais on aurait pu faire d'autres choix) ou bien qui n'ont pas de solution \\"
    texte_latex=r"$\left\{\begin{array}{l c l}"
    for l in range(n):
        #On ajoute les coefficients
        temp=""
        tous_nuls=all([c==0 for c in matrice[l]])
        for k,coeff in enumerate(matrice[l]):
            if coeff:
                if coeff!=1:
                    temp+=str(coeff)
                else :
                    temp+="\phantom{0}"
                temp+="n_{"+str(k)+"} +"
            else :
                if tous_nuls and k==l :
                    temp += r"\textcolor{red}{"+"0"*(vecteur[k]!=0)+"n_{"+str(l)+"}} "
                else:
                    temp+="\phantom{ 0n_{"+str(k)+"} +\ } "
        temp=temp[:-1]
        texte_latex+=temp+"&=& "+str(vecteur[l])+r"\\"
    texte_latex+=r"\end{array}\right.$"+"\n\n"
    return texte_latex

def titre_latex(titre):
    return r"\begin{LARGE}"+titre+r"\end{LARGE}"+"\n\n"+r"\vspace{2em}"





