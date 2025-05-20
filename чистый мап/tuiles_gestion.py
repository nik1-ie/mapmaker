import fltk
import globals
import solveur
import graphique_utils
import file_reading

def bords_sont_mer_ou_vides(plateau):
    """
    Vérifie si les bords du plateau sont constitués uniquement de cases vides (None) ou de la mer ("SSSS").
    Retourne True si c'est le cas, False sinon.
    """
    lignes = len(plateau)
    colonnes = len(plateau[0])
    for i in range(lignes):
        for j in range(colonnes):
            if i == 0 or i == lignes-1 or j == 0 or j == colonnes-1:
                if plateau[i][j] not in (None, "SSSS"):
                    return False
    return True

def forcer_bords_mer(plateau):
    """
    Force les bords du plateau à être de la mer ("SSSS") en modifiant directement le plateau.
    """
    lignes = len(plateau)
    colonnes = len(plateau[0])
    for i in range(lignes):
        for j in range(colonnes):
            if i == 0 or i == lignes-1 or j == 0 or j == colonnes-1:
                plateau[i][j] = "SSSS"

def dico_to_lst(dico):
    """
    Convertit un dictionnaire de coordonnées (x, y) en une matrice (liste de listes).
    Les coordonnées sont ajustées pour que la matrice commence à l'index (0, 0).
    """
    keys = dico.keys()
    if not keys:
        return [[None for _ in range(globals.colonnes)] for _ in range(globals.lignes)], 0, 0
    min_x = min((key[0] for key in keys), default=0)
    min_y = min((key[1] for key in keys), default=0)
    max_x = max((key[0] for key in keys), default=globals.lignes - 1)
    max_y = max((key[1] for key in keys), default=globals.colonnes - 1)
    lst = [[None for _ in range(min_y, max_y + 1)] for _ in range(min_x, max_x + 1)]
    for (x, y), value in dico.items():
        lst[x - min_x][y - min_y] = value
    return lst, min_x, min_y


def options(pos):
    """
    Affiche une fenêtre d'options pour permettre à l'utilisateur de choisir une tuile à partir d'un ensemble de tuiles disponibles.
    """
    globals.window = True
    
    chemin = file_reading.trouver_chemin_pack()

    if type(chemin) == str and chemin[-1:] not in ('/', '\\'):
        chemin += '/'

    
    plateau_temporaire = [[None for _ in range(globals.colonnes)] for _ in range(globals.lignes)]
    for (i, j), chemin_tuile in globals.cases_remplies.items():
        if 0 <= i < globals.lignes and 0 <= j < globals.colonnes:
            nom_tuile = file_reading.nom_tuile_court(chemin_tuile)
            plateau_temporaire[i][j] = nom_tuile

    
    nom_modele = solveur.recup_nom(plateau_temporaire, pos[0], pos[1])

    

    tuiles_compatibles = [
        tuile for tuile in solveur.rechercher_tuiles(nom_modele, solveur.toutes_tuiles)
        if solveur.emplacement_valide(plateau_temporaire, pos[0], pos[1], tuile)
    ]



    largeur = fltk.largeur_fenetre()
    hauteur = fltk.hauteur_fenetre()
    popup_width = 440
    popup_height = 540
    x1 = (largeur - popup_width) // 2
    y1 = (hauteur - popup_height) // 2
    x2 = x1 + popup_width
    y2 = y1 + popup_height

    NB_COL = 3
    NB_LIG = 3
    NB_PAR_PAGE = NB_COL * NB_LIG
    taille_tuile = 80
    espacement = 18
    grid_width = NB_COL * taille_tuile + (NB_COL - 1) * espacement
    grid_height = NB_LIG * taille_tuile + (NB_LIG - 1) * espacement
    debut_x = x1 + (popup_width - grid_width) // 2
    debut_y = y1 + 120

    
    filtre = ""
    offset = 0
    selection = None

    def filtrer_tuiles():
        if filtre == "":
            base = tuiles_compatibles
        else:
            base = [t for t in tuiles_compatibles if filtre.lower() in t.lower()]
        return base 


    def redessiner():
        fltk.efface_tout()
        fltk.rectangle(0, 0, largeur, hauteur, couleur='', remplissage='#000000')
        graphique_utils.rectangle_arrondi(x1-6, y1-6, popup_width+12, popup_height+12, 22, "#5E4B35", "", 3)
        graphique_utils.rectangle_arrondi(x1-2, y1-2, popup_width+4, popup_height+4, 18, "#B89F81", "", 2)
        graphique_utils.rectangle_arrondi(x1, y1, popup_width, popup_height, 16, "", "#F4E2BD", 0)
        graphique_utils.rectangle_arrondi(x1+20, y1+15, popup_width-40, 60, 10, "#5E4B35", "#E8D5A9", 2)
        fltk.texte((x1 + x2) // 2, y1 + 45, "CHOISIS UNE TUILE", couleur="#5E4B35",
                   police=globals.POLICE_PIXEL, taille=28, ancrage="center")
        graphique_utils.rectangle_arrondi(x1+30, y1+85, popup_width-60, 32, 8, "#5E4B35", "#FFFFFF", 2)
        fltk.texte(x1+40, y1+101, "filtre: " + filtre, couleur="#5E4B35", taille=18, ancrage="w", police=globals.POLICE_PIXEL)
        fltk.rectangle(x2-60, debut_y, x2-30, debut_y+40, remplissage="#E8D5A9", couleur="#5E4B35")
        fltk.texte(x2-45, debut_y+20, "▲", couleur="#5E4B35", taille=22, ancrage="center")
        fltk.rectangle(x2-60, debut_y+grid_height-40, x2-30, debut_y+grid_height, remplissage="#E8D5A9", couleur="#5E4B35")
        fltk.texte(x2-45, debut_y+grid_height-20, "▼", couleur="#5E4B35", taille=22, ancrage="center")
        tuiles_affichees = filtrer_tuiles()
        
        if not tuiles_affichees:
            fltk.texte((x1 + x2) // 2, debut_y + grid_height // 2, "Aucune tuile compatible :((", couleur="#5E4B35", taille=22, ancrage="center", police=globals.POLICE_PIXEL)
        else:
            for idx in range(NB_PAR_PAGE):
                i = offset + idx
                if i >= len(tuiles_affichees):
                    break
                tuile = tuiles_affichees[i]
                lig = idx // NB_COL
                col = idx % NB_COL
                tx = debut_x + col * (taille_tuile + espacement)
                ty = debut_y + lig * (taille_tuile + espacement)
                fltk.rectangle(tx, ty, tx+taille_tuile, ty+taille_tuile, remplissage="#F4E2BD", couleur="#5E4B35", epaisseur=2)
                fltk.image(tx+taille_tuile//2, ty+taille_tuile//2, f"{chemin}{tuile}.png",
                                largeur=taille_tuile-8, hauteur=taille_tuile-8, ancrage="center")
                
                if tuile == selection:
                    fltk.rectangle(tx-3, ty-3, tx+taille_tuile+3, ty+taille_tuile+3, remplissage='', couleur="#FFCC00", epaisseur=4)
        boutons_y = y2 - 80
        boutons_hauteur = 60
        graphique_utils.rectangle_arrondi(x1+20, boutons_y, popup_width-40, boutons_hauteur, 10, "#5E4B35", "#E8D5A9", 2)
        largeur_bouton = 140
        hauteur_bouton = 40
        espace_boutons = 60
        x_valider = x1 + (popup_width // 2) - largeur_bouton - (espace_boutons // 2)
        x_annuler = x1 + (popup_width // 2) + (espace_boutons // 2)
        y_boutons = boutons_y + 10
        
        graphique_utils.rectangle_arrondi(x_valider-2, y_boutons-2, largeur_bouton+4, hauteur_bouton+4, 10, globals.COUL_BOUTON_CONTOUR_FONCE, "", 2)
        graphique_utils.rectangle_arrondi(x_valider, y_boutons, largeur_bouton, hauteur_bouton, 8, globals.COUL_BOUTON_CONTOUR_FONCE, globals.COUL_BOUTON, 2)
        fltk.texte(x_valider + largeur_bouton // 2, y_boutons + hauteur_bouton // 2,
                   "valider", couleur=globals.COUL_BOUTON_TEXTE, police=globals.POLICE_PIXEL, taille=18, ancrage="center")
        graphique_utils.rectangle_arrondi(x_annuler-2, y_boutons-2, largeur_bouton+4, hauteur_bouton+4, 10, globals.COUL_BOUTON_CONTOUR_FONCE, "", 2)
        graphique_utils.rectangle_arrondi(x_annuler, y_boutons, largeur_bouton, hauteur_bouton, 8, globals.COUL_BOUTON_CONTOUR_FONCE, globals.COUL_BOUTON_SURVOL, 2)
        fltk.texte(x_annuler + largeur_bouton // 2, y_boutons + hauteur_bouton // 2,
                   "annuler", couleur=globals.COUL_ENTETE_TEXTE, police=globals.POLICE_PIXEL, taille=18, ancrage="center")
        fltk.mise_a_jour()
        return tuiles_affichees, x_valider, x_annuler, y_boutons, largeur_bouton, hauteur_bouton

    tuiles_affichees, x_valider, x_annuler, y_boutons, largeur_bouton, hauteur_bouton = redessiner()
    derniere_selection = None

    globals.besoin_redessiner = False

    while globals.window:
        ev = fltk.donne_ev()
        if ev:
            t = fltk.type_ev(ev)
            if t == "ClicGauche":
                x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
                if x2-60 <= x <= x2-30 and debut_y <= y <= debut_y+40:
                    if offset - NB_COL >= 0:
                        offset -= NB_COL
                        globals.besoin_redessiner = True
                elif x2-60 <= x <= x2-30 and debut_y+grid_height-40 <= y <= debut_y+grid_height:
                    if offset + NB_PAR_PAGE < len(filtrer_tuiles()):
                        offset += NB_COL
                        globals.besoin_redessiner = True
                elif x1+30 <= x <= x1+30+popup_width-60 and y1+85 <= y <= y1+85+32:
                    pass
                else:
                    found = False
                    for idx in range(NB_PAR_PAGE):
                        i = offset + idx
                        if i >= len(tuiles_affichees):
                            continue
                        lig = idx // NB_COL
                        col = idx % NB_COL
                        tx = debut_x + col * (taille_tuile + espacement)
                        ty = debut_y + lig * (taille_tuile + espacement)
                        if tx <= x <= tx+taille_tuile and ty <= y <= ty+taille_tuile:
                            selection = tuiles_affichees[i]
                            found = True
                            globals.besoin_redessiner = True
                            break
                    if x_valider <= x <= x_valider+largeur_bouton and y_boutons <= y <= y_boutons+hauteur_bouton:
                        if selection:
                            globals.cases_remplies[pos] = selection
                            globals.besoin_redessiner = True
                            globals.window = False
                            return selection
                    if x_annuler <= x <= x_annuler+largeur_bouton and y_boutons <= y <= y_boutons+hauteur_bouton:
                        globals.window = False
                        return None
            elif t == "Touche":
                k = fltk.touche(ev)
                if k in ("BackSpace", "Delete"):
                    if filtre:
                        filtre = filtre[:-1]
                        offset = 0
                        globals.besoin_redessiner = True
                elif k == "Return":
                    if selection:
                        globals.cases_remplies[pos] = selection
                        globals.besoin_redessiner = True
                        globals.window = False
                        return selection
                elif k == "Escape":
                    globals.window = False
                    return None
                elif len(k) == 1 and k in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.,;:!?@#$%^&*()[]{}<>/\\|+=~`\'" ':
                    filtre += k
                    offset = 0
                    globals.besoin_redessiner = True
        if globals.besoin_redessiner:
            tuiles_affichees, x_valider, x_annuler, y_boutons, largeur_bouton, hauteur_bouton = redessiner()
            globals.besoin_redessiner = False
        else:
            fltk.efface("curseur")
        graphique_utils.dessiner_curseur_souris()
        graphique_utils.mise_a_jour_avec_curseur()
        fltk.attente(0.01)
