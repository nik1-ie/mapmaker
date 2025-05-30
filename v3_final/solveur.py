# --- Imports
import os
import fltk
import random
import time
import affichage
# --- Fonctions 
def recup_toutes_tuiles(tuiles="pack1/tuiles/"):
    """
    Récupère tous les noms de fichiers tuiles disponibles dans le dossier spécifié.
    
    Args:
        tuiles (str): Chemin vers le dossier contenant les tuiles. Par défaut "pack1/tuiles/"
        
    Returns:
        list: Liste des noms de fichiers sans extension (.png)
    """
    return [f[:-4] for f in os.listdir(tuiles) if f.endswith('.png')]

toutes_tuiles = recup_toutes_tuiles()

def verifier_correspondance(tuile, modele):
    """
    Vérifie si une tuile correspond au modèle donné avec des jokers '?'.
    
    Args:
        tuile (str): Nom de la tuile à vérifier (4 caractères)
        modele (str): Modèle à comparer (peut contenir '?' comme joker)
        
    Returns:
        bool: True si la tuile correspond au modèle, False sinon
    """
    if len(tuile) != 4 or len(modele) != 4:
        return False
        
    for i in range(4):
        if modele[i] != '?' and tuile[i] != modele[i]:
            return False
    return True

def rechercher_tuiles(modele, lst_tuiles_dispo):
    """
    Filtre les tuiles disponibles selon un modèle donné.
    
    Args:
        modele (str): Modèle de tuile recherché (peut contenir '?')
        lst_tuiles_dispo (list): Liste des tuiles disponibles
        
    Returns:
        list: Liste des tuiles correspondant au modèle
    """
    return [tuile for tuile in lst_tuiles_dispo if verifier_correspondance(tuile, modele)]

def est_liste_de_none(lst_principale):
    """
    Vérifie si une liste ne contient que des valeurs None.
    
    Args:
        lst_principale (list): Liste de listes à vérifier
        
    Returns:
        bool: True si tous les éléments sont None, False sinon
    """
    for sous_liste in lst_principale:
        for element in sous_liste:
            if element is not None:
                return False
    return True 

def emplacement_valide(grille, i, j, nom_tuile):
    """
    Vérifie si une tuile peut être placée à la position donnée en respectant les voisins.
    
    Args:
        grille (list): Grille des tuiles représentant la carte
        i (int): Index de ligne
        j (int): Index de colonne
        nom_tuile (str): Nom de la tuile à placer
        
    Returns:
        bool: True si le placement est valide, False sinon
    """
    directions = [(-1, 0, 2), (0, 1, 3), (1, 0, 0), (0, -1, 1)]  # (di, dj, index_opposé)
    
    for di, dj, opp in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(grille) and 0 <= nj < len(grille[0]):
            if grille[ni][nj] is not None:
                if grille[ni][nj][opp] != nom_tuile[directions.index((di, dj, opp))]:
                    return False
    return True

def recup_nom(grille, i, j):
    """
    Génère le modèle de tuile requis pour une position basée sur les voisins.
    
    Args:
        grille (list): Grille des tuiles représentant la carte
        i (int): Index de ligne
        j (int): Index de colonne
        
    Returns:
        str: Modèle de tuile requis (contient '?' pour les cases vides/inconnues)
    """
    directions = [(-1, 0, 2), (0, 1, 3), (1, 0, 0), (0, -1, 1)] 
    modele = []
    
    for di, dj, opp in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(grille) and 0 <= nj < len(grille[0]):
            if grille[ni][nj] is not None:
                modele.append(grille[ni][nj][opp])
            else:
                modele.append('?')
        else:
            modele.append('?')
    
    return ''.join(modele)

def trouver_case_vide(grille):
    """
    Trouve la première case vide dans la grille (parcours ligne par ligne).
    
    Args:
        grille (list): Grille  à parcourir
        
    Returns:
        tuple: Coordonnées (i,j) de la première case vide trouvée, ou None
    """
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] is None:
                return (i, j)
    return None

def trouver_case_la_plus_contrainte(grille):
    """
    Trouve la case vide avec le moins de possibilités de tuiles .
    
    Args:
        grille (list): Grille des truiles à analyser
        
    Returns:
        tuple: Coordonnées (i,j) de la case la plus contrainte, ou None
    """
    min_possibilites = float('inf')
    meilleure_case = None
    
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] is None:
                modele = recup_nom(grille, i, j)
                possibilites = len(rechercher_tuiles(modele, toutes_tuiles))
                
                if possibilites < min_possibilites:
                    min_possibilites = possibilites
                    meilleure_case = (i, j)
                    if min_possibilites == 0:
                        return meilleure_case
    return meilleure_case

def initialiser_bords_ile(grille):
    """
    Initialise les bords d'une grille avec des tuiles de mer ('SSSS') pour une île.
    
    Args:
        grille (list): Grille des tuiles
        
    Returns:
        list: Grille modifiée avec les bords remplis
    """
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if i == 0 or i == len(grille)-1 or j == 0 or j == len(grille[0])-1:
                grille[i][j] = "SSSS"
    return grille

def solveur_recursif(grille, type_carte="ile", utilise_mdp=True):
    """
    Solveur récursif avec backtracking pour compléter la carte automatiquement.
    
    Args:
        grille (list): Grille des tuiles  à compléter
        type_carte (str): Type de carte ("ile" ou autre)
        utilise_mdp (bool): Utilise la partie avec la case la plus contrainte
        
    Returns:
        bool: True si une solution a été trouvée, False sinon
    """
    case_vide = trouver_case_la_plus_contrainte(grille) if utilise_mdp else trouver_case_vide(grille)
    
    if not case_vide:
        return True
    
    i, j = case_vide
    
    modele = recup_nom(grille, i, j)
    tuiles_possibles = rechercher_tuiles(modele, toutes_tuiles)
    random.shuffle(tuiles_possibles)
    
    for tuile in tuiles_possibles:
        grille[i][j] = tuile
        
        if solveur_recursif(grille, type_carte, utilise_mdp):
            return True
            
        grille[i][j] = None
    
    return False

def completer_carte(grille, type_carte="ile", utilise_mdp=True):
    """
    Fonction principale pour compléter une carte selon le type spécifié.
    
    Args:
        grille (list): Grille des tuiles à compléter (sera modifiée)
        type_carte (str): Type de carte ("ile" ou autre)
        utilise_mdp (bool): Utilise la partie avec la case la plus contrainte
        
    Returns:
        bool: True si la carte a pu être complétée, False sinon
    """
    if type_carte == "ile":
        grille = initialiser_bords_ile(grille)
    
    grille_copie = [ligne.copy() for ligne in grille]
    
    if solveur_recursif(grille_copie, type_carte, utilise_mdp):
        for i in range(len(grille)):
            grille[i] = grille_copie[i].copy()
        return True
    return False

def ajout_decors(grille, decors_terre="pack1/decors/terre", decors_mer="pack1/decors/mer"):
    """
    Ajoute aléatoirement des décors sur les tuiles de plaines ('P') et de mer ('SSSS') dans la grille.
    Pour les tuiles contenant plusieurs plaines, place un décor à une position spécifique en fonction
    des emplacements des 'P' dans le nom de la tuile. Pour les tuiles de mer, place occasionnellement
    un décor maritime au centre de la tuile.

    Args:
        grille (list): Grille 2D représentant la carte, chaque élément est une chaîne de 4 caractères
                      décrivant les biomes ou 'SSSS' pour la mer.
        decors_terre (str): Chemin vers le dossier contenant les images de décors terrestres.
                           Par défaut "pack1/decors/terre".
        decors_mer (str): Chemin vers le dossier contenant les images de décors maritimes.
                         Par défaut "pack1/decors/mer".

    Returns:
        None: La fonction affiche directement les décors via fltk mais ne retourne rien.
    """
    decors_terre = [f for f in os.listdir(decors_terre)]
    decors_mer = [f for f in os.listdir(decors_mer)]
    largeur = fltk.largeur_fenetre()
    hauteur = fltk.hauteur_fenetre()
    lignes = len(grille)
    colonnes = len(grille[0])

    chemin = 'pack1/decors/'
    dico_pos = {(0,3):(0,0,'nw'), (0,1):(largeur/lignes, 0,'ne'), (0,2):(0,hauteur/colonnes,'sw'),(1,2):(largeur/lignes,hauteur/colonnes,'se'),(2,3):(0,hauteur/colonnes,'sw'), (1,3): (0,hauteur/colonnes/2,'w')}
    for i in range(len(grille)):
        for j in range(len(grille[i])):

            if grille[i][j].count('P') > 1:

                alea = random.randint(1, 2)
                if alea == 1:
                    positions_p = [pos for pos, char in enumerate(grille[i][j]) if char == 'P']
                    pre,deu = positions_p[0],positions_p[1]
                    image = random.choice(decors_terre)
                    fltk.image(j * (largeur / len(grille[0])) + dico_pos[(pre,deu)][0], 
                             i * (hauteur / len(grille)) +dico_pos[(pre,deu)][1], chemin + 'terre/' + image,
                                 largeur=int((largeur // len(grille[0])) * 0.23), 
                                 hauteur=int((hauteur // len(grille)) * 0.23), 
                                 ancrage=dico_pos[(pre,deu)][2])
            

            elif 'SSSS' == grille[i][j]:
                alea = random.randint(1, 5)
                if alea == 1:
                    image = random.choice(decors_mer)
                    fltk.image(j * (largeur / len(grille[0])) + (largeur / len(grille[0])) / 2, 
                             i * (hauteur / len(grille)) + (hauteur / len(grille)) / 2, 
                             chemin + 'mer/' + image, 
                             largeur=int((largeur // len(grille[0])) * 0.5), 
                             hauteur=int((hauteur // len(grille)) * 0.5), 
                             ancrage='center')

if __name__ == "__main__":
    """
    Point d'entrée principal du programme.
    Initialise une fenêtre graphique et génère une carte.
    """
    fltk.cree_fenetre(800, 800)
    
    plateau_vide = [[None for _ in range(10)] for _ in range(10)]
    #plateau_vide = [
    #["SSSS", "SSSS", "SSSS", "SSSS", "SSSS", "SSSS", "SSSS", "SSSS"],
    #["SSSS", "SHGS", None,   None,   None,   None,   "SHPH", "SSSS"],
    #["SSSS", None,   "FMMM", "PPMM", None,   "RMPP", None,   "SSSS"],
    #["SSSS", None,   "PPPF", None,   "GFGS", None,   None,   "SSSS"],
    #["SSSS", None,   None,   "PBDP", None,   None,   None,   "SSSS"],
    #["SSSS", None,   "PPMF", None,   None,   None,   None,   "SSSS"],
    #["SSSS", "GRGS", None,   None,   None,   None,   "GFGS", "SSSS"],
    #["SSSS", "SSSS", "SSSS", "SSSS", "SSSS", "SSSS", "SSSS", "SSSS"]]
    lignes = len(plateau_vide)
    colonnes = len(plateau_vide[0])
    
    affichage.affichage_map(plateau_vide, lignes, colonnes)
    affichage.quadrillage(lignes, colonnes)
    time.sleep(2)
    fltk.mise_a_jour()
    
    if completer_carte(plateau_vide, "ile"):
        print("Carte complétée avec succès!")
        time.sleep(1)
        affichage.affichage_map(plateau_vide, lignes, colonnes)
        affichage.quadrillage(lignes, colonnes)
    else:
        fltk.rectangle(0, 0, fltk.largeur_fenetre(), fltk.hauteur_fenetre(), remplissage='white')
        fltk.texte(fltk.largeur_fenetre()/2, fltk.hauteur_fenetre()/2, "Aucune solution possible:", ancrage='center')
        fltk.mise_a_jour()
        print("Aucune solution")
    
    while True:
        fltk.mise_a_jour()
