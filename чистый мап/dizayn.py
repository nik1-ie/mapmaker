import fltk
import random
from globals import *
import utilitaires
import graphique_utils

def animer_pluie(gouttes, largeur_fenetre, hauteur_fenetre):
    """
    Anime et dessine les gouttes de pluie.
    """
    for i in range(len(gouttes)):
        xg, yg, vitesse = gouttes[i]
        fltk.ligne(xg, yg, xg, yg+12, couleur=COUL_PLUIE, epaisseur=2)
        gouttes[i][1] += vitesse
        if gouttes[i][1] > hauteur_fenetre:
            gouttes[i][0] = random.randint(0, largeur_fenetre)
            gouttes[i][1] = random.randint(-20, 0)
            gouttes[i][2] = random.randint(10, 18)

def dessiner_titre(largeur_fenetre, hauteur_fenetre):
    """
    Dessine le titre principal avec ses bordures.
    """
    largeur_titre = largeur_fenetre * 0.65
    hauteur_titre = hauteur_fenetre * 0.15

    
    x_titre = (largeur_fenetre - largeur_titre) // 2
    
    y_titre = hauteur_fenetre * 0.05
    
    graphique_utils.rectangle_arrondi(x_titre-6, y_titre-6, largeur_titre+12, hauteur_titre+12, 22, COUL_MENU_CONTOUR_FONCE, "", 3)
    graphique_utils.rectangle_arrondi(x_titre-2, y_titre-2, largeur_titre+4, hauteur_titre+4, 18, COUL_MENU_CONTOUR_CLAIR, "", 2)
    graphique_utils.rectangle_arrondi(x_titre, y_titre, largeur_titre, hauteur_titre, 16, "", COUL_ENTETE, 0)
    
    taille_texte = int(largeur_titre * 0.13)
    fltk.texte(x_titre + largeur_titre//2, y_titre + hauteur_titre//2, "MAPMAKER", couleur=COUL_ENTETE_TEXTE,
         police=POLICE_PIXEL, taille=taille_texte, ancrage="c")
    
    return x_titre, y_titre, largeur_titre, hauteur_titre


def dessiner_sous_titre(x_titre, y_titre, largeur_titre, hauteur_titre, largeur_fenetre):
    """
    Dessine le sous-titre avec sa bordure.
    """
    largeur_sous = min(max(int(largeur_fenetre * 0.25), 220), 500)
    hauteur_sous = 34
    x_sous = (largeur_fenetre - largeur_sous) // 2
    y_sous = y_titre + hauteur_titre - 6
    
    graphique_utils.rectangle_arrondi(x_sous, y_sous, largeur_sous, hauteur_sous, 10, COUL_MENU_CONTOUR_FONCE, COUL_SOUS_MENU, 2)
    taille_sous_titre = min(max(int(largeur_sous * 0.08), 13), 28)
    fltk.texte(x_sous + largeur_sous//2, y_sous + hauteur_sous//2, "façonne ton univers",
          couleur=COUL_SOUS_MENU_TEXTE, police=POLICE_PIXEL, taille=taille_sous_titre, ancrage="c")

def dessiner_cadre_menu():
    """
    Dessine le cadre principal du menu.
    """
    largeur_menu = fltk.largeur_fenetre() * 0.7
    hauteur_menu = fltk.hauteur_fenetre() * 0.6
    
    x_menu = (fltk.largeur_fenetre() - largeur_menu) // 2
    
    y_menu = fltk.hauteur_fenetre() * 0.3
    
    graphique_utils.rectangle_arrondi(x_menu-6, y_menu-6, largeur_menu+12, hauteur_menu+12, 24, COUL_MENU_CONTOUR_FONCE, "", 3)
    graphique_utils.rectangle_arrondi(x_menu-2, y_menu-2, largeur_menu+4, hauteur_menu+4, 20, COUL_MENU_CONTOUR_CLAIR, "", 2)
    graphique_utils.rectangle_arrondi(x_menu, y_menu, largeur_menu, hauteur_menu, 16, "", COUL_MENU, 0)
    
    return x_menu, y_menu, largeur_menu


def menu():
    gouttes = utilitaires.initialiser_gouttes(NB_GOUTTES)
    while True:
        fltk.efface_tout()
        largeur_fenetre_val = fltk.largeur_fenetre()
        hauteur_fenetre_val = fltk.hauteur_fenetre()

        fltk.image(largeur_fenetre_val//2, hauteur_fenetre_val//2, "icons/arbre.png",
              largeur=largeur_fenetre_val, hauteur=hauteur_fenetre_val, ancrage="center")
        animer_pluie(gouttes, largeur_fenetre_val, hauteur_fenetre_val)


        x_titre, y_titre, largeur_titre, hauteur_titre = dessiner_titre(largeur_fenetre_val, hauteur_fenetre_val) 
        dessiner_sous_titre(x_titre, y_titre, largeur_titre, hauteur_titre, largeur_fenetre_val)

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
                graphique_utils.rectangle_arrondi(x_bouton, y_bouton, largeur_bouton, hauteur_bouton, 10, COUL_MENU_CONTOUR_FONCE, "", 2)
                graphique_utils.rectangle_arrondi(x_bouton, y_bouton, largeur_bouton, hauteur_bouton, 10, COUL_MENU_CONTOUR_MOYEN, COUL_BOUTON_SURVOL, 2)
                couleur_texte = COUL_MENU
                couleur_icone = COUL_MENU
            else:
                graphique_utils.rectangle_arrondi(x_bouton, y_bouton, largeur_bouton, hauteur_bouton, 10, "", COUL_BOUTON, 0)
                couleur_texte = COUL_BOUTON_TEXTE
                couleur_icone = COUL_BOUTON_ICONE
            
            fltk.texte(x_menu + 28, y_bouton + hauteur_bouton // 2, icone,
                  couleur=couleur_icone, police=POLICE_PIXEL, taille=24, ancrage="c")
            fltk.texte(x_bouton + largeur_bouton // 2, y_bouton + hauteur_bouton // 2, etiquette,
                  couleur=couleur_texte, police=POLICE_PIXEL, taille=22, ancrage="c")
            fltk.texte(x_menu + largeur_menu - 28, y_bouton + hauteur_bouton // 2, icone,
                  couleur=couleur_icone, police=POLICE_PIXEL, taille=24, ancrage="c")
        
        graphique_utils.dessiner_curseur_souris()
        
        ev = fltk.donne_ev()
        if ev is not None:
            tev = fltk.type_ev(ev)
            if tev == "Redimension":
                gouttes = utilitaires.initialiser_gouttes(NB_GOUTTES)
                continue
            if tev == "ClicGauche":
                x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
                bouton = utilitaires.bouton_clique(x, y, x_bouton, y_debut, largeur_bouton, hauteur_bouton, espacement, NB_BOUTONS)
                if bouton is not None:
                    if etiquettes[bouton][1] == "quitter":
                        return "quitter"
                    elif etiquettes[bouton][1] == "nouvelle carte":
                        return "nouvelle_carte"
                    elif etiquettes[bouton][1] == "explorer cartes":
                        from actions import afficher_galerie_captures
                        afficher_galerie_captures()
            elif tev == "Quitte":
                return "quitter"
        
        graphique_utils.mise_a_jour_avec_curseur()
        fltk.attente(0.01)

if __name__ == "__main__":
    fltk.cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    action = menu()
    fltk.ferme_fenetre()
