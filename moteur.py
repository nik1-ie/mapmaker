# --- Imports
from affichage import *
import globals

# --- Fonctions

def emplacement_valide(grille, i, j, nom_tuile):
    '''
    J'ai remis la fonction de Noam ici idk pour utiliser avec le solveur ig
    '''
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

def smart_pick(plateau, i, j, dir):
    '''
    Fonction choisissant la tuile PARFAITE dans la direction choisie
    Arguments : plateau (list) - grille de tuiles
                i, j (int) - position actuelle
                dir (tuple) - direction recherchée
    Return : tuile (str) - nom de tuile existante et qui valide les conditions
    '''
    tuile = ""
    x,y = dir
    tuilex, tuiley = i+x, j+y
    prec_tuile = plateau[i][j]
    
    if i+x > len(plateau) or j+y > len(plateau[0]): #Si la direction dans laquelle on veut aller est inexistante
        print("This shouldn't happen.")
        return prec_tuile
    
    dico = {0:2, 1: 3, 2: 0, 3: 1}
    
    # get connexion letter on the needed side. 
    # look in globals.pack_1 for a tuile that matches
    # verify if anything clashes nearby
    # yes or no, retry if needed idk
    
    return tuile

def solveur(plateau, i=0, j=0):
    '''
    Solveur automatique...Récursif of course
    '''
    affichage_map(plateau, globals.lignes, globals.colonnes)
    if emplacement_valide(plateau, i, j, plateau[i][j]): #Si tout est ok!!
        return True
    
    if i == len(plateau) and j == len(plateau[0]): #Si t'es au bout du tableau sans avoir rien trouvé
        return False
    
    #Make an if qui fait les nv i, j et trouve une direction pour smart pick (how would it even work...)
    new_i, new_j = 0, 0
    if j == len(plateau[0]):
        new_i, new_j = i+1, 0
        if plateau[new_i][new_j]==None:
            print("Empty case, filling it up!")
            dir = (0, 0)
        else:
            print("On avance en x")
            dir = (1, 0)
    else:
        new_i, new_j = i, j+1
        if new_j == len(plateau[0]):
            dir = (1, 0)
        
    plateau2 = plateau 
    plateau2[i + dir[0]][j + dir[1]]=smart_pick(plateau, i,j)
    
    if solveur(plateau2, new_i, new_j):
        return True
    solveur(plateau2, new_i, new_j)
    return

if __name__ == "__main__":
    plateau = [['SSSS','SSSS','SSSS','SSSS', None],
              ['SSSS','SHGS', 'SHRH', 'SHFH', None],
              ['SSSS', None, 'RMPP', 'FMMM', 'PPMM'],
              ['SSSS', None, None, None, None],
              [None, None, None, None, None]]
    solveur(plateau)