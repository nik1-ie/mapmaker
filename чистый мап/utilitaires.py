import random
import globals


def initialiser_gouttes(nb_gouttes):
    """Initialise les gouttes de pluie"""
    gouttes = []
    for _ in range(nb_gouttes):
        gouttes.append([
            random.randint(0, globals.LARGEUR_FENETRE),
            random.randint(0, globals.HAUTEUR_FENETRE),
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

