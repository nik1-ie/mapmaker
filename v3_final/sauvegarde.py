# --- sauvegarde.py 
#       fichier gérant les sauvegardes, ainsi que l'affichage de sa page
# --- Import
import fltk
import random
import ast
import shutil, os
import globals
from graphique_utils import dessiner_curseur_souris, mise_a_jour_avec_curseur, rectangle_arrondi
from utilitaires import initialiser_gouttes, bouton_clique
import file_reading
import tuiles_gestion
# --- Fonctions


def save_pnj(name, map=""):
    '''
    Fonctions enregistrant l'image en fichier texte et image png.
    Arguments: name (str) - nom du fichier choisi
               map (lst) - liste des images
    
    '''
    #Sauvegarde en fichier texte pour éventuellement pouvoir charger le fichier plus tard
    fichier = open(f"{name}.txt", 'x')
    fichier.write(str(map))
    fichier.close()
    shutil.move(f'{name}.txt',f'saved\{name}.txt')
    return

def typing_bar(x1, y1, x2, y2):
    '''
    Fonction permettant à l'utilisateur d'entrer le nom de fichier souhaité:
    Arguments : Position de la bar.
    Return : name (str) - nom entré par l'utilisateur
    '''
    name = ""
    fltk.texte((x1+x2) //2, (y2+y1) //2, "nommez votre fichier", taille = 20, ancrage= 'center', couleur=globals.COUL_MENU_CONTOUR_MOYEN, police=globals.POLICE_PIXEL, tag="type")
    while True:
        tev = fltk.attend_ev()
        ev = fltk.type_ev(tev)
        if ev == "Touche":
            touche = fltk.touche(tev)
            if touche == "BackSpace":
                name = name[:-1]
                fltk.efface("type")
                fltk.texte((x1+x2) //2, (y2+y1) //2, name, taille = 20, ancrage= 'center', couleur=globals.COUL_MENU_CONTOUR_MOYEN, police=globals.POLICE_PIXEL, tag="type")
            elif touche == "Return":
                fltk.efface("type")
                return name
            elif touche == "space":
                name +="-"
                fltk.efface("type")
                fltk.texte((x1+x2) //2, (y2+y1) //2, name, taille = 20, ancrage= 'center', couleur=globals.COUL_MENU_CONTOUR_MOYEN, police=globals.POLICE_PIXEL, tag="type")
        
            else: 
                name += touche
                fltk.efface("type")
                fltk.texte((x1+x2) //2, (y2+y1) //2, name, taille = 20, ancrage= 'center', couleur=globals.COUL_MENU_CONTOUR_MOYEN, police=globals.POLICE_PIXEL, tag="type")
        
        dessiner_curseur_souris()
        
        mise_a_jour_avec_curseur()
        fltk.attente(0.01)

def get_content(file):
    '''
    Fonction recevant un nom de fichier et return le tableau de la carte contenue.
    Argument : file (str) - nom de fichier
    Return : carte (dico) - dico représentant la map
    '''
    file = open(f"saved/{file}.txt",'r')
    carte = file.read()
    file.close()
    carte = ast.literal_eval(carte)
    carte = tuiles_gestion.lst_to_dico(carte)
    return carte

def save(map = None):
    '''
    Affiche le menu de sauvegarde
    Argument : map (list) - carte créée a éventuellement enregistrer.
    '''
    global selection
    fltk.redimensionne_fenetre(globals.LARGEUR_FENETRE, globals.HAUTEUR_FENETRE)
    gouttes = initialiser_gouttes(globals.NB_GOUTTES)
    boutons = [
    ("⭐", ".pnj"),
    ("", ""),
    ("⭐", "charger")
    ]
    
    while True:
        saved = file_reading.get_files('saved')
        file_coords = []
        fltk.efface_tout()
        fltk.image(globals.LARGEUR_FENETRE//2, globals.HAUTEUR_FENETRE//2, "icons/arbre1.png", largeur=globals.LARGEUR_FENETRE, hauteur=globals.HAUTEUR_FENETRE, ancrage="center")
        for i in range(globals.NB_GOUTTES):
            xg, yg, vitesse = gouttes[i]
            fltk.ligne(xg, yg, xg, yg+12, couleur=globals.COUL_PLUIE, epaisseur=2)
            gouttes[i][1] += vitesse
            if gouttes[i][1] > globals.HAUTEUR_FENETRE:
                gouttes[i][0] = random.randint(0, globals.LARGEUR_FENETRE)
                gouttes[i][1] = random.randint(-20, 0)
                gouttes[i][2] = random.randint(10, 18)
    
        largeur_titre, hauteur_titre = 390, 80
        x_titre = (globals.LARGEUR_FENETRE - largeur_titre) // 2
        y_titre = 32
        rectangle_arrondi(x_titre-6, y_titre-6, largeur_titre+12, hauteur_titre+12, 22, globals.COUL_MENU_CONTOUR_FONCE, "", 3)
        rectangle_arrondi(x_titre-2, y_titre-2, largeur_titre+4, hauteur_titre+4, 18, globals.COUL_MENU_CONTOUR_CLAIR, "", 2)
        rectangle_arrondi(x_titre, y_titre, largeur_titre, hauteur_titre, 16, "", globals.COUL_ENTETE, 0)
        fltk.texte(x_titre + largeur_titre//2, y_titre + 10, "SAUVEGARDE", couleur=globals.COUL_ENTETE_TEXTE,
                police=globals.POLICE_PIXEL, taille=36, ancrage="n")
        fltk.texte(x_titre + largeur_titre//2, y_titre + 49, "", couleur=globals.COUL_ENTETE_TEXTE,
                police=globals.POLICE_PIXEL, taille=36, ancrage="n")
        
        largeur_sous, hauteur_sous = 320, 34
        x_sous = (globals.LARGEUR_FENETRE - largeur_sous) // 2
        y_sous = y_titre + hauteur_titre - 12
        rectangle_arrondi(x_sous, y_sous, largeur_sous, hauteur_sous, 10, globals.COUL_MENU_CONTOUR_FONCE, globals.COUL_SOUS_MENU, 2)
        fltk.texte(x_sous + largeur_sous//2, y_sous + hauteur_sous//2, "enregistre ta belle carte!",
              couleur=globals.COUL_SOUS_MENU_TEXTE, police=globals.POLICE_PIXEL, taille=17, ancrage="c")
        
        largeur_menu, hauteur_menu = 400, 340
        x_menu = (globals.LARGEUR_FENETRE - largeur_menu) // 2
        y_menu = 180
        rectangle_arrondi(x_menu-6, y_menu-6, largeur_menu+12, hauteur_menu+12, 24, globals.COUL_MENU_CONTOUR_FONCE, "", 3)
        rectangle_arrondi(x_menu-2, y_menu-2, largeur_menu+4, hauteur_menu+4, 20, globals.COUL_MENU_CONTOUR_CLAIR, "", 2)
        rectangle_arrondi(x_menu, y_menu, largeur_menu, hauteur_menu, 16, "", globals.COUL_MENU, 0)
        
        largeur_menu, hauteur_menu = 400, 340
        x_menu = (globals.LARGEUR_FENETRE - largeur_menu) // 2
        y_menu = 180
        rectangle_arrondi(x_menu-6, y_menu-6, largeur_menu+12, hauteur_menu+12, 24, globals.COUL_MENU_CONTOUR_FONCE, "", 3)
        rectangle_arrondi(x_menu-2, y_menu-2, largeur_menu+4, hauteur_menu+4, 20, globals.COUL_MENU_CONTOUR_CLAIR, "", 2)
        rectangle_arrondi(x_menu, y_menu, largeur_menu, hauteur_menu, 16, "", globals.COUL_MENU, 0)

        x_souris, y_souris = fltk.abscisse_souris(), fltk.ordonnee_souris()

        for i, (icone, etiquette) in enumerate(boutons):
            y_bouton = globals.y_debut + i * (globals.hauteur_bouton + globals.espacement)
            survole = globals.x_bouton <= x_souris <= globals.x_bouton + globals.largeur_bouton and y_bouton <= y_souris <= y_bouton + globals.hauteur_bouton
            if etiquette != "":
                if survole:
                    rectangle_arrondi(globals.x_bouton, y_bouton, globals.largeur_bouton, globals.hauteur_bouton, 10, globals.COUL_MENU_CONTOUR_FONCE, "", 2)
                    rectangle_arrondi(globals.x_bouton, y_bouton, globals.largeur_bouton, globals.hauteur_bouton, 10, globals.COUL_MENU_CONTOUR_MOYEN, globals.COUL_BOUTON_SURVOL, 2)
                    couleur_texte = globals.COUL_MENU
                    couleur_icone = globals.COUL_MENU
                else:
                    rectangle_arrondi(globals.x_bouton, y_bouton, globals.largeur_bouton, globals.hauteur_bouton, 10, "", globals.COUL_BOUTON, 0)
                    couleur_texte = globals.COUL_BOUTON_TEXTE
                    couleur_icone = globals.COUL_BOUTON_ICONE
                fltk.texte(x_menu + 28, y_bouton + globals.hauteur_bouton // 2, icone,
                    couleur=couleur_icone, police=globals.POLICE_PIXEL, taille=24, ancrage="c")
                fltk.texte(globals.x_bouton + globals.largeur_bouton // 2, y_bouton + globals.hauteur_bouton // 2, etiquette,
                    couleur=couleur_texte, police=globals.POLICE_PIXEL, taille=22, ancrage="c")
                fltk.texte(x_menu + largeur_menu - 28, y_bouton + globals.hauteur_bouton // 2, icone,
                    couleur=couleur_icone, police=globals.POLICE_PIXEL, taille=24, ancrage="c")
            else:
                barx, bary = globals.x_bouton , y_bouton
                barx_end, bary_end = barx + globals.largeur_bouton, bary + globals.hauteur_bouton

        y_fichiers = globals.y_debut + 3 * (globals.hauteur_bouton + globals.espacement) + 10
        for idx, nom_fichier in enumerate(saved):
            fltk.texte(x_menu + largeur_menu // 2, y_fichiers + idx *28 , nom_fichier, couleur=globals.COUL_MENU_CONTOUR_MOYEN,  police=globals.POLICE_PIXEL, taille=20, ancrage="n")
            file_coords.append([(x_menu + largeur_menu // 2,y_fichiers + idx *28)])

        dessiner_curseur_souris()

        ev = fltk.donne_ev()
        if ev is not None:
            tev = fltk.type_ev(ev)
            if tev == "ClicGauche":
                x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
                bouton = bouton_clique(x, y, globals.x_bouton, globals.y_debut, globals.largeur_bouton, globals.hauteur_bouton, globals.espacement, globals.NB_BOUTONS)
                if bouton == 0:
                    file = typing_bar(barx, bary, barx_end, bary_end)
                    save_pnj(file, map)
                for idx, coords_list in enumerate(file_coords):
                    for (fx, fy) in coords_list:
                        if fx - globals.largeur_bouton//2 <= x <= fx + globals.largeur_bouton//2  and fy - globals.hauteur_bouton <= y <= fy + globals.hauteur_bouton:
                            content = get_content(saved[idx])
                            globals.cases_remplies.clear()
                            return "charger carte", content
            elif tev == "Quitte":
                globals.cases_remplies.clear()
                return "menu"
                
        mise_a_jour_avec_curseur()
        fltk.attente(0.01)

if __name__ == "__main__":
    fltk.cree_fenetre(globals.LARGEUR_FENETRE, globals.HAUTEUR_FENETRE)
    p = [['RPGB', 'PFPP', 'PPPF', 'FFFP', 'MPFF'], ['GMGS', 'PPPM', 'PFPP', 'FMPF', 'FMMM'], ['GPGS', 'PMPP', 'PPRM', 'PFMP', 'MMFF'], ['GRRH', 'PMMR', 'RPPM', 'MMRP', 
'FFMM'], ['RPGB', 'MPFP', 'PBDP', 'RPGB', 'MPPP']]
    save(p)