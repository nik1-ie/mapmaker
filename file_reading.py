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
    return get_files(pack, os.listdir(pack))

def get_files(pack, reps):
    '''
    Pour chaque dossier, on récupère les noms de fichiers que l'on stocke dans un dictionnaire.
    Arguments : rep (list) - liste des noms de dossiers
    Return : (dict) - dictionnaire de noms de fichiers selon le dossier dans lesquels ils se trouvent
    '''
    files = {}
    for dossier in reps:
        files[dossier] = os.listdir(f'{pack}\{dossier}')
    return files