# --- Imports
import fltk
import affichage
import globals
import moteur

# --- Fonctions
def menu():
    '''
    Fonctions affichant le menu.
    '''
    fltk.cree_fenetre(800,800)
    fltk.texte(400, 50, "MapMaker", taille=30, ancrage="center", couleur="black")
    boutons = [
        ("Créer", 300, 100),
        ("Solveur test", 300, 180),
        ("JSP2", 300, 260)
        #vous avez capté l'idée...
    ]
    for bouton in boutons:
        fltk.rectangle(bouton[1], bouton[2], bouton[1]+200, bouton[2]+40)
        fltk.texte(bouton[1]+200//2, bouton[2]+40//2, bouton[0], taille=20, ancrage="center")
    
# --- Main
if __name__ == "__main__":
    menu()
    solving_test = [
        ['SSSS', 'SSSS', 'SSSS', 'SSSS', None, None, None, None, None, None],
        ['SSSS', 'SHGS', 'SHRH', 'SHFH', None, None, None, None, None, None],
        ['SSSS', None, 'RMPP', 'FMMM', 'PPMM', None, None, None, None, None],
        ['SSSS', None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None]
    ]
    
    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "Quitte":
            fltk.ferme_fenetre()
            break
        if tev == "ClicGauche":
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            if 300<x<500 and 100<y<140:
                fltk.efface_tout()
                affichage.main()
                break
            if 300 < x < 500 and 180 < y < 220:
                fltk.efface_tout()
                affichage.quadrillage(globals.lignes, globals.colonnes)
                moteur.solveur(solving_test)
                break

                
        fltk.mise_a_jour()
        