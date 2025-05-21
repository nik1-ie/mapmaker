import fltk
import globals

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

def dessiner_curseur_souris(image: str = "ICONS/paw.png", taille: int = 32):
    """
    Dessine un curseur personnalisé à la position actuelle de la souris
    """
    x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
    fltk.image(x, y, image, largeur=taille, hauteur=taille, ancrage="center", tag="curseur")

def mise_a_jour_avec_curseur():
    """Wrapper pour mise_a_jour qui dessine toujours le curseur avant la mise à jour.
    """
    dessiner_curseur_souris()
    fltk.mise_a_jour()

def actualiser_taille_case():
    """
    Calcule et retourne la taille actuelle d'une case en fonction du facteur de zoom.
    """
    return round(globals.TAILLE_CASE_BASE * globals.facteur_zoom)

def dessiner_barre_outils():
    """
    Dessine la barre d'outils en haut de la fenêtre, avec les boutons pour les différentes actions.
    """
    largeur = fltk.largeur_fenetre()
    
    fltk.rectangle(0, 0, largeur, globals.HAUTEUR_BARRE_OUTILS, remplissage=globals.COUL_MENU_CONTOUR_FONCE, couleur=globals.COULEUR_SEPARATEUR)
    fltk.ligne(0, globals.HAUTEUR_BARRE_OUTILS, largeur, globals.HAUTEUR_BARRE_OUTILS, couleur=globals.COULEUR_SEPARATEUR, epaisseur=2)
    milieu = largeur // 2
    fltk.ligne(milieu, 5, milieu, globals.HAUTEUR_BARRE_OUTILS-5, couleur=globals.COULEUR_SEPARATEUR, epaisseur=2)

    outils_gauche = [
        ("ajouter", "Ajouter un tile"),
        ("supprimer", "Supprimer un tile"),
        ("remplacer", "Remplacer un tile"),
        ("remplir", "Remplir une zone"),
        ("selectionner", "Sélectionner un tile"),
        ("annuler", "Annuler"),
        ("refaire", "Refaire")
    ]
    x_debut = 10
    for i, (action, tooltip) in enumerate(outils_gauche):
        x = x_debut + i * (globals.LARGEUR_BOUTON + globals.ESPACEMENT_BOUTONS)
        y = (globals.HAUTEUR_BARRE_OUTILS - globals.HAUTEUR_BOUTON) // 2
        couleur_fond = globals.COULEUR_BOUTON_ACTIF if globals.mode_actuel == action else globals.COULEUR_BOUTON_INACTIF
        rectangle_arrondi(x, y, globals.LARGEUR_BOUTON, globals.HAUTEUR_BOUTON, 8, globals.COULEUR_SEPARATEUR, couleur_fond, 2)
        
        fltk.image(x + globals.LARGEUR_BOUTON//2, y + globals.HAUTEUR_BOUTON//2, globals.ICONS[action], largeur=32, hauteur=32, ancrage='center')

    outils_droite = [
        ("zoom_plus", "Zoom +"),
        ("zoom_moins", "Zoom -"),
        ("grille", "Afficher/Masquer grille"),
        ("centrer", "Centrer carte"),
        ("plein_ecran", "Mode plein écran"),
        ("mini_carte", "Mini-carte"),
        ("capture", "Capture d'écran")
    ]
    x_debut = milieu + 10
    for i, (action, tooltip) in enumerate(outils_droite):
        x = x_debut + i * (globals.LARGEUR_BOUTON + globals.ESPACEMENT_BOUTONS)
        y = (globals.HAUTEUR_BARRE_OUTILS - globals.HAUTEUR_BOUTON) // 2
        etat_special = False
        if action == "grille" and globals.afficher_grille:
            etat_special = True
        elif action == "plein_ecran" and globals.plein_ecran:
            etat_special = True
        elif action == "mini_carte" and globals.mini_carte_active:
            etat_special = True
        couleur_fond = globals.COULEUR_BOUTON_ACTIF if etat_special else globals.COULEUR_BOUTON_INACTIF
        rectangle_arrondi(x, y, globals.LARGEUR_BOUTON, globals.HAUTEUR_BOUTON, 8, globals.COULEUR_SEPARATEUR, couleur_fond, 2)
        fltk.image(x + globals.LARGEUR_BOUTON//2, y + globals.HAUTEUR_BOUTON//2, globals.ICONS[action], largeur=32, hauteur=32, ancrage='center')

def basculer_plein_ecran():
    """
    Bascule entre le mode plein écran et le mode fenêtre pour l'application.
    """
    if globals.plein_ecran:
        fltk.redimensionne_fenetre(*globals.TAILLE_FENETRE_DEFAUT)
    else:
        fltk.redimensionne_fenetre(globals.LARGEUR_ECRAN, globals.HAUTEUR_ECRAN)
    fltk.mise_a_jour()