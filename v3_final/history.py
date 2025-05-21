import globals

def ajouter_action(action, donnees_avant, donnees_apres):
    """
    Ajoute une action à l'historique des actions, pour permettre l'annulation et la restauration.
    """
    if globals.position_historique < len(globals.historique_actions) - 1:
        globals.historique_actions = globals.historique_actions[:globals.position_historique + 1]

    globals.historique_actions.append({
        'action': action,
        'avant': donnees_avant,
        'apres': donnees_apres
    })
    globals.position_historique = len(globals.historique_actions) - 1

def annuler():
    """
    Annule la dernière action effectuée, en restaurant l'état précédent des cases remplies.
    """
    if globals.position_historique >= 0:
        action = globals.historique_actions[globals.position_historique]
        
        if action['action'] == 'ajouter':
            pos = action['avant']['position']
            if pos in globals.cases_remplies:
                del globals.cases_remplies[pos]
                
        elif action['action'] == 'supprimer':
            pos = action['avant']['position']
            tuile = action['avant']['tuile']
            globals.cases_remplies[pos] = tuile
            
        elif action['action'] == 'remplacer':
            pos = action['avant']['position']
            tuile = action['avant']['tuile']
            globals.cases_remplies[pos] = tuile
            
        elif action['action'] == 'remplir':
            avant = action['avant']['cases'] if 'cases' in action['avant'] else action['avant']
            to_remove = set(globals.cases_remplies.keys()) - set(avant.keys())
            for pos in to_remove:
                del globals.cases_remplies[pos]
            for pos, tuile in avant.items():
                if tuile is None and pos in globals.cases_remplies:
                    del globals.cases_remplies[pos]
                else:
                    globals.cases_remplies[pos] = tuile

        elif action['action'] == 'selectionner':
            avant = action['avant']['cases'] if 'cases' in action['avant'] else action['avant']
            to_remove = set(globals.cases_remplies.keys()) - set(avant.keys())
            for pos in to_remove:
                del globals.cases_remplies[pos]
            for pos, tuile in avant.items():
                if tuile is None and pos in globals.cases_remplies:
                    del globals.cases_remplies[pos]
                else:
                    globals.cases_remplies[pos] = tuile
                    
        globals.position_historique -= 1
        globals.besoin_redessiner = True
        return True
    return False

def refaire():
    """
    Restaure la dernière action annulée, en appliquant à nouveau les changements aux cases remplies.
    """
    if globals.position_historique < len(globals.historique_actions) - 1:
        globals.position_historique += 1
        action = globals.historique_actions[globals.position_historique]
        
        if action['action'] == 'ajouter':
            pos = action['apres']['position']
            tuile = action['apres']['tuile']
            globals.cases_remplies[pos] = tuile
            
        elif action['action'] == 'supprimer':
            pos = action['apres']['position']
            if pos in globals.cases_remplies:
                del globals.cases_remplies[pos]
                
        elif action['action'] == 'remplacer':
            pos = action['apres']['position']
            tuile = action['apres']['tuile']
            globals.cases_remplies[pos] = tuile
            
        elif action['action'] == 'remplir':
            apres = action['apres']['cases'] if 'cases' in action['apres'] else action['apres']
            to_remove = set(globals.cases_remplies.keys()) - set(apres.keys())
            for pos in to_remove:
                del globals.cases_remplies[pos]
            for pos, tuile in apres.items():
                if tuile is None and pos in globals.cases_remplies:
                    del globals.cases_remplies[pos]
                else:
                    globals.cases_remplies[pos] = tuile

        elif action['action'] == 'selectionner':
            apres = action['apres']['cases'] if 'cases' in action['apres'] else action['apres']
            to_remove = set(globals.cases_remplies.keys()) - set(apres.keys())
            for pos in to_remove:
                del globals.cases_remplies[pos]
            for pos, tuile in apres.items():
                if tuile is None and pos in globals.cases_remplies:
                    del globals.cases_remplies[pos]
                else:
                    globals.cases_remplies[pos] = tuile
                        
        globals.besoin_redessiner = True
        return True
    return False
