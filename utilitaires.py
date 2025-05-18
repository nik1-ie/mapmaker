import fltk
import random
from globals import *

def dessiner_curseur_souris(image: str = "paw.png", taille: int = 32):
    """
    Dessine un curseur personnalisé à la position actuelle de la souris
    """
    x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
    fltk.image(x, y, image, largeur=taille, hauteur=taille, ancrage="center", tag="curseur")

def mise_a_jour_avec_curseur():
    """Wrapper pour mise_a_jour qui dessine toujours le curseur avant la mise à jour."""
    dessiner_curseur_souris()
    fltk.mise_a_jour()

def rectangle_arrondi(x, y, l, h, r, contour, remplissage, epaisseur=1):
    fltk.cercle(x+r, y+r, r, couleur="", remplissage=remplissage)
    fltk.cercle(x+l-r, y+r, r, couleur="", remplissage=remplissage)
    fltk.cercle(x+r, y+h-r, r, couleur="", remplissage=remplissage)
    fltk.cercle(x+l-r, y+h-r, r, couleur="", remplissage=remplissage)
    fltk.rectangle(x+r, y, x+l-r, y+h, couleur="", remplissage=remplissage)
    fltk.rectangle(x, y+r, x+l, y+h-r, couleur="", remplissage=remplissage)
    fltk.rectangle(x+r, y, x+l-r, y+r, couleur="", remplissage=remplissage)
    fltk.rectangle(x, y+r, x+r, y+h-r, couleur="", remplissage=remplissage)
    fltk.rectangle(x+l-r, y+r, x+l, y+h-r, couleur="", remplissage=remplissage)
    fltk.rectangle(x+r, y+h-r, x+l-r, y+h, couleur="", remplissage=remplissage)
    if contour and epaisseur > 0:
        fltk.arc(x+r, y+r, r, 90, 90, couleur=contour, epaisseur=epaisseur)
        fltk.arc(x+l-r, y+r, r, 90, 0, couleur=contour, epaisseur=epaisseur)
        fltk.arc(x+l-r, y+h-r, r, 90, 270, couleur=contour, epaisseur=epaisseur)
        fltk.arc(x+r, y+h-r, r, 90, 180, couleur=contour, epaisseur=epaisseur)
        fltk.ligne(x+r, y, x+l-r, y, couleur=contour, epaisseur=epaisseur)
        fltk.ligne(x+l, y+r, x+l, y+h-r, couleur=contour, epaisseur=epaisseur)
        fltk.ligne(x+r, y+h, x+l-r, y+h, couleur=contour, epaisseur=epaisseur)
        fltk.ligne(x, y+r, x, y+h-r, couleur=contour, epaisseur=epaisseur)


def initialiser_gouttes(nb_gouttes):
    """Initialise les gouttes de pluie"""
    gouttes = []
    for _ in range(nb_gouttes):
        gouttes.append([
            random.randint(0, LARGEUR_FENETRE),
            random.randint(0, HAUTEUR_FENETRE),
            random.randint(10, 18)
        ])
    return gouttes

def bouton_clique(x, y, x_bouton, y_debut, largeur_bouton, hauteur_bouton, espacement, nb_boutons):
    """Renvoie l'indice du bouton sur lequel on a cliqué, ou None."""
    for i in range(nb_boutons):
        y_bouton = y_debut + i * (hauteur_bouton + espacement)
        if x_bouton <= x <= x_bouton + largeur_bouton and y_bouton <= y <= y_bouton + hauteur_bouton:
            return i
    return None