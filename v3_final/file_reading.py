# --- file_reading.py ---
    # Ce fichier contient les fonctions nécessaires à la lecture de fichiers qui seront utilisées pour 
    # le projet.

# --- Imports ---
import os
import globals
import time
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

def nom_tuile_court(chemin_tuile):
    """
    Extrait les 4 premiers caractères du nom de fichier (sans extension) à partir d'un chemin.
    """
    if chemin_tuile is None:
        return None
    return os.path.splitext(os.path.basename(chemin_tuile))[0][:4]

def trouver_chemin_pack():
    """
    Trouve le chemin du pack de tuiles en fonction de la structure de répertoires.
    Renvoie le chemin du répertoire contenant les tuiles.
    """
    return globals.chemin_de_tuiles
    
def generer_nom_capture(dossier="captures"):
    """
    Génère un nom de fichier unique pour sauvegarder une capture d'écran de la carte.
    Arguments :
        dossier (str) : Dossier où sera enregistrée la capture (par défaut 'captures').
    Retourne :
        str : Chemin complet vers un nouveau fichier PNG nommé selon la date et l'heure courantes.
    """
    if not os.path.exists(dossier):
        os.makedirs(dossier)
    nom_fichier = os.path.join(dossier, f"carte_{time.strftime('%Y%m%d_%H%M%S')}.png")
    return nom_fichier

def lister_captures(dossier="captures"):
    """
    Liste tous les fichiers PNG dans le dossier donné dont le nom commence par 'carte_'.
    Arguments:
        dossier (str): Le dossier où chercher les fichiers de capture. Par défaut 'captures'.
    return:
        list: Une liste des chemins des fichiers PNG trouvés, triée par ordre décroissant.
    """
    if not os.path.exists(dossier):
        return []
    fichiers = [os.path.join(dossier, f) for f in os.listdir(dossier)
                if f.startswith("carte_") and f.endswith(".png")]
    fichiers.sort(reverse=True)
    return fichiers

if __name__ == "__main__":
    files = file_dico('pack1')
    print(files)
