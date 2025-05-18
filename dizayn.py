from fltk import *
import random
from globals import *
from utilitaires import dessiner_curseur_souris, mise_a_jour_avec_curseur, rectangle_arrondi, initialiser_gouttes, bouton_clique


def menu():
    """
    Affiche le menu principal et retourne l'action choisie
    """
    gouttes = initialiser_gouttes(NB_GOUTTES)

    while True:
        efface_tout()
        image(LARGEUR_FENETRE//2, HAUTEUR_FENETRE//2, "arbre1.png", largeur=LARGEUR_FENETRE, hauteur=HAUTEUR_FENETRE, ancrage="center")
        for i in range(NB_GOUTTES):
            xg, yg, vitesse = gouttes[i]
            ligne(xg, yg, xg, yg+12, couleur=COUL_PLUIE, epaisseur=2)
            gouttes[i][1] += vitesse
            if gouttes[i][1] > HAUTEUR_FENETRE:
                gouttes[i][0] = random.randint(0, LARGEUR_FENETRE)
                gouttes[i][1] = random.randint(-20, 0)
                gouttes[i][2] = random.randint(10, 18)

        largeur_titre, hauteur_titre = 390, 80
        x_titre = (LARGEUR_FENETRE - largeur_titre) // 2
        y_titre = 32
        rectangle_arrondi(x_titre-6, y_titre-6, largeur_titre+12, hauteur_titre+12, 22, COUL_MENU_CONTOUR_FONCE, "", 3)
        rectangle_arrondi(x_titre-2, y_titre-2, largeur_titre+4, hauteur_titre+4, 18, COUL_MENU_CONTOUR_CLAIR, "", 2)
        rectangle_arrondi(x_titre, y_titre, largeur_titre, hauteur_titre, 16, "", COUL_ENTETE, 0)
        texte(x_titre + largeur_titre//2, y_titre + 10, "MAPMAKER", couleur=COUL_ENTETE_TEXTE,
              police=POLICE_PIXEL, taille=36, ancrage="n")
        texte(x_titre + largeur_titre//2, y_titre + 49, "", couleur=COUL_ENTETE_TEXTE,
              police=POLICE_PIXEL, taille=36, ancrage="n")

        largeur_sous, hauteur_sous = 320, 34
        x_sous = (LARGEUR_FENETRE - largeur_sous) // 2
        y_sous = y_titre + hauteur_titre - 12
        rectangle_arrondi(x_sous, y_sous, largeur_sous, hauteur_sous, 10, COUL_MENU_CONTOUR_FONCE, COUL_SOUS_MENU, 2)
        texte(x_sous + largeur_sous//2, y_sous + hauteur_sous//2, "façonne ton propre univers",
              couleur=COUL_SOUS_MENU_TEXTE, police=POLICE_PIXEL, taille=17, ancrage="c")

        largeur_menu, hauteur_menu = 400, 340
        x_menu = (LARGEUR_FENETRE - largeur_menu) // 2
        y_menu = 180
        rectangle_arrondi(x_menu-6, y_menu-6, largeur_menu+12, hauteur_menu+12, 24, COUL_MENU_CONTOUR_FONCE, "", 3)
        rectangle_arrondi(x_menu-2, y_menu-2, largeur_menu+4, hauteur_menu+4, 20, COUL_MENU_CONTOUR_CLAIR, "", 2)
        rectangle_arrondi(x_menu, y_menu, largeur_menu, hauteur_menu, 16, "", COUL_MENU, 0)

        x_souris, y_souris = abscisse_souris(), ordonnee_souris()

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
            texte(x_menu + 28, y_bouton + hauteur_bouton // 2, icone,
                couleur=couleur_icone, police=POLICE_PIXEL, taille=24, ancrage="c")
            texte(x_bouton + largeur_bouton // 2, y_bouton + hauteur_bouton // 2, etiquette,
                couleur=couleur_texte, police=POLICE_PIXEL, taille=22, ancrage="c")
            texte(x_menu + largeur_menu - 28, y_bouton + hauteur_bouton // 2, icone,
                couleur=couleur_icone, police=POLICE_PIXEL, taille=24, ancrage="c")

        dessiner_curseur_souris()


        ev = donne_ev()
        if ev is not None:
            tev = type_ev(ev)
            if tev == "ClicGauche":
                x, y = abscisse(ev), ordonnee(ev)
                bouton = bouton_clique(x, y, x_bouton, y_debut, largeur_bouton, hauteur_bouton, espacement, NB_BOUTONS)
                if bouton is not None:
                    if etiquettes[bouton][1] == "quitter":
                        return "quitter"
                    elif etiquettes[bouton][1] == "nouvelle carte":
                        return "nouvelle_carte"
            elif tev == "Quitte":
                return "quitter"

        mise_a_jour_avec_curseur()
        attente(0.01)

if __name__ == "__main__":
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    action = menu()
    print(f"Action sélectionnée : {action}")
    ferme_fenetre()
