import os

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
import pytest

from game import music, pause


def _key(key):
    return pygame.event.Event(pygame.KEYDOWN, key=key)


@pytest.fixture(autouse=True)
def _reset_state():
    pause.resume()
    yield
    pause.resume()
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()


def test_pause_and_resume_functions_exist():
    assert callable(pause.pause)
    assert callable(pause.resume)


def test_pause_stops_game_execution():
    music.load()
    music.play()

    pause.pause()

    assert pause.is_paused()
    assert not pygame.mixer.music.get_busy()


def test_resume_resumes_game_execution():
    music.load()
    music.play()
    pause.pause()

    pause.resume()

    assert not pause.is_paused()
    assert pygame.mixer.music.get_busy()


def test_esc_pauses_and_resumes_game():
    pause.handle_event(_key(pygame.K_ESCAPE))
    assert pause.is_paused()

    pause.handle_event(_key(pygame.K_ESCAPE))
    assert not pause.is_paused()


def test_resume_option_in_pause_menu_resumes_game():
    pause.pause()
    assert pause.selected_option() == pause.RESUME

    action = pause.handle_event(_key(pygame.K_RETURN))

    assert action == pause.RESUME
    assert not pause.is_paused()


def test_quit_option_in_pause_menu_exits_game():
    pause.pause()
    pause.handle_event(_key(pygame.K_DOWN))
    assert pause.selected_option() == pause.QUIT

    action = pause.handle_event(_key(pygame.K_RETURN))

    assert action == pause.QUIT


def test_menu_keys_are_ignored_when_not_paused():
    assert pause.handle_event(_key(pygame.K_RETURN)) is None
    assert not pause.is_paused()


def test_draw_menu_renders_without_errors():
    pygame.font.init()
    screen = pygame.Surface((800, 600))
    pause.pause()

    pause.draw_menu(screen, pygame.font.SysFont("Arial", 40))
