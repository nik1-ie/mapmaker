import fltk

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
    chemin = 'pack1/tuiles/'

    larg = fltk.largeur_fenetre()
    haut = fltk.hauteur_fenetre()
    fltk.rectangle(0, 0, larg, haut, remplissage='grey')
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j] != None:
                fltk.image(j * (larg / lignes), i * (haut/colonnes), chemin + plateau[i][j] + '.png', largeur=larg // lignes, hauteur=haut // colonnes, ancrage='nw')
    fltk.mise_a_jour()


fltk.cree_fenetre(800, 800)
plateau = [['SSSS','SSSS','SSSS','SSSS', None],
           ['SSSS','SHGS', 'SHRH', 'SHFH', None],
           ['SSSS', None, 'RMPP', 'FMMM', 'PPMM'],
           ['SSSS', None, None, None, None],
           [None, None, None, None, None]]
lignes = 5
colonnes = 5
affichage_map(plateau, lignes, colonnes)
quadrillage(lignes, colonnes)
while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "Quitte":
            fltk.ferme_fenetre()
            break
        fltk.mise_a_jour()