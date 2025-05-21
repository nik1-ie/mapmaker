# --- Fichiers de variables globales...

# --- Imports ---
import file_reading
import os

# --- Paramètres de la carte ---
colonnes = 10
lignes = 10
NB_GOUTTES = 50
pack_1 = file_reading.file_dico('pack1')
pack1_way = f'pack1/tuiles/'

# --- Dimensions de la fenêtre et de l'écran ---
HAUTEUR_BARRE_OUTILS = 60
HAUTEUR_BOUTON = 50
HAUTEUR_ECRAN = 1080
LARGEUR_BOUTON = 50
LARGEUR_ECRAN = 1920
LARGEUR_FENETRE, HAUTEUR_FENETRE = 500, 631
TAILLE_CASE_BASE = 50
TAILLE_FENETRE_DEFAUT = (800, 600)
TAILLE_ICONE = 24
ESPACEMENT_BOUTONS = 5

# --- Limites de zoom ---
ZOOM_MAX = 3.0
ZOOM_MIN = 0.5

# --- Couleurs d’interface ---
COUL_BOUTON = "#f7e7b3"
COUL_BOUTON_CONTOUR_CLAIR = "#fff7d0"
COUL_BOUTON_CONTOUR_FONCE = "#5f421e"
COUL_BOUTON_ICONE = "#5f421e"
COUL_BOUTON_SURVOL = "#d9b668"
COUL_BOUTON_TEXTE = "#5f421e"
COUL_ENTETE = "#5f421e"
COUL_ENTETE_TEXTE = "#fff2d0"
COUL_FOND = "#3b4634"
COUL_MENU = "#f7e7b3"
COUL_MENU_CONTOUR_CLAIR = "#fff7d0"
COUL_MENU_CONTOUR_FONCE = "#5f421e"
COUL_MENU_CONTOUR_MOYEN = "#7a5c32"
COUL_PIED = "#162028"
COUL_PLUIE = "#46607c"
COUL_SOUS_MENU = "#f7e7b3"
COUL_SOUS_MENU_TEXTE = "#5f421e"

COULEUR_BARRE_OUTILS = "#F4E2BD"
COULEUR_BOUTON_ACTIF = "#B89F81"
COULEUR_BOUTON_INACTIF = "#E8D5A9"
COULEUR_SEPARATEUR = "#B89F81"
COULEUR_TEXTE_BOUTON = "#5E4B35"

# --- Icônes ---
ICONS = {
    "ajouter": "./icons/add.png",
    "annuler": "./icons/previous.png",
    "capture": "./icons/photo-size.png",
    "centrer": "./icons/minimize.png",
    "grille": "./icons/computer.png",
    "mini_carte": "./icons/search.png",
    "plein_ecran": "./icons/maximize.png",
    "refaire": "./icons/next-icon.png",
    "remplacer": "./icons/love.png",
    "remplir": "./icons/camera.png",
    "selectionner": "./icons/maximize (1).png",
    "supprimer": "./icons/subtract.png",
    "zoom_moins": "./icons/zoom-out.png",
    "zoom_plus": "./icons/zoom-in.png",
}

# --- Étiquettes et police ---
etiquettes = [
    ("⭐", "nouvelle carte"),
    ("", "charger carte"),
    ("⭐", "modèles"),
    ("", "explorer cartes"),
    ("⭐", "paramètres"),
    ("", "quitter")
]
NB_BOUTONS = len(etiquettes)
POLICE_PIXEL = "Fixedsys"

# --- Variables d’état ---
afficher_grille = True
besoin_redessiner = False
cases_remplies = {}
facteur_zoom = 1.0
historique_actions = []
mini_carte_active = False
mode_actuel = "ajouter"
pan_x, pan_y = 0, 0
plein_ecran = False
position_historique = -1
selection_debut = None
selection_en_cours = False
selection_fin = None
window = False

# --- Paramtères de la sauvegarde ---
largeur_menu, hauteur_menu = 400, 340
x_menu = (LARGEUR_FENETRE - largeur_menu) // 2
y_menu = 180
largeur_bouton = largeur_menu - 32
hauteur_bouton = 44
espacement = 8
x_bouton = x_menu + 16
y_debut = y_menu + 28