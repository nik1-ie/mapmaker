import fltk
import globals
import solveur
import os
import random
from utilitaires import dessiner_curseur_souris, mise_a_jour_avec_curseur, rectangle_arrondi, initialiser_gouttes, bouton_clique
from PIL import Image




TAILLE_CASE_BASE = 50
ZOOM_MIN = 0.5
ZOOM_MAX = 3.0

facteur_zoom = 1.0
pan_x, pan_y = 0, 0
cases_remplies = {}
window = False
afficher_grille = True
mode_actuel = "ajouter"
historique_actions = []
position_historique = -1
plein_ecran = False
mini_carte_active = False

COULEUR_BARRE_OUTILS = "#F4E2BD"
COULEUR_BOUTON_INACTIF = "#E8D5A9"
COULEUR_BOUTON_ACTIF = "#B89F81"
COULEUR_TEXTE_BOUTON = "#5E4B35"
COULEUR_SEPARATEUR = "#B89F81"

HAUTEUR_BARRE_OUTILS = 60
LARGEUR_BOUTON = 50
HAUTEUR_BOUTON = 50
ESPACEMENT_BOUTONS = 5
TAILLE_ICONE = 24

ICONS = {
    "ajouter": "./icons/add.png",
    "supprimer": "./icons/subtract.png",
    "remplacer": "./icons/love.png",
    "remplir": "./icons/camera.png",
    "selectionner": "./icons/maximize (1).png",
    "annuler": "./icons/previous.png",
    "refaire": "./icons/next-icon.png",
    "zoom_plus": "./icons/zoom-in.png",
    "zoom_moins": "./icons/zoom-out.png",
    "grille": "./icons/computer.png",
    "centrer": "./icons/minimize.png",
    "plein_ecran": "./icons/maximize.png",
    "mini_carte": "./icons/search.png",
    "capture": "./icons/photo-size.png",
}

LARGEUR_ECRAN = 1920
HAUTEUR_ECRAN = 1080
TAILLE_FENETRE_DEFAUT = (800, 600)




def extraire_nom_tuile(chemin_tuile):
    """
    Extrait le nom de base (4 premiers caractères) d'une tuile à partir de son chemin de fichier.
    Retourne None si le chemin n'est pas valide ou ne correspond pas à une image PNG.
    """
    if not chemin_tuile or not isinstance(chemin_tuile, str):
        return None
    nom_fichier = os.path.basename(chemin_tuile)
    if nom_fichier.endswith('.png'):
        nom_base = nom_fichier[:-4]
        
        if len(nom_base) >= 4:
            return nom_base[:4]
    return None

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

def basculer_plein_ecran():
    """
    Bascule entre le mode plein écran et le mode fenêtre pour l'application.
    """
    global plein_ecran
    if plein_ecran:
        fltk.redimensionne_fenetre(*TAILLE_FENETRE_DEFAUT)
    else:
        fltk.redimensionne_fenetre(LARGEUR_ECRAN, HAUTEUR_ECRAN)
    fltk.mise_a_jour()

def actualiser_taille_case():
    """
    Calcule et retourne la taille actuelle d'une case en fonction du facteur de zoom.
    """
    return round(TAILLE_CASE_BASE * facteur_zoom)

def dessiner_barre_outils():
    """
    Dessine la barre d'outils en haut de la fenêtre, avec les boutons pour les différentes actions.
    """
    largeur = fltk.largeur_fenetre()
    
    fltk.rectangle(0, 0, largeur, HAUTEUR_BARRE_OUTILS, remplissage=globals.COUL_MENU_CONTOUR_FONCE, couleur=COULEUR_SEPARATEUR)
    fltk.ligne(0, HAUTEUR_BARRE_OUTILS, largeur, HAUTEUR_BARRE_OUTILS, couleur=COULEUR_SEPARATEUR, epaisseur=2)
    milieu = largeur // 2
    fltk.ligne(milieu, 5, milieu, HAUTEUR_BARRE_OUTILS-5, couleur=COULEUR_SEPARATEUR, epaisseur=2)

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
        x = x_debut + i * (LARGEUR_BOUTON + ESPACEMENT_BOUTONS)
        y = (HAUTEUR_BARRE_OUTILS - HAUTEUR_BOUTON) // 2
        couleur_fond = COULEUR_BOUTON_ACTIF if mode_actuel == action else COULEUR_BOUTON_INACTIF
        rectangle_arrondi(x, y, LARGEUR_BOUTON, HAUTEUR_BOUTON, 8, COULEUR_SEPARATEUR, couleur_fond, 2)
        
        fltk.image(x + LARGEUR_BOUTON//2, y + HAUTEUR_BOUTON//2, ICONS[action], largeur=32, hauteur=32, ancrage='center')

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
        x = x_debut + i * (LARGEUR_BOUTON + ESPACEMENT_BOUTONS)
        y = (HAUTEUR_BARRE_OUTILS - HAUTEUR_BOUTON) // 2
        etat_special = False
        if action == "grille" and afficher_grille:
            etat_special = True
        elif action == "plein_ecran" and plein_ecran:
            etat_special = True
        elif action == "mini_carte" and mini_carte_active:
            etat_special = True
        couleur_fond = COULEUR_BOUTON_ACTIF if etat_special else COULEUR_BOUTON_INACTIF
        rectangle_arrondi(x, y, LARGEUR_BOUTON, HAUTEUR_BOUTON, 8, COULEUR_SEPARATEUR, couleur_fond, 2)
        fltk.image(x + LARGEUR_BOUTON//2, y + HAUTEUR_BOUTON//2, ICONS[action], largeur=32, hauteur=32, ancrage='center')

def gerer_clic_barre_outils(x, y):
    """
    Gère les clics de souris sur la barre d'outils, en changeant le mode d'action ou en effectuant des actions spéciales
    comme le zoom, l'annulation, la restauration, etc.
    """
    global mode_actuel, facteur_zoom, pan_x, pan_y, afficher_grille, plein_ecran, mini_carte_active

    if y > HAUTEUR_BARRE_OUTILS:
        return False

    largeur = fltk.largeur_fenetre()
    milieu = largeur // 2

    outils_gauche = [
        "ajouter", "supprimer", "remplacer", "remplir", "selectionner", "annuler", "refaire"
    ]

    x_debut = 10
    for i, action in enumerate(outils_gauche):
        x_bouton = x_debut + i * (LARGEUR_BOUTON + ESPACEMENT_BOUTONS)
        y_bouton = (HAUTEUR_BARRE_OUTILS - HAUTEUR_BOUTON) // 2

        if (x_bouton <= x <= x_bouton + LARGEUR_BOUTON and 
            y_bouton <= y <= y_bouton + HAUTEUR_BOUTON):
            if action in ["ajouter", "supprimer", "remplacer", "remplir", "selectionner"]:
                mode_actuel = action
            elif action == "annuler":
                annuler()
            elif action == "refaire":
                refaire()
            return True

    outils_droite = [
        "zoom_plus", "zoom_moins", "grille", "centrer", "plein_ecran", "mini_carte", "capture"
    ]
    
    x_debut = milieu + 10
    for i, action in enumerate(outils_droite):
        x_bouton = x_debut + i * (LARGEUR_BOUTON + ESPACEMENT_BOUTONS)
        y_bouton = (HAUTEUR_BARRE_OUTILS - HAUTEUR_BOUTON) // 2
        
        if (x_bouton <= x <= x_bouton + LARGEUR_BOUTON and 
            y_bouton <= y <= y_bouton + HAUTEUR_BOUTON):
            if action == "zoom_plus":
                facteur_zoom = min(ZOOM_MAX, facteur_zoom * 1.2)
            elif action == "zoom_moins":
                facteur_zoom = max(ZOOM_MIN, facteur_zoom * 0.8)
            elif action == "grille":
                afficher_grille = not afficher_grille
            elif action == "centrer":
                pan_x, pan_y = 0, 0
            elif action == "plein_ecran":
                plein_ecran = not plein_ecran
                basculer_plein_ecran()
            elif action == "mini_carte":
                mini_carte_active = not mini_carte_active
                
            elif action == "capture":
                capture_ecran()
            return True
    
    return False

def dessiner_carte(plateau, lignes, colonnes, pan_x, pan_y, facteur_zoom):
    """
    Dessine la carte en fonction du plateau, des dimensions, du décalage et du facteur de zoom.
    """
    taille_case = round(TAILLE_CASE_BASE * facteur_zoom)
    largeur = fltk.largeur_fenetre()
    hauteur = fltk.hauteur_fenetre()
    
    fltk.rectangle(0, 0, largeur, hauteur, remplissage='white')
    
    for i in range(lignes):
        for j in range(colonnes):
            x1 = j * taille_case - pan_x
            y1 = i * taille_case - pan_y + HAUTEUR_BARRE_OUTILS
            x2 = x1 + taille_case
            y2 = y1 + taille_case

            if plateau[i][j] is not None:
                chemin_image = plateau[i][j]
                fltk.image(x1 + taille_case // 2, y1 + taille_case // 2, 
                          chemin_image, largeur=taille_case, hauteur=taille_case, 
                          ancrage='center')
            else:
                
                fltk.rectangle(x1, y1, x2, y2, remplissage='#F4E2BD', epaisseur=0)

    if afficher_grille:
        for i in range(lignes + 1):
            y = i * taille_case - pan_y + HAUTEUR_BARRE_OUTILS
            fltk.ligne(0, y, largeur, y, couleur='#444444')
        
        for j in range(colonnes + 1):
            x = j * taille_case - pan_x
            fltk.ligne(x, HAUTEUR_BARRE_OUTILS, x, hauteur, couleur='#444444')
    
    dessiner_barre_outils()
    
    if mini_carte_active:
        dessiner_mini_carte(plateau, lignes, colonnes)
    
    mise_a_jour_avec_curseur()

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
    
    rectangle_arrondi(x_mini, y_mini, mini_largeur, mini_hauteur, 5, "#444444", "#FFFFFF", 2)
    
    echelle_x = (mini_largeur - 10) / (colonnes * TAILLE_CASE_BASE)
    echelle_y = (mini_hauteur - 10) / (lignes * TAILLE_CASE_BASE)
    echelle = min(echelle_x, echelle_y)
    
    for i in range(lignes):
        for j in range(colonnes):
            mini_x = x_mini + 5 + j * TAILLE_CASE_BASE * echelle
            mini_y = y_mini + 5 + i * TAILLE_CASE_BASE * echelle
            mini_taille = TAILLE_CASE_BASE * echelle

            couleur = '#F4E2BD'
            if plateau[i][j] is not None:
                couleur = '#8899FF'
            
            fltk.rectangle(mini_x, mini_y, mini_x + mini_taille, mini_y + mini_taille, 
                          remplissage=couleur, epaisseur=0)

def options(pos):
    """
    Affiche une fenêtre d'options pour permettre à l'utilisateur de choisir une tuile à partir d'un ensemble de tuiles disponibles.
    """
    import string

    global window, cases_remplies
    window = True

    
    if isinstance(globals.pack_1, dict):
        chemin = "./pack1/tuiles/"
        if not os.path.exists(chemin):
            alternatives = ["./pack1/", "./tuiles/", ".", "./assets/"]
            for alt in alternatives:
                if os.path.exists(alt):
                    chemin = alt
                    break
    else:
        chemin = globals.pack_1

    
    if isinstance(chemin, str) and not (chemin.endswith('/') or chemin.endswith('\\')):
        chemin += '/'

    
    plateau_temporaire = [[None for _ in range(globals.colonnes)] for _ in range(globals.lignes)]
    for (i, j), chemin_tuile in cases_remplies.items():
        if 0 <= i < globals.lignes and 0 <= j < globals.colonnes:
            nom_tuile = extraire_nom_tuile(chemin_tuile)
            plateau_temporaire[i][j] = nom_tuile

    
    nom_modele = solveur.recup_nom(plateau_temporaire, pos[0], pos[1])

    
    tuiles_recommandees = solveur.rechercher_tuiles(nom_modele, solveur.toutes_tuiles)

    try:
        dossier_tuiles = os.path.dirname(chemin) if chemin else "."
        if dossier_tuiles == "":
            dossier_tuiles = "."
        tuiles_disponibles = [fichier[:-4] for fichier in os.listdir(dossier_tuiles) if fichier.endswith(".png")]
    except Exception:
        tuiles_disponibles = []

    if not tuiles_recommandees and not tuiles_disponibles:
        toutes_tuiles = ["herbe", "eau", "pierre", "terre", "sable", "chemin", "foret", "montagne", "neige"]
    else:
        toutes_tuiles = sorted(list(set(tuiles_recommandees + tuiles_disponibles)))

    
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
        
        if not filtre.strip():
            base = toutes_tuiles
        else:
            base = [t for t in toutes_tuiles if filtre.lower() in t.lower()]
        
        recos = [t for t in tuiles_recommandees if t in base]
        autres = [t for t in base if t not in recos]
        
        return recos + autres

    def redessiner():
        fltk.efface_tout()
        fltk.rectangle(0, 0, largeur, hauteur, couleur='', remplissage='#000000')
        rectangle_arrondi(x1-6, y1-6, popup_width+12, popup_height+12, 22, "#5E4B35", "", 3)
        rectangle_arrondi(x1-2, y1-2, popup_width+4, popup_height+4, 18, "#B89F81", "", 2)
        rectangle_arrondi(x1, y1, popup_width, popup_height, 16, "", "#F4E2BD", 0)
        rectangle_arrondi(x1+20, y1+15, popup_width-40, 60, 10, "#5E4B35", "#E8D5A9", 2)
        fltk.texte((x1 + x2) // 2, y1 + 45, "CHOISIS UNE TUILE", couleur="#5E4B35",
                   police=globals.POLICE_PIXEL, taille=28, ancrage="center")
        rectangle_arrondi(x1+30, y1+85, popup_width-60, 32, 8, "#5E4B35", "#FFFFFF", 2)
        fltk.texte(x1+40, y1+101, "filtre: " + filtre, couleur="#5E4B35", taille=18, ancrage="w", police=globals.POLICE_PIXEL)
        fltk.rectangle(x2-60, debut_y, x2-30, debut_y+40, remplissage="#E8D5A9", couleur="#5E4B35")
        fltk.texte(x2-45, debut_y+20, "▲", couleur="#5E4B35", taille=22, ancrage="center")
        fltk.rectangle(x2-60, debut_y+grid_height-40, x2-30, debut_y+grid_height, remplissage="#E8D5A9", couleur="#5E4B35")
        fltk.texte(x2-45, debut_y+grid_height-20, "▼", couleur="#5E4B35", taille=22, ancrage="center")
        tuiles_affichees = filtrer_tuiles()
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
            try:
                fltk.image(tx+taille_tuile//2, ty+taille_tuile//2, f"{chemin}{tuile}.png",
                           largeur=taille_tuile-8, hauteur=taille_tuile-8, ancrage="center")
            except Exception:
                fltk.texte(tx+taille_tuile//2, ty+taille_tuile//2, "?", couleur="#5E4B35", taille=24, ancrage="center")
            if tuile == selection:
                fltk.rectangle(tx-3, ty-3, tx+taille_tuile+3, ty+taille_tuile+3, remplissage='', couleur="#FFCC00", epaisseur=4)
        boutons_y = y2 - 80
        boutons_hauteur = 60
        rectangle_arrondi(x1+20, boutons_y, popup_width-40, boutons_hauteur, 10, "#5E4B35", "#E8D5A9", 2)
        largeur_bouton = 140
        hauteur_bouton = 40
        espace_boutons = 60
        x_valider = x1 + (popup_width // 2) - largeur_bouton - (espace_boutons // 2)
        x_annuler = x1 + (popup_width // 2) + (espace_boutons // 2)
        y_boutons = boutons_y + 10
        
        rectangle_arrondi(x_valider-2, y_boutons-2, largeur_bouton+4, hauteur_bouton+4, 10, globals.COUL_BOUTON_CONTOUR_FONCE, "", 2)
        rectangle_arrondi(x_valider, y_boutons, largeur_bouton, hauteur_bouton, 8, globals.COUL_BOUTON_CONTOUR_FONCE, globals.COUL_BOUTON, 2)
        fltk.texte(x_valider + largeur_bouton // 2, y_boutons + hauteur_bouton // 2,
                   "valider", couleur=globals.COUL_BOUTON_TEXTE, police=globals.POLICE_PIXEL, taille=18, ancrage="center")
        rectangle_arrondi(x_annuler-2, y_boutons-2, largeur_bouton+4, hauteur_bouton+4, 10, globals.COUL_BOUTON_CONTOUR_FONCE, "", 2)
        rectangle_arrondi(x_annuler, y_boutons, largeur_bouton, hauteur_bouton, 8, globals.COUL_BOUTON_CONTOUR_FONCE, globals.COUL_BOUTON_SURVOL, 2)
        fltk.texte(x_annuler + largeur_bouton // 2, y_boutons + hauteur_bouton // 2,
                   "annuler", couleur=globals.COUL_ENTETE_TEXTE, police=globals.POLICE_PIXEL, taille=18, ancrage="center")
        fltk.mise_a_jour()
        return tuiles_affichees, x_valider, x_annuler, y_boutons, largeur_bouton, hauteur_bouton

    tuiles_affichees, x_valider, x_annuler, y_boutons, largeur_bouton, hauteur_bouton = redessiner()
    derniere_selection = None

    besoin_redessiner = False

    while window:
        ev = fltk.donne_ev()
        if ev:
            t = fltk.type_ev(ev)
            if t == "ClicGauche":
                x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
                if x2-60 <= x <= x2-30 and debut_y <= y <= debut_y+40:
                    if offset - NB_COL >= 0:
                        offset -= NB_COL
                        besoin_redessiner = True
                elif x2-60 <= x <= x2-30 and debut_y+grid_height-40 <= y <= debut_y+grid_height:
                    if offset + NB_PAR_PAGE < len(filtrer_tuiles()):
                        offset += NB_COL
                        besoin_redessiner = True
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
                            besoin_redessiner = True
                            break
                    if x_valider <= x <= x_valider+largeur_bouton and y_boutons <= y <= y_boutons+hauteur_bouton:
                        if selection:
                            cases_remplies[pos] = f"{chemin}{selection}.png"
                            window = False
                            return f"{chemin}{selection}.png"
                    if x_annuler <= x <= x_annuler+largeur_bouton and y_boutons <= y <= y_boutons+hauteur_bouton:
                        window = False
                        return None
            elif t == "Touche":
                k = fltk.touche(ev)
                if k in ("BackSpace", "Delete"):
                    if filtre:
                        filtre = filtre[:-1]
                        offset = 0
                        besoin_redessiner = True
                elif k == "Return":
                    if selection:
                        cases_remplies[pos] = f"{chemin}{selection}.png"
                        window = False
                        return f"{chemin}{selection}.png"
                elif k == "Escape":
                    window = False
                    return None
                elif len(k) == 1 and k in string.printable:
                    filtre += k
                    offset = 0
                    besoin_redessiner = True
        if besoin_redessiner:
            tuiles_affichees, x_valider, x_annuler, y_boutons, largeur_bouton, hauteur_bouton = redessiner()
            besoin_redessiner = False
        else:
            fltk.efface("curseur")
        dessiner_curseur_souris()
        mise_a_jour_avec_curseur()
        fltk.attente(0.01)


def dico_to_lst(dico):
    """
    Convertit un dictionnaire de cases remplies en une liste de listes (matrice) pour faciliter le dessin de la carte.
    """
    keys = dico.keys()
    if not keys:
        return [[None for _ in range(globals.colonnes)] for _ in range(globals.lignes)]
    
    max_x = max((key[0] for key in keys), default=globals.lignes - 1)
    max_y = max((key[1] for key in keys), default=globals.colonnes - 1)
    max_x = max(max_x, globals.lignes - 1)
    max_y = max(max_y, globals.colonnes - 1)
    
    lst = [[None for _ in range(max_y + 1)] for _ in range(max_x + 1)]
    for (x, y), value in dico.items():
        lst[x][y] = value
    
    return lst

def ajouter_action(action, donnees_avant, donnees_apres):
    """
    Ajoute une action à l'historique des actions, pour permettre l'annulation et la restauration.
    """
    global historique_actions, position_historique

    if position_historique < len(historique_actions) - 1:
        historique_actions = historique_actions[:position_historique + 1]

    historique_actions.append({
        'action': action,
        'avant': donnees_avant,
        'apres': donnees_apres
    })
    position_historique = len(historique_actions) - 1

def annuler():
    """
    Annule la dernière action effectuée, en restaurant l'état précédent des cases remplies.
    """
    global historique_actions, position_historique, cases_remplies
    
    if position_historique >= 0:
        action = historique_actions[position_historique]
        
        if action['action'] == 'ajouter':
            
            pos = action['avant']['position']
            if pos in cases_remplies:
                del cases_remplies[pos]
                
        elif action['action'] == 'supprimer':
            
            pos = action['avant']['position']
            tuile = action['avant']['tuile']
            cases_remplies[pos] = tuile
            
        elif action['action'] == 'remplacer':
            
            pos = action['avant']['position']
            tuile = action['avant']['tuile']
            cases_remplies[pos] = tuile
            
        elif action['action'] == 'remplir':
            
            if 'cases' in action['avant']:
                
                for pos, tuile in action['avant']['cases'].items():
                    if tuile is None and pos in cases_remplies:
                        del cases_remplies[pos]
                    else:
                        cases_remplies[pos] = tuile
            else:
                
                for pos, tuile in action['avant'].items():
                    if tuile is None and pos in cases_remplies:
                        del cases_remplies[pos]
                    else:
                        cases_remplies[pos] = tuile
                    
        position_historique -= 1
        return True
    return False


def refaire():
    """
    Restaure la dernière action annulée, en appliquant à nouveau les changements aux cases remplies.
    """
    global historique_actions, position_historique, cases_remplies
    
    if position_historique < len(historique_actions) - 1:
        position_historique += 1
        action = historique_actions[position_historique]
        
        if action['action'] == 'ajouter':
            pos = action['apres']['position']
            tuile = action['apres']['tuile']
            cases_remplies[pos] = tuile
            
        elif action['action'] == 'supprimer':
            pos = action['apres']['position']
            if pos in cases_remplies:
                del cases_remplies[pos]
                
        elif action['action'] == 'remplacer':
            pos = action['apres']['position']
            tuile = action['apres']['tuile']
            cases_remplies[pos] = tuile
            
        elif action['action'] == 'remplir':
            
            if 'cases' in action['apres']:
                for pos, tuile in action['apres']['cases'].items():
                    if tuile is None and pos in cases_remplies:
                        del cases_remplies[pos]
                    else:
                        cases_remplies[pos] = tuile
            else:
                for pos, tuile in action['apres'].items():
                    if tuile is None and pos in cases_remplies:
                        del cases_remplies[pos]
                    else:
                        cases_remplies[pos] = tuile
                        
        return True
    return False


def capture_ecran():
    """
    Capture l'écran et sauvegarde l'image de la carte actuelle dans le dossier 'captures'.
    """
    lignes = globals.lignes
    colonnes = globals.colonnes
    taille_case = TAILLE_CASE_BASE

    dossier = "captures"


    img = Image.new("RGBA", (colonnes * taille_case, lignes * taille_case), (244, 226, 189, 255))

    for (i, j), chemin in cases_remplies.items():
        try:
            tuile = Image.open(chemin).convert("RGBA")
            tuile = tuile.resize((taille_case, taille_case), Image.NEAREST)
            img.paste(tuile, (j * taille_case, i * taille_case), mask=tuile)
        except Exception as e:
            print(f"Erreur chargement tuile {chemin} : {e}")

    import time
    nom_fichier = os.path.join(dossier, f"carte_{time.strftime('%Y%m%d_%H%M%S')}.png")
    img.save(nom_fichier)
    print(f"Carte sauvegardée sous : {nom_fichier}")
    return True

def afficher_galerie_captures():
    """
    Affiche une galerie des captures d'écran précédemment enregistrées, permettant de naviguer entre elles.
    """
    import glob
    dossier = "captures"
    fichiers = sorted(glob.glob(os.path.join(dossier, "carte_*.png")), reverse=True)
    if not fichiers:
        fltk.efface_tout()
        fltk.texte(fltk.largeur_fenetre()//2, fltk.hauteur_fenetre()//2, "Aucune capture trouvée", couleur="#5E4B35", taille=24, ancrage="center")
        fltk.mise_a_jour()
        fltk.attente(1.5)
        return

    idx = 0
    while True:
        fltk.efface_tout()
        fltk.rectangle(0, 0, fltk.largeur_fenetre(), fltk.hauteur_fenetre(), remplissage="#F4E2BD")
        fltk.texte(fltk.largeur_fenetre()//2, 30, f"Capture {idx+1}/{len(fichiers)} : {os.path.basename(fichiers[idx])}", couleur="#5E4B35", taille=18, ancrage="center")
        try:
            fltk.image(fltk.largeur_fenetre()//2, fltk.hauteur_fenetre()//2, fichiers[idx],
                       largeur=fltk.largeur_fenetre()-80, hauteur=fltk.hauteur_fenetre()-100, ancrage="center")
        except Exception:
            fltk.texte(fltk.largeur_fenetre()//2, fltk.hauteur_fenetre()//2, "Erreur d'affichage", couleur="red", taille=20, ancrage="center")
        fltk.texte(60, fltk.hauteur_fenetre()//2, "<", couleur="#5E4B35", taille=40, ancrage="center")
        fltk.texte(fltk.largeur_fenetre()-60, fltk.hauteur_fenetre()//2, ">", couleur="#5E4B35", taille=40, ancrage="center")
        fltk.texte(fltk.largeur_fenetre()//2, fltk.hauteur_fenetre()-30, "Echap pour quitter", couleur="#5E4B35", taille=14, ancrage="center")
        fltk.mise_a_jour()
        ev = fltk.donne_ev()
        if ev:
            t = fltk.type_ev(ev)
            if t == "ClicGauche":
                x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
                if x < 120:
                    idx = (idx - 1) % len(fichiers)
                elif x > fltk.largeur_fenetre() - 120:
                    idx = (idx + 1) % len(fichiers)
            elif t == "Touche":
                k = fltk.touche(ev)
                if k in ("Left", "a"):
                    idx = (idx - 1) % len(fichiers)
                elif k in ("Right", "d"):
                    idx = (idx + 1) % len(fichiers)
                elif k in ("Escape",):
                    break
            elif t == "Quitte":
                break
        fltk.attente(0.01)

selection_rectangle = None
debut_selection = None

def gerer_clic(x, y):
    """
    Gère les clics de souris sur la grille de la carte, en fonction du mode actuel (ajouter, supprimer, sélectionner, remplacer, remplir).
    """
    global facteur_zoom, pan_x, pan_y, window, mode_actuel
    global selection_debut, selection_fin, selection_en_cours, cases_remplies, tuile_selectionnee

    if gerer_clic_barre_outils(x, y):
        return True

    y_ajuste = y - HAUTEUR_BARRE_OUTILS

    taille_case = actualiser_taille_case()
    colonne = (x + pan_x) // taille_case
    ligne = (y_ajuste + pan_y) // taille_case

    if 0 <= ligne < globals.lignes and 0 <= colonne < globals.colonnes:
        pos = (ligne, colonne)
        if mode_actuel == "ajouter":
            avant = cases_remplies.get(pos, None)
            nouvelle_tuile = options(pos)
            if nouvelle_tuile:
                ajouter_action('ajouter',
                    {'position': pos, 'tuile': avant},
                    {'position': pos, 'tuile': nouvelle_tuile}
                )
        elif mode_actuel == "supprimer":
            if pos in cases_remplies:
                avant = cases_remplies[pos]
                ajouter_action('supprimer',
                    {'position': pos, 'tuile': avant},
                    {'position': pos, 'tuile': None}
                )
                del cases_remplies[pos]
        elif mode_actuel == "selectionner":
            if isinstance(globals.pack_1, dict):
                chemin = "./pack1/tuiles/"
                if not os.path.exists(chemin):
                    alternatives = ["./pack1/", "./tuiles/", ".", "./assets/"]
                    for alt in alternatives:
                        if os.path.exists(alt):
                            chemin = alt
                            break
            else:
                chemin = globals.pack_1

            if isinstance(chemin, str) and not (chemin.endswith('/') or chemin.endswith('\\')):
                chemin += '/'

            plateau = [[None for _ in range(globals.colonnes)] for _ in range(globals.lignes)]
            for (i, j), chemin_tuile in cases_remplies.items():
                if 0 <= i < globals.lignes and 0 <= j < globals.colonnes:
                    nom_tuile = extraire_nom_tuile(chemin_tuile)
                    plateau[i][j] = nom_tuile

            if not bords_sont_mer_ou_vides(plateau):
                print("Erreur : Les bords doivent être vides ou déjà de la mer (SSSS) pour générer une île!")
                forcer_bords_mer(plateau)
                print("Correction automatique : les bords sont maintenant de la mer.")
                return

            etat_avant = {}
            for (i, j), tuile in cases_remplies.items():
                etat_avant[(i, j)] = tuile

          
            if solveur.completer_carte(plateau, "ile"):
                etat_apres = {}
                for i in range(globals.lignes):
                    for j in range(globals.colonnes):
                        if plateau[i][j] is not None:
                            chemin_tuile = f"{chemin}{plateau[i][j]}.png"
                            cases_remplies[(i, j)] = chemin_tuile
                            etat_apres[(i, j)] = chemin_tuile
                ajouter_action('remplir', etat_avant, etat_apres)
            else:
                print("Impossible de compléter la carte avec les tuiles actuelles.")


        elif mode_actuel == "remplacer":
            avant = cases_remplies.get(pos, None)
            nouvelle_tuile = options(pos)
            if nouvelle_tuile:
                ajouter_action('remplacer',
                    {'position': pos, 'tuile': avant},
                    {'position': pos, 'tuile': nouvelle_tuile}
                )
        elif mode_actuel == "remplir":
            if not selection_en_cours:
                selection_debut = (ligne, colonne)
                selection_en_cours = True
            else:
                selection_fin = (ligne, colonne)
                remplir_zone_selection()
                selection_debut = None
                selection_fin = None
                selection_en_cours = False
        return True
    return False

def dessiner_selection():
    """
    Dessine un rectangle de sélection sur la carte pour indiquer la zone qui sera affectée par les actions de remplissage.
    """
    if not selection_en_cours or not selection_debut:
        return

    x, y = fltk.abscisse_souris(), fltk.ordonnee_souris() - HAUTEUR_BARRE_OUTILS
    taille_case = actualiser_taille_case()
    col_fin = (x + pan_x) // taille_case
    lig_fin = (y + pan_y) // taille_case

    col_fin = max(0, min(col_fin, globals.colonnes - 1))
    lig_fin = max(0, min(lig_fin, globals.lignes - 1))

    l1, c1 = selection_debut
    l2, c2 = lig_fin, col_fin

    l_min, l_max = min(l1, l2), max(l1, l2)
    c_min, c_max = min(c1, c2), max(c1, c2)

    for i in range(l_min, l_max + 1):
        for j in range(c_min, c_max + 1):
            x1 = j * taille_case - pan_x
            y1 = i * taille_case - pan_y + HAUTEUR_BARRE_OUTILS
            x2 = x1 + taille_case
            y2 = y1 + taille_case
            fltk.rectangle(x1, y1, x2, y2,
                           couleur='#FF0000',
                           remplissage='#FF0040',
                           epaisseur=2,
                           tag='selection')

def remplir_zone_selection():
    """
    Remplit une zone rectangulaire sélectionnée avec des tuiles aléatoires, en fonction des tuiles adjacentes.
    """
    if not selection_debut or not selection_fin:
        return

    l1, c1 = selection_debut
    l2, c2 = selection_fin

    l_min, l_max = min(l1, l2), max(l1, l2)
    c_min, c_max = min(c1, c2), max(c1, c2)

    etat_avant = {}
    etat_apres = {}

    for i in range(l_min, l_max + 1):
        for j in range(c_min, c_max + 1):
            pos = (i, j)
            etat_avant[pos] = cases_remplies.get(pos, None)

    plateau_complet = [[None for _ in range(globals.colonnes)] for _ in range(globals.lignes)]
    for (i, j), tuile in cases_remplies.items():
        if 0 <= i < globals.lignes and 0 <= j < globals.colonnes:
            nom_tuile = os.path.basename(tuile)[:-4] if isinstance(tuile, str) and tuile.endswith('.png') else tuile
            plateau_complet[i][j] = nom_tuile

    for i in range(l_min, l_max + 1):
        for j in range(c_min, c_max + 1):
            if (i, j) not in cases_remplies:
                modele = solveur.recup_nom(plateau_complet, i, j)
                tuiles_possibles = solveur.rechercher_tuiles(modele, solveur.toutes_tuiles)
                if not tuiles_possibles:
                    tuiles_possibles = solveur.toutes_tuiles
                if tuiles_possibles:
                    nouvelle_tuile = random.choice(tuiles_possibles)
                    cases_remplies[(i, j)] = f"./pack1/tuiles/{nouvelle_tuile}.png"
                    plateau_complet[i][j] = nouvelle_tuile
                    etat_apres[(i, j)] = cases_remplies[(i, j)]

    if etat_avant:
        ajouter_action('remplir', etat_avant, etat_apres)

def initialiser():
    """
    Réinitialise l'état du programme, y compris le facteur de zoom, la position du panorama, les cases remplies,
    le mode d'affichage, et les options de sélection.
    """
    global facteur_zoom, pan_x, pan_y, cases_remplies, window, afficher_grille, mode_actuel
    global plein_ecran, mini_carte_active
    global selection_en_cours, selection_debut, selection_fin  
    
    facteur_zoom = 1.0
    pan_x, pan_y = 0, 0
    cases_remplies = {}
    window = False
    afficher_grille = True
    mode_actuel = "ajouter"
    plein_ecran = False
    mini_carte_active = False

    selection_en_cours = False   
    selection_debut = None       
    selection_fin = None 
    
    globals.lignes = 12
    globals.colonnes = 16

def main():
    """
    Boucle principale du programme, gérant les événements et le rendu de la fenêtre.
    """
    global pan_x, pan_y, window, selection_en_cours

    initialiser()
    besoin_redessiner = True

    while True:
        ev = fltk.donne_ev()
        if ev:
            if fltk.type_ev(ev) == 'ClicGauche':
                x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
                if not window:
                    gerer_clic(x, y)
                    besoin_redessiner = True
            elif fltk.type_ev(ev) == 'Touche':
                touche = fltk.touche(ev)
                if touche == 'Left':
                    pan_x -= 50
                    besoin_redessiner = True
                elif touche == 'Right':
                    pan_x += 50
                    besoin_redessiner = True
                elif touche == 'Up':
                    pan_y -= 50
                    besoin_redessiner = True
                elif touche == 'Down':
                    pan_y += 50
                    besoin_redessiner = True
                elif touche == 'Escape':
                    if window:
                        window = False
                    else:
                        return "retour_menu"
                elif touche == 'z':
                    annuler()
                    besoin_redessiner = True
                elif touche == 'y':
                    refaire()
                    besoin_redessiner = True
            elif fltk.type_ev(ev) == 'Quitte':
                return "quitter"

        if not window:
            if besoin_redessiner:
                fltk.efface_tout()
                dessiner_carte(
                    dico_to_lst(cases_remplies),
                    globals.lignes,
                    globals.colonnes,
                    pan_x,
                    pan_y,
                    facteur_zoom
                )
                besoin_redessiner = False
            else:
                fltk.efface('selection')

            if selection_en_cours:
                dessiner_selection()

            fltk.efface("curseur")
            dessiner_curseur_souris()
            fltk.mise_a_jour()

        fltk.attente(0.01)

if __name__ == "__main__":
    fltk.cree_fenetre(800, 600)
    resultat = main()
    print(f"Résultat: {resultat}")
    fltk.ferme_fenetre()
