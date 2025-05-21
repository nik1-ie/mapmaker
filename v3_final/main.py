import fltk
import dizayn
import globals
import map_editeur
import sauvegarde


def main():
    """
    Fonction principale qui gère le flux de l'application
    """
    fltk.cree_fenetre(globals.LARGEUR_FENETRE, globals.HAUTEUR_FENETRE, redimension=True, frequence=60, affiche_repere=True)
    a_charger = None
    etat = "menu"
    outcome = None
    while True:
        if etat == "menu":
            action = dizayn.menu()
            if action == "quitter":
                break
            elif action == "nouvelle_carte":
                fltk.redimensionne_fenetre(800, 600)
                etat = "graphique"
            elif action == "sauvegarde":
                etat = "sauvegarde"
        elif etat == "graphique":

            resultat = map_editeur.main()
            if resultat == "retour_menu":
                globals.cases_remplies.clear()
                fltk.redimensionne_fenetre(globals.LARGEUR_FENETRE, globals.HAUTEUR_FENETRE)
                etat = "menu"
            elif resultat == "quitter":
                break
        elif etat == "sauvegarde":
            outcome, a_charger = sauvegarde.save()
            globals.cases_remplies = a_charger
            etat = "graphique"
            if outcome == "quitter":
                break
    
    fltk.ferme_fenetre()

if __name__ == "__main__":
    main()
