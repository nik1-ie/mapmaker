# Imports
import globals
import os


# Conditions des tuiles aled
def recup_toutes_tuiles(tiles_dir="pack1/tuiles/"):
    """Récupère toutes les tuiles disponibles (noms sans extension)"""
    return [f[:-4] for f in os.listdir(tiles_dir)]
print(recup_toutes_tuiles())


def verifier_correspondance(tuile, modele):
    """Vérifie si une tuile correspond au modèle (4 caractères avec ? pour joker)"""
    if len(tuile) != 4 or len(modele) != 4:
        return False
        
    for i in range(4):
        if modele[i] != '?' and tuile[i] != modele[i]:
            return False
    return True


def rechercher_tuiles(modele):
    """Retourne TOUTES les tuiles correspondant au modèle sous forme de liste"""
    tuiles_disponibles = recup_toutes_tuiles()
    resultats = []
    
    for tuile in tuiles_disponibles:
        if verifier_correspondance(tuile, modele):
            resultats.append(tuile)
    
    return resultats


#Autre
def emplacement_valide(grille, i, j, nom_tuile):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dico = {0:2, 1: 3, 2: 0, 3: 1}
    bon = True
    for indice in range(len(directions)):
        x = directions[indice][0]
        y = directions[indice][1]
        if grille[i + x][j + y][dico[indice]] == nom_tuile[indice]:
            bon = True
        else:
            bon = False
    return bon

def recup_nom(grille, i, j):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dico = {0:2, 1: 3, 2: 0, 3: 1}
    nom = ""
    for indice in range(len(directions)):
        x = directions[indice][0]
        y = directions[indice][1]
        if grille[i + x][j + y] is None:
            nom = "?"
            #recup_nom(grille, i + x, j + y) faudrait pouvoir vérif le None avec une priorité ou en enlevant de la liste des cases vides//// ou bien faire un aleatoire  ou tempo jspp
        else:
            nom += grille[i + x][j + y][dico[indice]]
    return nom

def recup_vide(grille):
    #dico pour pouvoir recup les coords et le statut de la case vide (pour le récursif)
    coord= []
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] is None:
                coord.append((i,j))
    return coord

















#Niki Core :
def tuile_valide(grille, i, j, nom_tuile):
    '''
    Fonction vérifiant si l'emplacement de la tuile colle par rapport aux tuiles l'entourant.
    Arguments : grille (list de list) - plateau représentant notre map
                i, j (int) - position de la tuile à  vérifier
                nom_tuile (str) - nom de notre tuile
    Return : Booléen
    '''
    tuile_link  = {0:(-1, 0), 1:(0, 1), 2:(1, 0), 3:(0, -1)}

    for v in range (2):
        
        x, y = i + tuile_link[v][0] , j + tuile_link[v][1] #the tuile we're lookin for
        if i + tuile_link[v][0] >= len(grille):
            x = i
        elif j + tuile_link[v][1] <= len(grille[0]):
            y = j

        voisin = grille[x][y]
        if voisin != None:
            if nom_tuile[v] != voisin[v + 2]:
                return False
    return True

def smart_pick(plateau, i, j, dir):
    '''
    Fonction choisissant la tuile PARFAITE dans la direction choisie
    Arguments : plateau (list) - grille de tuiles
                i, j (int) - position actuelle
                dir (tuple) - direction recherchée
    Return : tuile (str) - nom de tuile existante et qui valide les conditions
    '''
    x,y = dir
    prec_tuile = plateau[i][j]
    
    if i+x > len(plateau) or j+y > len(plateau[0]): #Si la direction dans laquelle on veut aller est inexistante
        print("This shouldn't happen.")
        return prec_tuile
    
    # get connexion letter on the needed side. 
    tuile_link  = {(-1, 0):0, (0, 1):1, (1, 0):2, (0, -1):3}
    link_dir = tuile_link[dir] #id of the letter needed
    link = plateau[i][j][link_dir] #the tuile connexion we need
    print(globals.pack_1)
    pack = globals.pack_1['pack1/tuiles']
    copy = plateau.copy()
    print("Copie : ", copy, "End copy")
    for file in pack:
        if file[link_dir] == link:
            print("File matches!")
            copy[i + dir[0]][j + dir [1]] = link
            print("Edited copy", copy, "End edited copy")
            if tuile_valide(copy, i, j, file):
                print("File completly matches!")
                return file
            print("File does not match entirely.")
    return None

def verify_all(grille):
    '''
    Fonction vérifiant tout
    '''
    if None in grille:
        return False
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if emplacement_valide(grille, i ,j ,grille[i][j]) != True:
                return False
    return True
        

def solveur(plateau, i=0, j=0):
    '''
    Solveur automatique...Récursif of course
    '''
    # affichage_map(plateau, globals.lignes, globals.colonnes)
    if verify_all(plateau): #Si tout est ok!!
        return plateau
    
    if i == len(plateau) and j == len(plateau[0]): #Si t'es au bout du tableau sans avoir rien trouvé
        return False
    
    #Make an if qui fait les nv i, j et trouve une direction pour smart pick (how would it even work...)
    new_i, new_j = 0, 0
    if j == len(plateau[0]):
        new_i, new_j = i+1, 0
        if plateau[new_i][new_j]==None:
            print("Empty case, not normal!")
        else:
            print("On avance en x")
            dir = (1, 0)
    else:
        new_i, new_j = i, j+1
        if new_j == len(plateau[0]):
            dir = (1, 0)
        dir = (0, 1)
        
    plateau2 = plateau.copy()
    plateau2[i + dir[0]][j + dir[1]]=smart_pick(plateau, i,j, dir)
    
    if solveur(plateau2, new_i, new_j):
        return True
    solveur(plateau2, new_i, new_j)
    return


#TEST YIPIIII
if __name__ == "__main__":
    plateau = [['SSSS','SSSS','SSSS','SSSS', None],
           ['SSSS','SHGS', 'SHRH', 'SHFH', None],
           ['SSSS', None, 'RMPP', 'FMMM', 'PPMM'],
           ['SSSS', None, None, None, None],
           [None, None, None, None, None]]

    plateau_pasbon = [['SSSS','SSSS','SSSS','SSSS', None],
           ['SSSS','SSDH', 'SHRH', 'SHFH', None],
           ['SSSS', None, 'RMPP', 'FMMM', 'PPMM'],
           ['SSSS', None, None, None, None],
           [None, None, None, None, None]]
    #print(emplacement_valide(plateau, 1, 2, 'SHRM'))
    print(recup_vide(plateau))
    print(recup_nom(plateau, 3, 1))


    # Liste de tuiles avec Forêt en haut et Rivière en bas
    print("\nTuiles F?R? (Forêt haut, Rivière bas):")
    print(rechercher_tuiles("F?R?"))

    # Liste de tuiles avec Mer à gauche
    print("\nTuiles ???S (Mer gauche):")
    print(rechercher_tuiles("???S"))  # Retourne une liste

    # Liste de tuiles avec Plaine en bas
    print("\nTuiles ??P? (Plaine bas):")
    print(rechercher_tuiles("??P?"))  # Retourne une liste
    
    # 4. Cas où aucune tuile ne correspond
    print("\nTuiles XXXX (Aucune correspondance):")
    print(rechercher_tuiles("XXXX"))  # Retourne une liste vide pour le moment mais tkt on doit faire la verif si c'est une cote ou pas
    #genre si c'est une cote on met aleatoire spécial cote et sinon on met ce qu on veut hors cote.
