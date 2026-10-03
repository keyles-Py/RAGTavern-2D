import pygame

RESUME = "resume"
QUIT = "quit"
MENU_OPTIONS = [("Reanudar", RESUME), ("Salir", QUIT)]

_paused = False
_selected = 0


def is_paused() -> bool:
    return _paused


def selected_option() -> str:
    return MENU_OPTIONS[_selected][1]


def pause() -> None:
    global _paused, _selected
    _paused = True
    _selected = 0
    if pygame.mixer.get_init():
        pygame.mixer.music.pause()


def resume() -> None:
    global _paused
    _paused = False
    if pygame.mixer.get_init():
        pygame.mixer.music.unpause()


def toggle() -> None:
    if _paused:
        resume()
    else:
        pause()


def handle_event(event) -> str | None:
    """Procesa un evento de teclado. Devuelve QUIT si el jugador elige salir."""
    global _selected
    if event.type != pygame.KEYDOWN:
        return None

    if event.key == pygame.K_ESCAPE:
        toggle()
        return None

    if not _paused:
        return None

    if event.key in (pygame.K_UP, pygame.K_w):
        _selected = (_selected - 1) % len(MENU_OPTIONS)
    elif event.key in (pygame.K_DOWN, pygame.K_s):
        _selected = (_selected + 1) % len(MENU_OPTIONS)
    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        action = selected_option()
        if action == RESUME:
            resume()
        return action
    return None


def draw_menu(screen, font) -> None:
    width, height = screen.get_size()

    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    titulo = font.render("PAUSA", True, (255, 215, 0))
    screen.blit(titulo, titulo.get_rect(center=(width / 2, height / 2 - 80)))

    for i, (label, _) in enumerate(MENU_OPTIONS):
        color = (255, 255, 255) if i == _selected else (150, 150, 150)
        texto = font.render(f"> {label} <" if i == _selected else label, True, color)
        screen.blit(texto, texto.get_rect(center=(width / 2, height / 2 + i * 50)))
