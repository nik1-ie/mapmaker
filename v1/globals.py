# --- Fichiers de variables globales...

# --- Import
import file_reading


lignes = 10
colonnes = 10

pack_1 = file_reading.file_dico('pack1')
pack1_way = f'pack1/tuiles/'

LARGEUR_FENETRE, HAUTEUR_FENETRE = 500, 631

largeur_fenetre = 800
hauteur_fenetre = 800

COUL_FOND = "#3b4634"
COUL_MENU = "#f7e7b3"
COUL_MENU_CONTOUR_FONCE = "#5f421e"
COUL_MENU_CONTOUR_CLAIR = "#fff7d0"
COUL_MENU_CONTOUR_MOYEN = "#7a5c32"
COUL_ENTETE = "#5f421e"
COUL_ENTETE_TEXTE = "#fff2d0"
COUL_SOUS_MENU = "#f7e7b3"
COUL_SOUS_MENU_TEXTE = "#5f421e"
COUL_BOUTON = "#f7e7b3"
COUL_BOUTON_TEXTE = "#5f421e"
COUL_BOUTON_ICONE = "#5f421e"
COUL_BOUTON_CONTOUR_FONCE = "#5f421e"
COUL_BOUTON_CONTOUR_CLAIR = "#fff7d0"
COUL_BOUTON_SURVOL = "#d9b668"
COUL_PIED = "#162028"
COUL_PLUIE = "#46607c"
POLICE_PIXEL = "Fixedsys"

etiquettes = [
    ("⭐", "nouvelle carte"),
    ("", "sauvegarde"),
    ("⭐", "modèles"),
    ("", "explorer cartes"),
    ("⭐", "paramètres"),
    ("", "quitter")
]
NB_BOUTONS = len(etiquettes)
NB_GOUTTES = 50


largeur_menu, hauteur_menu = 400, 340
x_menu = (LARGEUR_FENETRE - largeur_menu) // 2
y_menu = 180
largeur_bouton = largeur_menu - 32
hauteur_bouton = 44
espacement = 8
x_bouton = x_menu + 16
y_debut = y_menu + 28