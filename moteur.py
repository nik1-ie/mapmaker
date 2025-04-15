# --- Imports
# from affichage.py import *

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


def solveur(plateau, i=0, j=0):
    '''
    Solveur automatique...Récursif of course
    '''
    if emplacement_valide(plateau, i, j, plateau[i][j]):
        return True
    
    return

if __name__ == "__main__":
    plateau = [['SSSS','SSSS','SSSS','SSSS', None],
              ['SSSS','SHGS', 'SHRH', 'SHFH', None],
              ['SSSS', None, 'RMPP', 'FMMM', 'PPMM'],
              ['SSSS', None, None, None, None],
              [None, None, None, None, None]]
    solveur()