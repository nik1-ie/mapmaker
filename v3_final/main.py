import fltk
import dizayn
import globals
import map_editeur
import sauvegarde
import music


def main():
    """
    Fonction principale qui gère le flux de l'application
    """
    fltk.cree_fenetre(globals.LARGEUR_FENETRE, globals.HAUTEUR_FENETRE, redimension=True, frequence=60, affiche_repere=True)
    a_charger = None
    etat = "menu"
    outcome = None
    music_on = True 
    while True:
        ev = fltk.donne_ev()
        if ev and fltk.type_ev(ev) == "Touche":
            touche = fltk.touche(ev)
            if touche.lower() == "m":
                music_on = not music_on
                if music_on:
                    if etat == "menu":
                        music.play_music(globals.musique_2)
                    else:
                        music.play_music(globals.musique_1)
                else:
                    music.stop_music()
        if etat == "menu":
            if music_on:
                music.play_music(globals.musique_2)
            else:
                music.stop_music()
            action = dizayn.menu()
            if action == "quitter":
                break
            elif action == "nouvelle_carte":
                if music_on:
                    music.play_music(globals.musique_1)
                else:
                    music.stop_music()
                fltk.redimensionne_fenetre(800, 600)
                fltk.mise_a_jour()
                etat = "graphique"
            elif action == "sauvegarde":
                if music_on:
                    music.play_music(globals.musique_1)
                else:
                    music.stop_music()
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
