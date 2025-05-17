import fltk
import globals
import test_solveur
## Constantes ####################
TAILLE_CASE_BASE = 50
ZOOM_MIN = 0.5
ZOOM_MAX = 3.0
globals.lignes = 12
globals.colonnes = 16

## Variables globales ############
facteur_zoom = 1.0
pan_x, pan_y = 0, 0
cases_remplies = {}
window = False
##################################

def actualiser_taille_case():
    """Calcule la taille de chaque case en fonction du facteur de zoom"""
    return round(TAILLE_CASE_BASE * facteur_zoom)

def dessiner_carte():
    """Dessine le quadrillage"""
    global pan_x, pan_y
    fltk.efface_tout()
    taille_case = actualiser_taille_case()
    fltk.rectangle(0, 0, fltk.largeur_fenetre(), fltk.hauteur_fenetre(), remplissage='white')

    largeur = fltk.largeur_fenetre()
    hauteur = fltk.hauteur_fenetre()

    offset_x = pan_x % taille_case
    offset_y = pan_y % taille_case


    for (i, j) in cases_remplies:
        x1 = j * taille_case - pan_x
        y1 = i * taille_case - pan_y
        x2 = x1 + taille_case
        y2 = y1 + taille_case
        if cases_remplies[(i,j)] != None:
            fltk.image(x1+x2 //2, y1+y2//2, cases_remplies[(i,j)])
        else:
            fltk.rectangle(x1, y1, x2, y2, remplissage='#FFC0CF', epaisseur=0)
            

    for i in range(0, hauteur // taille_case + 2):
        y = i * taille_case - offset_y
        fltk.ligne(0, y, largeur, y, couleur='#444444')

    for j in range(0, largeur // taille_case + 2):
        x = j * taille_case - offset_x
        fltk.ligne(x, 0, x, hauteur, couleur='#444444')

    dessiner_boutons()
    fltk.mise_a_jour()

def dessiner_boutons():
    """Dessine les boutons de zoom et de panoramique en haut de l'écran, adaptés à la largeur de la fenêtre"""
    largeur = fltk.largeur_fenetre()

    boutons = [
        ("+", largeur // 2 - 2 * 50, 10 , 40, 20),
        ("-", largeur // 2 - 50, 10 , 40, 20),
        ("←", largeur // 2, 10 , 40, 20),
        ("→", largeur // 2 + 50, 10 , 40, 20),
        ("↑", largeur // 2 + 2 * 50, 10 , 40, 20),
        ("↓", largeur // 2 + 3 * 50, 10 , 40, 20),
    ]

    for texte, x1, y1, x2, y2 in boutons:
        x2 = x1 + 40
        y2 = y1 + 20
        fltk.rectangle(x1, y1, x2, y2, remplissage='#E0E0E0', epaisseur=2, couleur='#E0E0E0')
        fltk.texte((x1 + x2) // 2, (y1 + y2) // 2, texte, ancrage='center', taille=14)

def gerer_clic(x, y):
    """Gère les clics de souris sur la fenêtre"""
    global facteur_zoom, pan_x, pan_y, cases_remplies
    largeur = fltk.largeur_fenetre()

    if 10 <= y <= 30: #Si on clique manuellement sur un des boutons
        if largeur // 2 - 2 * 50 <= x <= largeur // 2 - 2 * 50 +40:
            facteur_zoom = min(ZOOM_MAX, facteur_zoom * 1.2)
        if largeur // 2 - 50 <= x <= largeur // 2 - 50 + 40:
            facteur_zoom = max(ZOOM_MIN, facteur_zoom * 0.8)
        if largeur // 2 <= x <= largeur // 2 + 40:
            pan_x -= 50
        if largeur // 2 + 50 <= x <= largeur // 2 + 90:
            pan_x += 50
        if largeur // 2 + 2 * 50 <= x <= largeur // 2 + 2 * 50 + 40:
            pan_y -= 50
        if largeur // 2 + 3 * 50 <= x <= largeur // 2 + 3 * 50 + 40:
            pan_y += 50
        return True #blyatt, надо тут поменять обратно эту хуйню на все елсы, иначе не будет работать на всей линии этих кнопок      



    taille_case = actualiser_taille_case()
    colonne = (x + pan_x) // taille_case
    ligne = (y + pan_y) // taille_case
    if (ligne, colonne) not in cases_remplies:
        cases_remplies[ligne, colonne] = None
        # cases_remplies.add((ligne, colonne))
        options((ligne, colonne))
    return True

def dico_to_lst(dico):
    '''
    Fonctions transformant notre dictionnaire en liste afin d'utiliser les fonctions d'analyses.
    Arguments : dico (dico) - dictionnaire de positions.
    Return : lst (liste) - liste de taille nécessaire, pleine de None ou de tuiles.
    '''
    keys = dico.keys()
    max_x = max((key[0] for key in keys))
    max_y = max((key[1] for key in keys))
    lst = [[None for _ in range(max_y + 1)] for _ in range(max_x + 1)]
    for (x, y), value in dico.items():
        lst[x][y] = value
    return lst

def options(pos):
    '''
    Affiche une fenêtre de choix de tuiles selon la position à laquelle on se trouve.
    '''
    print("IN the window function ???")
    global window
    chemin = globals.pack1_way
    window = True
    
    yess = dico_to_lst(cases_remplies)
    print(f'Nv plateau ??{yess} end of new plateau.')
    nom = test_solveur.recup_nom(yess, pos[0], pos[1])
    option = test_solveur.rechercher_tuiles(nom)
    print(f' Options ! {option} end options.')
    largeur = fltk.largeur_fenetre()
    hauteur = fltk.hauteur_fenetre()
    popup_width = 400
    popup_height = 300
    x1 = (largeur - popup_width) // 2
    y1 = (hauteur - popup_height) // 2
    x2 = x1 + popup_width
    y2 = y1 + popup_height

    fltk.rectangle(x1, y1, x2, y2, remplissage='#FFFFFF', epaisseur=2, couleur='#000000')
    fltk.texte((x1 + x2) // 2, y1 + 20, "Tuiles possibles", ancrage='center', taille=16, couleur='#000000')
    for tuile in option:
        print('eh ?')
        tuile_width = 5
        tuile_height = 5
        margin = 10
        cols = (popup_width - 2 * margin) // (tuile_width + margin)
        for idx, tuile in enumerate(option):
            row = idx // cols
            col = idx % cols
            x_tuile = x1 + margin + col * (tuile_width + margin)
            y_tuile = y1 + 40 + row * (tuile_height + margin)
            fltk.image(x_tuile + tuile_width // 2, y_tuile + tuile_height // 2, f"{chemin}{tuile}.png")
            
    while True:
        ev = fltk.attend_clic_gauche()

    #     x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
    #     print("yay clic")

    return

def main():
    global pan_x, pan_y
    
    
    while True:
        ev = fltk.donne_ev()
        if ev:
            if fltk.type_ev(ev) == 'ClicGauche':
                x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
                if window == True:
                    print("In thee window !!")
                else:
                    gerer_clic(x, y)
            elif fltk.type_ev(ev) == 'Touche':
                touche = fltk.touche(ev)
                if touche == 'Left':
                    pan_x -= 50
                elif touche == 'Right':
                    pan_x += 50
                elif touche == 'Up':
                    pan_y -= 50
                elif touche == 'Down':
                    pan_y += 50
                elif touche == 'Escape':
                    fltk.efface_tout()
                    fltk.redimensionne_fenetre(800, 800)
                    import menu
                    menu.menu()
                    break
            elif fltk.type_ev(ev) == 'Quitte':
                break
        
        dessiner_carte()
        fltk.mise_a_jour()
    
    fltk.ferme_fenetre()

if __name__ == "__main__":
    fltk.cree_fenetre(800, 600)
    plateau = [['SSSS','SSSS','SSSS','SSSS', None],
            ['SSSS','SHGS', 'SHRH', 'SHFH', None],
            ['SSSS', None, 'RMPP', 'FMMM', 'PPMM'],
            ['SSSS', None, None, None, None],
            [None, None, None, None, None]]
    main()
    
'''
    boutons = [
        (750, 550, 770, 570, "+"),
        (775, 550, 795, 570, "-"),
        (660, 550, 680, 570, "←"),
        (680, 550, 700, 570, "→"),
        (700, 550, 720, 570, "↑"),
        (720, 550, 740, 570, "↓"),
    ]
'''