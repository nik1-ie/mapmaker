# --- Imports
import fltk
import globals
import test_solveur
# --- Constantes
plateau = []
lignes, colonnes = 0, 0
largeur, hauteur = 0, 0
window = False
option_id = 1
# --- Fonctions
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

    fltk.rectangle(0, 0, largeur, hauteur, remplissage='grey')
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j] != None:
                fltk.image(j * (largeur / lignes), i * (hauteur/colonnes), chemin + plateau[i][j] + '.png', largeur=largeur // lignes, hauteur=hauteur // colonnes, ancrage='nw')
    fltk.mise_a_jour()

def plateau_vide(l, c):
    '''
    Fonction permettant de créer une grille vide à remplir par la suite.
    Arguments : l, c (int) - taille des lignes et colonnes
    Returns : plateau (list de list) - grille vide
    '''
    plateau = [[None for _ in range(c)] for _ in range(l)]
    return plateau

def options_tab(opt):
    '''
    Fonction faisant des listes de tuiles afin de les afficher plus facilement.
    '''
    opt2 = []
    for i in range(0, len(opt), 5):
        opt2.append(opt[i:i+5])
    opt2 = opt2[option_id:]
    return opt2


def options(pos):
    '''
    Affiche une fenêtre de choix de tuiles selon la position à laquelle on se trouve.
    '''
    print("IN the window function ???")
    global window, option_id
    chemin = globals.pack1_way
    window = True
    
    yess = plateau
    nom = test_solveur.recup_nom(yess, pos[0], pos[1])
    option = test_solveur.rechercher_tuiles(nom)
    option = options_tab(option)
    popup_width = largeur - 100
    popup_height = hauteur - 100
    x1 = (largeur - popup_width) // 2
    y1 = (hauteur - popup_height) // 2
    x2 = x1 + popup_width
    y2 = y1 + popup_height

    fltk.rectangle(x1, y1, x2, y2, remplissage='#FFFFFF', epaisseur=2, couleur='#000000')
    fltk.texte((x1 + x2) // 2, y1 + 20, "Tuiles possibles", ancrage='center', taille=16, couleur='#000000')

    def affiche():
        print("AFFIIIICHE")
        col = x1 + 5
        coords = []
        for line in option:
            for i in range(len(line)):
                tuile = line[i]
                tuile_width = (popup_width ) // 6  # 5 tuiles max par ligne
                tuile_height = tuile_width
                margin = 10

                # Calcul de la position de la tuile dans le popup
                x_tuile = col + i * (tuile_width + margin)
                y_tuile = y1 + 50 + option.index(line) * (tuile_height + margin)

                # Si la tuile dépasse le popup, on arrête d'afficher cette ligne
                if x_tuile + tuile_width > x2 :
                     break
                if y_tuile + tuile_height > y2:
                    break
                fltk.image(x_tuile, y_tuile, f"{chemin}{tuile}.png", largeur=tuile_width, hauteur=tuile_height, ancrage='nw', tag="choix")
                # Ajoute les coordonnées des coins de chaque image dans coords
                coords.append([
                    (x_tuile, x_tuile + tuile_width), # coord de x
                    (y_tuile, y_tuile + tuile_height),  # coord de y
                ])
                # print(tuile, coords[i])
        return coords
    
    c = affiche()

    while True:
        tev = fltk.donne_ev()
        ev = fltk.type_ev(tev) #works when we replace donne_ev by attend_ev.
        if ev == "Clic_gauche":
            x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
            for idx, ((x_min, x_max), (y_min, y_max)) in enumerate(c): #look for where the clic is. if not on any tuile, ignores.
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    # Trouver la tuile correspondante
                    tuile = None
                    count = 0
                    for line in option:
                        for t in line:
                            if count == idx:
                                tuile = t
                                break
                            count += 1
                        if tuile is not None:
                            return tuile #on return la tuile choisie normalement T-T
                    
        elif ev == "Enter":
            # fltk.efface("choix")
            c = affiche()
        elif ev == "Escape":
            window = False
            break
        elif ev == "Down":
            option_id += 1
            # fltk.efface("choix")
            c = affiche()
        elif ev == "Up":
            option_id -= 1
            # fltk.efface("choix")
            c = affiche()
    return

def main():
    global plateau, lignes, colonnes, hauteur, largeur
    hauteur, largeur = fltk.hauteur_fenetre(), fltk.largeur_fenetre()
    lignes = globals.lignes
    colonnes = globals.colonnes
    plateau = plateau_vide(lignes, colonnes)
    affichage_map(plateau, lignes, colonnes)
    quadrillage(lignes, colonnes)
    
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
                if plateau[coord_clic[0]][coord_clic[1]] != None:
                    plateau[coord_clic[0], coord_clic[1]] = None
                else:
                    t = options(coord_clic)
                    plateau[coord_clic[0], coord_clic[1]] = t #on met la tuile
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
