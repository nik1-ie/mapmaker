import fltk
import globals
import graphique_utils



def quadrillage(lignes, colonnes):
    '''
    Fonction qui créé et affiche la grille en fonction de la taille donnée.
    Arguments: lignes(int) - nombres de lignes de la grille
               colonnes(int) - nombres de colonnes de la grille
    '''
    x = 0
    y = 0
    fltk.ligne(0, 0, fltk.largeur_fenetre(), 0)
    for _ in range(lignes + 1):
        fltk.ligne(0, y, fltk.largeur_fenetre(),y)
        y += fltk.hauteur_fenetre()/colonnes

    for _ in range(colonnes + 1):
        fltk.ligne(x, 0, x, fltk.hauteur_fenetre())
        x += fltk.largeur_fenetre()/lignes
    fltk.mise_a_jour()


def affichage_map(plateau, lignes, colonnes):
    '''
    Fonction qui affiche le plateau de jeu en fonction de la taille donnée.
    Arguments: plateau(list de list) - grille à afficher
               lignes(int) - nombres de lignes de la grille
               colonnes(int) - nombres de colonnes de la grille
    '''
    chemin = 'pack1/tuiles/'

    larg = fltk.largeur_fenetre()
    haut = fltk.hauteur_fenetre()
    fltk.rectangle(0, 0, larg, haut, remplissage='grey')
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j] != None:
                fltk.image(j * (larg / lignes), i * (haut/colonnes), chemin + plateau[i][j] + '.png', largeur=larg // lignes, hauteur=haut // colonnes, ancrage='nw')
    fltk.mise_a_jour()

def plateau_vide(l, c):
    '''
    Fonction permettant de créer une grille vide à remplir par la suite.
    Arguments : l, c (int) - taille des lignes et colonnes
    Returns : plateau (list de list) - grille vide
    '''
    plateau = [[None for _ in range(c)] for _ in range(l)]
    return plateau

def dessiner_carte(plateau, lignes, colonnes, pan_x, pan_y, facteur_zoom, min_x=0, min_y=0):
    """
    Dessine la carte en fonction du plateau, des dimensions, du décalage et du facteur de zoom.
    """
    taille_case = round(globals.TAILLE_CASE_BASE * facteur_zoom)
    largeur = fltk.largeur_fenetre()
    hauteur = fltk.hauteur_fenetre()
    
    fltk.rectangle(0, 0, largeur, hauteur, remplissage='#F4E2BD')

    premier_indice_x = pan_x // taille_case
    premier_indice_y = pan_y // taille_case
    dernier_indice_x = premier_indice_x + largeur // taille_case + 2
    dernier_indice_y = premier_indice_y + (hauteur - globals.HAUTEUR_BARRE_OUTILS) // taille_case + 2
    
    for indice_y in range(premier_indice_y, dernier_indice_y):
        y = indice_y * taille_case - pan_y + globals.HAUTEUR_BARRE_OUTILS
        for indice_x in range(premier_indice_x, dernier_indice_x):
            x = indice_x * taille_case - pan_x
            matrice_y = indice_y - min_x
            matrice_x = indice_x - min_y
            if 0 <= matrice_y < lignes and 0 <= matrice_x < colonnes and plateau[matrice_y][matrice_x] is not None:
                chemin_image = f"./pack1/tuiles/{plateau[matrice_y][matrice_x]}.png"
                fltk.image(x + taille_case // 2, y + taille_case // 2,
                        chemin_image, largeur=taille_case, hauteur=taille_case,
                        ancrage='center')
    
    if globals.afficher_grille:
        for indice_y in range(premier_indice_y, dernier_indice_y + 1):
            y = indice_y * taille_case - pan_y + globals.HAUTEUR_BARRE_OUTILS
            fltk.ligne(0, y, largeur, y, couleur='#444444')
        for indice_x in range(premier_indice_x, dernier_indice_x + 1):
            x = indice_x * taille_case - pan_x
            fltk.ligne(x, globals.HAUTEUR_BARRE_OUTILS, x, hauteur, couleur='#444444')
    
    graphique_utils.dessiner_barre_outils()
    
    if globals.mini_carte_active:
        dessiner_mini_carte(plateau, lignes, colonnes)

    
    graphique_utils.mise_a_jour_avec_curseur()


def dessiner_mini_carte(plateau, lignes, colonnes):
    """
    Dessine une mini-carte dans le coin inférieur droit de la fenêtre pour montrer un aperçu de la carte entière.
    """
    largeur = fltk.largeur_fenetre()
    hauteur = fltk.hauteur_fenetre()
    
    mini_largeur = 150
    mini_hauteur = 150
    marge = 10
    
    x_mini = largeur - mini_largeur - marge
    y_mini = hauteur - mini_hauteur - marge
    
    graphique_utils.rectangle_arrondi(x_mini, y_mini, mini_largeur, mini_hauteur, 5, "#444444", "#FFFFFF", 2)
    
    echelle_x = (mini_largeur - 10) / (colonnes * globals.TAILLE_CASE_BASE)
    echelle_y = (mini_hauteur - 10) / (lignes * globals.TAILLE_CASE_BASE)
    echelle = min(echelle_x, echelle_y)
    
    for i in range(lignes):
        for j in range(colonnes):
            mini_x = x_mini + 5 + j * globals.TAILLE_CASE_BASE * echelle
            mini_y = y_mini + 5 + i * globals.TAILLE_CASE_BASE * echelle
            mini_taille = globals.TAILLE_CASE_BASE * echelle

            couleur = '#F4E2BD'
            if plateau[i][j] is not None:
                couleur = '#8899FF'
            
            fltk.rectangle(mini_x, mini_y, mini_x + mini_taille, mini_y + mini_taille, 
                          remplissage=couleur, epaisseur=0)

