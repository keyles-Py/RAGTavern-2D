import os
import pygame

SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "sounds")
DEFAULT_TRACK = os.path.join(SOUNDS_DIR, "Night In The Tavern.mp3")


def load(path: str = DEFAULT_TRACK) -> None:
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load(path)


def play(loops: int = -1) -> None:
    pygame.mixer.music.play(loops)
