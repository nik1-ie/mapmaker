import fltk
from PIL import Image
import globals
import solveur
import graphique_utils
import history
from tuiles_gestion import options
from toolbar import gerer_clic_barre_outils
import file_reading

def dessiner_selection():
    """
    Dessine un rectangle de sélection sur la carte pour indiquer la zone qui sera affectée par les actions de remplissage.
    """
    if not globals.selection_en_cours or not globals.selection_debut:
        return

    x, y = fltk.abscisse_souris(), fltk.ordonnee_souris() - globals.HAUTEUR_BARRE_OUTILS
    taille_case = graphique_utils.actualiser_taille_case()
    col_fin = (x + globals.pan_x) // taille_case
    lig_fin = (y + globals.pan_y) // taille_case

    l1, c1 = globals.selection_debut
    l2, c2 = lig_fin, col_fin

    l_min, l_max = min(l1, l2), max(l1, l2)
    c_min, c_max = min(c1, c2), max(c1, c2)

    for i in range(l_min, l_max + 1):
        for j in range(c_min, c_max + 1):
            x1 = j * taille_case - globals.pan_x
            y1 = i * taille_case - globals.pan_y + globals.HAUTEUR_BARRE_OUTILS
            x2 = x1 + taille_case
            y2 = y1 + taille_case
            fltk.rectangle(x1, y1, x2, y2,
                           couleur='#FF0000',
                           remplissage='#FF0040',
                           epaisseur=2,
                           tag='selection')

def remplir_zone_selection():
    if not globals.selection_debut or not globals.selection_fin:
        return

    l1, c1 = globals.selection_debut
    l2, c2 = globals.selection_fin
    l_min, l_max = min(l1, l2), max(l1, l2)
    c_min, c_max = min(c1, c2), max(c1, c2)

    hauteur = l_max - l_min + 1
    largeur = c_max - c_min + 1
    grille = [[None for _ in range(largeur)] for _ in range(hauteur)]

    for (i, j), tuile in globals.cases_remplies.items():
        if l_min <= i <= l_max and c_min <= j <= c_max:
            grille[i - l_min][j - c_min] = tuile

    success = solveur.completer_carte(grille, type_carte="autre", utilise_mdp=True)

    if success:
        etat_avant = {}
        etat_apres = {}
        for i in range(hauteur):
            for j in range(largeur):
                pos_abs = (i + l_min, j + c_min)
                etat_avant[pos_abs] = globals.cases_remplies.get(pos_abs, None)
                if grille[i][j] is not None:
                    globals.cases_remplies[pos_abs] = grille[i][j]
                    etat_apres[pos_abs] = grille[i][j]
                elif pos_abs in globals.cases_remplies:
                    del globals.cases_remplies[pos_abs]
        history.ajouter_action('remplir', {'cases': etat_avant}, {'cases': etat_apres})
        globals.besoin_redessiner = True
    else:
        print("Aucune solution possible pour cette zone avec les tuiles actuelles.")




def capture_ecran():
    lignes, colonnes = globals.lignes, globals.colonnes
    taille_case = globals.TAILLE_CASE_BASE
    img = Image.new("RGBA", (colonnes * taille_case, lignes * taille_case), (244, 226, 189, 255))
    for (i, j), nom_tuile in globals.cases_remplies.items():
        chemin = f"./pack1/tuiles/{nom_tuile}.png"
        try:
            tuile = Image.open(chemin).convert("RGBA").resize((taille_case, taille_case), Image.NEAREST)
            img.paste(tuile, (j * taille_case, i * taille_case), mask=tuile)
        except Exception:
            pass
    nom_fichier = file_reading.generer_nom_capture()
    try:
        img.save(nom_fichier)
    except Exception:
        return False
    return True

def afficher_galerie_captures():
    """
    Affiche une galerie des captures d'écran précédemment enregistrées, permettant de naviguer entre elles.
    """
    fichiers = file_reading.lister_captures()
    if not fichiers:
        fltk.efface_tout()
        fltk.texte(fltk.largeur_fenetre()//2, fltk.hauteur_fenetre()//2, "Aucune capture trouvée", couleur="#5E4B35", taille=24, ancrage="center", police=globals.POLICE_PIXEL)
        fltk.mise_a_jour()
        fltk.attente(1.5)
        return

    idx = 0
    while True:
        fltk.efface_tout()
        fltk.rectangle(0, 0, fltk.largeur_fenetre(), fltk.hauteur_fenetre(), remplissage="#F4E2BD")
        nom_capture = fichiers[idx].replace("\\", "/").split("/")[-1]
        fltk.texte(fltk.largeur_fenetre()//2, 30, f"Capture {idx+1}/{len(fichiers)} : {nom_capture}", couleur="#5E4B35", taille=18, ancrage="center", police=globals.POLICE_PIXEL)
        try:
            fltk.image(fltk.largeur_fenetre()//2, fltk.hauteur_fenetre()//2, fichiers[idx],
                       largeur=fltk.largeur_fenetre()-80, hauteur=fltk.hauteur_fenetre()-100, ancrage="center")
        except Exception:
            fltk.texte(fltk.largeur_fenetre()//2, fltk.hauteur_fenetre()//2, "Erreur d'affichage", couleur="red", taille=20, ancrage="center")
        fltk.texte(60, fltk.hauteur_fenetre()//2, "<", couleur="#5E4B35", taille=40, ancrage="center")
        fltk.texte(fltk.largeur_fenetre()-60, fltk.hauteur_fenetre()//2, ">", couleur="#5E4B35", taille=40, ancrage="center")
        fltk.texte(fltk.largeur_fenetre()//2, fltk.hauteur_fenetre()-30, "Escape pour quitter", couleur="#5E4B35", taille=14, ancrage="center", police=globals.POLICE_PIXEL)
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

def gerer_clic(x, y):
    """
    Gère les clics de souris sur la grille de la carte, en fonction du mode actuel (ajouter, supprimer, sélectionner, remplacer, remplir).
    """

    if gerer_clic_barre_outils(x, y):
        return True

    if y < globals.HAUTEUR_BARRE_OUTILS:
        return False



    y_ajuste = y - globals.HAUTEUR_BARRE_OUTILS
    taille_case = graphique_utils.actualiser_taille_case()
    colonne = (x + globals.pan_x) // taille_case
    ligne = (y_ajuste + globals.pan_y) // taille_case
    pos = (ligne, colonne)


    if ligne >= globals.lignes:
        globals.lignes = ligne + 1
    if colonne >= globals.colonnes:
        globals.colonnes = colonne + 1

    if globals.mode_actuel == "ajouter":
        avant = globals.cases_remplies.get(pos, None)
        nouvelle_tuile = options(pos)
        if nouvelle_tuile:
            history.ajouter_action('ajouter',
                {'position': pos, 'tuile': avant},
                {'position': pos, 'tuile': nouvelle_tuile}
            )
            globals.cases_remplies[pos] = nouvelle_tuile
            globals.besoin_redessiner = True

    elif globals.mode_actuel == "supprimer":
        if pos in globals.cases_remplies:
            avant = globals.cases_remplies[pos]
            history.ajouter_action('supprimer',
                {'position': pos, 'tuile': avant},
                {'position': pos, 'tuile': None}
            )
            del globals.cases_remplies[pos]
            globals.besoin_redessiner = True

    elif globals.mode_actuel == "remplacer":
        avant = globals.cases_remplies.get(pos, None)
        nouvelle_tuile = options(pos)
        if nouvelle_tuile:
            history.ajouter_action('remplacer',
                {'position': pos, 'tuile': avant},
                {'position': pos, 'tuile': nouvelle_tuile}
            )
            globals.cases_remplies[pos] = nouvelle_tuile
            globals.besoin_redessiner = True

    elif globals.mode_actuel == "remplir":
        if not globals.selection_en_cours:
            globals.selection_debut = (ligne, colonne)
            globals.selection_en_cours = True
        else:
            globals.selection_fin = (ligne, colonne)
            remplir_zone_selection()
            globals.selection_debut = None
            globals.selection_fin = None
            globals.selection_en_cours = False
        return True
    elif globals.mode_actuel == "selectionner":
        plateau = [[None for _ in range(globals.colonnes)] for _ in range(globals.lignes)]
        for (i, j), chemin_tuile in globals.cases_remplies.items():
            if 0 <= i < globals.lignes and 0 <= j < globals.colonnes:
                plateau[i][j] = file_reading.nom_tuile_court(chemin_tuile)
        etat_avant = dict(globals.cases_remplies)

        success = solveur.completer_carte(plateau, type_carte="ile", utilise_mdp=True)

        if success:
            etat_apres = {}
            for i in range(globals.lignes):
                for j in range(globals.colonnes):
                    pos = (i, j)
                    if plateau[i][j] is not None:
                        globals.cases_remplies[pos] = plateau[i][j]
                        etat_apres[pos] = plateau[i][j]
                    elif pos in globals.cases_remplies:
                        del globals.cases_remplies[pos]
            history.ajouter_action('selectionner', {'cases': etat_avant}, {'cases': etat_apres})
            globals.besoin_redessiner = True
        else:
            print("Impossible de compléter la carte avec les tuiles actuelles.")
    

