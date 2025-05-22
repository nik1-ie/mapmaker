import pygame
pygame.init()
pygame.mixer.init()
    
def play_music(file=None):
    """
    Joue la musique de fond.
    """
    if file:
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(0.05)  
        pygame.mixer.music.play(-1)  
    else:
        pygame.mixer.music.stop()

def play_click_sound(file=None):
    """
    Joue un son de clic.
    """
    if file:
        sound = pygame.mixer.Sound(file)
        sound.set_volume(0.4) 
        sound.play()
    else:
        pass

def stop_music():
    """
    Arrête la musique de fond.
    """
    pygame.mixer.music.stop()