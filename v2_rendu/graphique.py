import fltk

## Constantes ####################
TAILLE_CASE_BASE = 50
ZOOM_MIN = 0.5
ZOOM_MAX = 3.0
NB_LIGNES = 12
NB_COLONNES = 16

## Variables globales ############
facteur_zoom = 1.0
pan_x, pan_y = 0, 0
cases_remplies = set() 
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
    """Dessine les boutons de zoom et de panoramique"""
    boutons = [
        (750, 550, 770, 570, "+"),
        (775, 550, 795, 570, "-"),
        (660, 550, 680, 570, "←"),
        (680, 550, 700, 570, "→"),
        (700, 550, 720, 570, "↑"),
        (720, 550, 740, 570, "↓"),
    ]

    for x1, y1, x2, y2, texte in boutons:
        fltk.rectangle(x1, y1, x2, y2, remplissage='#E0E0E0', epaisseur=2, couleur='#E0E0E0')
        fltk.texte((x1 + x2)//2, (y1 + y2)//2, texte, ancrage='center', taille=14)

def gerer_clic(x, y):
    """Gère les clics de souris sur la fenêtre"""
    global facteur_zoom, pan_x, pan_y, cases_remplies
    

    if 550 <= y <= 570:
        if 750 <= x <= 770:
            facteur_zoom = min(ZOOM_MAX, facteur_zoom * 1.2)
        if 775 <= x <= 795:
            facteur_zoom = max(ZOOM_MIN, facteur_zoom * 0.8)
        if 660 <= x <= 680:
            pan_x -= 50
        if 680 <= x <= 700:
            pan_x += 50
        if 700 <= x <= 720:
            pan_y -= 50
        if 720 <= x <= 740:
            pan_y += 50
        return True #blyatt, надо тут поменять обратно эту хуйню на все елсы, иначе не будет работать на всей линии этих кнопок      



    taille_case = actualiser_taille_case()
    colonne = (x + pan_x) // taille_case
    ligne = (y + pan_y) // taille_case
    if (ligne, colonne) not in cases_remplies:
        cases_remplies.add((ligne, colonne))  
    return True

def main():
    global pan_x, pan_y
    
    
    while True:
        ev = fltk.donne_ev()
        if ev:
            if fltk.type_ev(ev) == 'ClicGauche':
                x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
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
            elif fltk.type_ev(ev) == 'Quitte':
                break
        
        dessiner_carte()
        fltk.mise_a_jour()
    
    fltk.ferme_fenetre()

if __name__ == "__main__":
    fltk.cree_fenetre(800, 600)
    main()
