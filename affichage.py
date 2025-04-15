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

def emplacement_valide(grille, i, j, nom_tuile):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dico = {0:2, 1: 3, 2: 0, 3: 1}
    bon = True
    for indice in range(len(directions)):
        x = directions[indice][0]
        y = directions[indice][1]
        if grille[i + x][j + y][dico[indice]] == nom_tuile[indice]:
            bon = True
        else:
            bon = False
    return bon

def plateau_vide(l, c):
    '''
    Fonction permettant de créer une grille vide à remplir par la suite.
    Arguments : l, c (int) - taille des lignes et colonnes
    Returns : plateau (list de list) - grille vide
    '''
    plateau = [[None for _ in range(c)] for _ in range(l)]
    return plateau

def main():
    lignes = 10
    colonnes = 10
    plateau = plateau_vide(lignes, colonnes)
    affichage_map(plateau, lignes, colonnes)
    quadrillage(lignes, colonnes)
    # print(emplacement_valide(plateau, 1, 2, 'SHRH')) - Y'a un pb quand tout est vide ... ?

    
    larg = fltk.largeur_fenetre() //lignes
    haut = fltk.hauteur_fenetre() // colonnes
    while True:
            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            if tev == "Quitte":
                fltk.ferme_fenetre()
                break
            if tev == "ClicGauche":
                abs = fltk.abscisse(ev)
                ord = fltk.ordonnee(ev)
                coord_clic = (abs//larg, ord//haut)
                print(coord_clic)
                    
            fltk.mise_a_jour()


if __name__ == "__main__":
    fltk.cree_fenetre(800, 800)
    main()
    plateau = [['SSSS','SSSS','SSSS','SSSS', None],
            ['SSSS','SHGS', 'SHRH', 'SHFH', None],
            ['SSSS', None, 'RMPP', 'FMMM', 'PPMM'],
            ['SSSS', None, None, None, None],
            [None, None, None, None, None]]

    plateau_pasbon = [['SSSS','SSSS','SSSS','SSSS', None],
            ['SSSS','SSDH', 'SHRH', 'SHFH', None],
            ['SSSS', None, 'RMPP', 'FMMM', 'PPMM'],
            ['SSSS', None, None, None, None],
            [None, None, None, None, None]]# pour tester avec un plateau qui n'existe pas
