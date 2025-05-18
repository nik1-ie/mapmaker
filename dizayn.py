import fltk
import random
import sauvegarde
from globals import *
from utilitaires import dessiner_curseur_souris, mise_a_jour_avec_curseur, rectangle_arrondi, initialiser_gouttes, bouton_clique

def animer_pluie(gouttes):
    """
    Anime et dessine les gouttes de pluie.
    """
    for i in range(len(gouttes)):
        xg, yg, vitesse = gouttes[i]
        fltk.ligne(xg, yg, xg, yg+12, couleur=COUL_PLUIE, epaisseur=2)
        gouttes[i][1] += vitesse
        if gouttes[i][1] > HAUTEUR_FENETRE:
            gouttes[i][0] = random.randint(0, LARGEUR_FENETRE)
            gouttes[i][1] = random.randint(-20, 0)
            gouttes[i][2] = random.randint(10, 18)

def dessiner_titre():
    """
    Dessine le titre principal avec ses bordures.
    """
    largeur_titre = fltk.largeur_fenetre() * 0.65
    hauteur_titre = fltk.hauteur_fenetre() * 0.15
    
    x_titre = (fltk.largeur_fenetre() - largeur_titre) // 2
    
    y_titre = fltk.hauteur_fenetre() * 0.05
    
    rectangle_arrondi(x_titre-6, y_titre-6, largeur_titre+12, hauteur_titre+12, 22, COUL_MENU_CONTOUR_FONCE, "", 3)
    rectangle_arrondi(x_titre-2, y_titre-2, largeur_titre+4, hauteur_titre+4, 18, COUL_MENU_CONTOUR_CLAIR, "", 2)
    rectangle_arrondi(x_titre, y_titre, largeur_titre, hauteur_titre, 16, "", COUL_ENTETE, 0)
    
    taille_texte = int(largeur_titre * 0.13)
    fltk.texte(x_titre + largeur_titre//2, y_titre + 20, "MAPMAKER", couleur=COUL_ENTETE_TEXTE,
         police=POLICE_PIXEL, taille=taille_texte, ancrage="n")
    
    return x_titre, y_titre, largeur_titre, hauteur_titre


def dessiner_sous_titre(x_titre, y_titre, largeur_titre, hauteur_titre):
    """
    Dessine le sous-titre avec sa bordure.
    """
    largeur_sous, hauteur_sous = 320, 34
    x_sous = (LARGEUR_FENETRE - largeur_sous) // 2
    y_sous = y_titre + hauteur_titre - 12
    
    rectangle_arrondi(x_sous, y_sous, largeur_sous, hauteur_sous, 10, COUL_MENU_CONTOUR_FONCE, COUL_SOUS_MENU, 2)
    fltk.texte(x_sous + largeur_sous//2, y_sous + hauteur_sous//2, "façonne ton propre univers",
          couleur=COUL_SOUS_MENU_TEXTE, police=POLICE_PIXEL, taille=17, ancrage="c")

def dessiner_cadre_menu():
    """
    Dessine le cadre principal du menu.
    """
    largeur_menu = fltk.largeur_fenetre() * 0.7
    hauteur_menu = fltk.hauteur_fenetre() * 0.6
    
    x_menu = (fltk.largeur_fenetre() - largeur_menu) // 2
    
    y_menu = fltk.hauteur_fenetre() * 0.3
    
    rectangle_arrondi(x_menu-6, y_menu-6, largeur_menu+12, hauteur_menu+12, 24, COUL_MENU_CONTOUR_FONCE, "", 3)
    rectangle_arrondi(x_menu-2, y_menu-2, largeur_menu+4, hauteur_menu+4, 20, COUL_MENU_CONTOUR_CLAIR, "", 2)
    rectangle_arrondi(x_menu, y_menu, largeur_menu, hauteur_menu, 16, "", COUL_MENU, 0)
    
    return x_menu, y_menu, largeur_menu


def menu():
    gouttes = initialiser_gouttes(NB_GOUTTES)
    while True:
        fltk.efface_tout()
        largeur_fenetre_val = fltk.largeur_fenetre()
        hauteur_fenetre_val = fltk.hauteur_fenetre()

        fltk.image(largeur_fenetre_val//2, hauteur_fenetre_val//2, "arbre1.png",
              largeur=largeur_fenetre_val, hauteur=hauteur_fenetre_val, ancrage="center")
        animer_pluie(gouttes)

        x_titre, y_titre, largeur_titre, hauteur_titre = dessiner_titre()
        dessiner_sous_titre(x_titre, y_titre, largeur_titre, hauteur_titre)
        x_menu, y_menu, largeur_menu = dessiner_cadre_menu()

        NB_BOUTONS = len(etiquettes)
        hauteur_menu = fltk.hauteur_fenetre() * 0.6
        largeur_bouton = largeur_menu * 0.9

        espace_total = hauteur_menu * 0.1
        hauteur_bouton = (hauteur_menu - espace_total) / NB_BOUTONS * 0.8
        espacement = (hauteur_menu - espace_total) / NB_BOUTONS * 0.2

        x_bouton = x_menu + (largeur_menu - largeur_bouton) // 2
        y_debut = y_menu + espace_total / 2 + 14

        x_souris, y_souris = fltk.abscisse_souris(), fltk.ordonnee_souris()
        
        for i, (icone, etiquette) in enumerate(etiquettes):
            y_bouton = y_debut + i * (hauteur_bouton + espacement)
            survole = x_bouton <= x_souris <= x_bouton + largeur_bouton and y_bouton <= y_souris <= y_bouton + hauteur_bouton
            
            if survole:
                rectangle_arrondi(x_bouton, y_bouton, largeur_bouton, hauteur_bouton, 10, COUL_MENU_CONTOUR_FONCE, "", 2)
                rectangle_arrondi(x_bouton, y_bouton, largeur_bouton, hauteur_bouton, 10, COUL_MENU_CONTOUR_MOYEN, COUL_BOUTON_SURVOL, 2)
                couleur_texte = COUL_MENU
                couleur_icone = COUL_MENU
            else:
                rectangle_arrondi(x_bouton, y_bouton, largeur_bouton, hauteur_bouton, 10, "", COUL_BOUTON, 0)
                couleur_texte = COUL_BOUTON_TEXTE
                couleur_icone = COUL_BOUTON_ICONE
            
            fltk.texte(x_menu + 28, y_bouton + hauteur_bouton // 2, icone,
                  couleur=couleur_icone, police=POLICE_PIXEL, taille=24, ancrage="c")
            fltk.texte(x_bouton + largeur_bouton // 2, y_bouton + hauteur_bouton // 2, etiquette,
                  couleur=couleur_texte, police=POLICE_PIXEL, taille=22, ancrage="c")
            fltk.texte(x_menu + largeur_menu - 28, y_bouton + hauteur_bouton // 2, icone,
                  couleur=couleur_icone, police=POLICE_PIXEL, taille=24, ancrage="c")
        
        dessiner_curseur_souris()
        
        ev = fltk.donne_ev()
        if ev is not None:
            tev = fltk.type_ev(ev)
            if tev == "Redimension":
                gouttes = initialiser_gouttes(NB_GOUTTES)
                continue
            if tev == "ClicGauche":
                x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
                bouton = bouton_clique(x, y, x_bouton, y_debut, largeur_bouton, hauteur_bouton, espacement, NB_BOUTONS)
                if bouton is not None:
                    if etiquettes[bouton][1] == "quitter":
                        return "quitter"
                    elif etiquettes[bouton][1] == "nouvelle carte":
                        return "nouvelle_carte"
                    elif etiquettes[bouton][1] == "explorer cartes":
                        from graphique import afficher_galerie_captures
                        afficher_galerie_captures()
                    elif etiquettes[bouton][1] == "sauvegarde":
                        fltk.efface_tout()
                        sauvegarde.save()
                        break
            elif tev == "Quitte":
                return "quitter"
        
        mise_a_jour_avec_curseur()
        fltk.attente(0.01)

if __name__ == "__main__":
    fltk.cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    action = menu()
    print(f"Action sélectionnée : {action}")
    fltk.ferme_fenetre()
