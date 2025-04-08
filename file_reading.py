# --- file_reading.py ---
    # Ce fichier contient les fonctions nécessaires à la lecture de fichiers qui seront utilisées pour 
    # le projet.

# --- Imports ---
import os

# --- Fonctions ---

def get_repo_name(pack):
    '''
    Fonction permettant de récupérer les noms de dossier et de fichiers de tuiles, images, etc.
    Arguments : pack (str) - nom du pack/dossier principal choisi
    Return : appel de la fonction get_files()
    '''
    return os.listdir(pack)

def get_files(chemin):
    '''
    Pour le dossier donné, on récupère les noms de fichiers que l'on stocke dans une dictionnaire.
    Arguments : pack (str) - nom de pack
                rep (str) - nom de dossier
    Return : (liste) - dictionnaire de noms de fichiers selon le dossier dans lesquels ils se trouvent
    '''
    files = []
    for name in os.listdir(chemin):
        files.append(name[:-4])
    return files

def file_dico(pack, dict = {}):
    '''
    Fonction récursive créeant directement le dictionnaire.
    Arguments : pack (str) - chosen pack
                dict (dict) - dictionnaire en cours de création
    Return :    dict (dict) - dictionnaire de chemins et de ficheirs complété
    '''
    list = get_repo_name(pack)
    for filename in list:
        full_path = os.path.join(pack, filename)
        full_path = os.path.normpath(full_path)
        if os.path.isdir(full_path):
            file_dico(full_path)
        elif os.path.isfile(full_path):
            dict[os.path.dirname(full_path)] = get_files(os.path.dirname(full_path))
            return dict
    return dict

if __name__ == "__main__":
    files = file_dico('pack1')
    print(files)
