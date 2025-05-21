import fltk
import dizayn
import graphique
import globals

def main():
    """
    Fonction principale qui gère le flux de l'application
    """
    fltk.cree_fenetre(globals.LARGEUR_FENETRE, globals.HAUTEUR_FENETRE)
    
    etat = "menu"
    
    while True:
        if etat == "menu":
            action = dizayn.menu()
            if action == "quitter":
                break
            elif action == "nouvelle_carte":
                fltk.redimensionne_fenetre(800, 600)
                etat = "graphique"
        elif etat == "graphique":
            resultat = graphique.main()
            if resultat == "retour_menu":
                fltk.redimensionne_fenetre(globals.LARGEUR_FENETRE, globals.HAUTEUR_FENETRE)
                etat = "menu"
            elif resultat == "quitter":
                break
    
    fltk.ferme_fenetre()

if __name__ == "__main__":
    main()
