import fltk
import globals
import graphique_utils
import tuiles_gestion
import history
import affichage
import actions
import music

selection_rectangle = None
debut_selection = None


def initialiser():
    """
    Réinitialise l'état du programme, y compris le facteur de zoom, la position du panorama, les cases remplies,
    le mode d'affichage, et les options de sélection.
    """
    global facteur_zoom, pan_x, pan_y, mode_actuel
    globals.facteur_zoom = 1.0
    globals.pan_x, globals.pan_y = 0, 0
    globals.window = False
    globals.afficher_grille = True
    globals.mode_actuel = "ajouter"
    globals.plein_ecran = False
    globals.mini_carte_active = False
    globals.selection_en_cours = False
    globals.selection_debut = None
    globals.selection_fin = None
    globals.lignes = 12
    globals.colonnes = 16

def resize(plateau, l ,c):
    '''
    Fonction prenant une map en la mettant à jour à la taille souhaitée.
    Arguments: plateau (lst) - liste de liste
               l, c (int) - taille de ligne et colonne souhaitée
    Return: plateau (lst) - plateau mis à jour
    '''
    while len(plateau) < l:
        plateau.append([None for _ in range(c)])
    for i in range(len(plateau)):
        while len(plateau[i]) < c:
            plateau[i].append(None)
    for i in range(len(plateau)):
        if len(plateau[i]) > c:
            plateau[i] = plateau[i][:c]
    if len(plateau) > l:
        plateau = plateau[:l]
    return plateau

def main():
    """
    Boucle principale du programme, gérant les événements et le rendu de la fenêtre.
    """
    initialiser()
    globals.besoin_redessiner = True

    while True:
        ev = fltk.donne_ev()
        if ev:
            if fltk.type_ev(ev) == 'ClicGauche':
                x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
                if not globals.window:
                    actions.gerer_clic(x, y)
                    globals.besoin_redessiner = True
            elif fltk.type_ev(ev) == 'Touche':
                touche = fltk.touche(ev)
                if touche == 'Left':
                    globals.pan_x -= 50
                    globals.besoin_redessiner = True
                elif touche == 'Right':
                    globals.pan_x += 50
                    globals.besoin_redessiner = True
                elif touche == 'Up':
                    globals.pan_y -= 50
                    globals.besoin_redessiner = True
                elif touche == 'Down':
                    globals.pan_y += 50
                    globals.besoin_redessiner = True
                elif touche == 'Escape':
                    if globals.window:
                        globals.window = False
                    else:
                        return "retour_menu"
                elif touche == 'z':
                    history.annuler()
                    globals.besoin_redessiner = True
                elif touche == 'y':
                    history.refaire()
                    globals.besoin_redessiner = True
            elif fltk.type_ev(ev) == 'Redimension':
                globals.besoin_redessiner = True
            elif fltk.type_ev(ev) == 'Quitte':
                return "quitter"

        if not globals.window:
            if globals.besoin_redessiner:
                fltk.efface_tout()
                if globals.cases_remplies:
                    min_x = min(i for (i, j) in globals.cases_remplies.keys())
                    min_y = min(j for (i, j) in globals.cases_remplies.keys())
                else:
                    min_x = min_y = 0

                plateau, min_x, min_y = tuiles_gestion.dico_to_lst(globals.cases_remplies)
                    
                lignes = len(plateau)
                colonnes = len(plateau[0]) if plateau else 0
                affichage.dessiner_carte(
                    plateau,
                    lignes,
                    colonnes,
                    globals.pan_x,
                    globals.pan_y,
                    globals.facteur_zoom,
                    min_x,
                    min_y
                )

                globals.besoin_redessiner = False
            else:
                fltk.efface('selection')

            if globals.selection_en_cours:
                actions.dessiner_selection()

            fltk.efface("curseur")
            graphique_utils.dessiner_curseur_souris()
            fltk.mise_a_jour()

        fltk.attente(0.01)

if __name__ == "__main__":
    fltk.cree_fenetre(800, 600, redimension=True, frequence=60)
    resultat = main()
    print(f"Résultat: {resultat}")
    fltk.ferme_fenetre()
