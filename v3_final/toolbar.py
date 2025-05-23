import fltk
import globals
import history
import graphique_utils
import actions
import sauvegarde
import tuiles_gestion
import music

def gerer_clic_barre_outils(x, y):
    """
    Gère les clics de souris sur la barre d'outils, en changeant le mode d'action ou en effectuant des actions spéciales
    comme le zoom, l'annulation, la restauration, etc.
    """

    if y > globals.HAUTEUR_BARRE_OUTILS:
        return False

    largeur = fltk.largeur_fenetre()
    milieu = largeur // 2

    outils_gauche = [
        "ajouter", "supprimer", "remplacer", "remplir", "selectionner", "annuler", "refaire"
    ]

    x_debut = 10
    for i, action in enumerate(outils_gauche):
        x_bouton = x_debut + i * (globals.LARGEUR_BOUTON + globals.ESPACEMENT_BOUTONS)
        y_bouton = (globals.HAUTEUR_BARRE_OUTILS - globals.HAUTEUR_BOUTON) // 2

        if (x_bouton <= x <= x_bouton + globals.LARGEUR_BOUTON and 
            y_bouton <= y <= y_bouton + globals.HAUTEUR_BOUTON):
            music.play_click_sound(globals.click_1) 
            if action in ["ajouter", "supprimer", "remplacer", "remplir", "selectionner"]:
                globals.mode_actuel = action
                globals.besoin_redessiner = True
            elif action == "annuler":
                history.annuler()
                globals.besoin_redessiner = True
            elif action == "refaire":
                history.refaire()
                globals.besoin_redessiner = True
            return True

    outils_droite = [
        "zoom_plus", "zoom_moins", "grille", "centrer", "sauvegarde", "mini_carte", "capture"
    ]
    
    x_debut = milieu + 10
    for i, action in enumerate(outils_droite):
        x_bouton = x_debut + i * (globals.LARGEUR_BOUTON + globals.ESPACEMENT_BOUTONS)
        y_bouton = (globals.HAUTEUR_BARRE_OUTILS - globals.HAUTEUR_BOUTON) // 2
        
        if (x_bouton <= x <= x_bouton + globals.LARGEUR_BOUTON and 
            y_bouton <= y <= y_bouton + globals.HAUTEUR_BOUTON):
            music.play_click_sound(globals.click_1) 
            if action == "zoom_plus":
                globals.facteur_zoom = min(globals.ZOOM_MAX, globals.facteur_zoom * 1.2)
            elif action == "zoom_moins":
                globals.facteur_zoom = max(globals.ZOOM_MIN, globals.facteur_zoom * 0.8)
            elif action == "grille":
                globals.afficher_grille = not globals.afficher_grille
            elif action == "centrer":
                if globals.chemin_de_tuiles == "./pack1/tuiles/":
                    globals.chemin_de_tuiles = "./pack1/ghi/"
                else: 
                    globals.chemin_de_tuiles = "./pack1/tuiles/"
                fltk.mise_a_jour()
            elif action == "sauvegarde":
                lst, x, y = tuiles_gestion.dico_to_lst(globals.cases_remplies)
                sauvegarde.save(lst)
            elif action == "mini_carte":
                globals.mini_carte_active = not globals.mini_carte_active
            elif action == "capture":
                actions.capture_ecran()
            globals.besoin_redessiner = True
            return True
    
    return False
