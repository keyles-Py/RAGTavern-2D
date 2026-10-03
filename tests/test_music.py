import os

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import glob

import pygame
import pytest

from game import music


@pytest.fixture(autouse=True)
def _quit_mixer_after_test():
    yield
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()


def test_sounds_directory_has_music_files():
    files = glob.glob(os.path.join(music.SOUNDS_DIR, "*.mp3")) + glob.glob(
        os.path.join(music.SOUNDS_DIR, "*.wav")
    )
    assert files


def test_load_loads_music_from_file():
    music.load()
    assert pygame.mixer.get_init() is not None


def test_play_plays_background_music():
    music.load()
    music.play()
    assert pygame.mixer.music.get_busy()
