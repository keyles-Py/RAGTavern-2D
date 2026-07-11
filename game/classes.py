import pygame
import random

class Spritesheet:
    def __init__(self, archivo_path):
        self.sheet = pygame.image.load(archivo_path).convert_alpha()

    def obtener_imagen(self, columna, fila, ancho, alto):
        x = columna * ancho
        y = fila * alto
        
        imagen = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        imagen.blit(self.sheet, (0, 0), (x, y, ancho, alto))
        return imagen

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        sprite_util = Spritesheet("game/assets/finale_player.png")
        
        self.ancho_frame = 90
        self.alto_frame = 150

        self.animaciones = {
            "idle_back": [],
            "idle_front": [],
            "walk_down": [],
            "walk_up": [],
            "walk_right": [],
            "walk_left": []
        }

        self.animaciones["walk_down"].append(sprite_util.obtener_imagen(0, 0, self.ancho_frame, self.alto_frame))
        self.animaciones["walk_down"].append(sprite_util.obtener_imagen(1, 0, self.ancho_frame, self.alto_frame))

        self.animaciones["walk_up"].append(sprite_util.obtener_imagen(2, 0, self.ancho_frame, self.alto_frame))
        self.animaciones["walk_up"].append(sprite_util.obtener_imagen(3, 0, self.ancho_frame, self.alto_frame))

        self.animaciones["walk_right"].append(sprite_util.obtener_imagen(4, 0, self.ancho_frame, self.alto_frame))

        self.animaciones["idle_back"].append(sprite_util.obtener_imagen(0, 1, self.ancho_frame, self.alto_frame))

        self.animaciones["idle_front"].append(sprite_util.obtener_imagen(1, 1, self.ancho_frame, self.alto_frame))

        self.animaciones["walk_right"].append(sprite_util.obtener_imagen(2, 1, self.ancho_frame, self.alto_frame))

        self.animaciones["walk_left"].append(sprite_util.obtener_imagen(3, 1, self.ancho_frame, self.alto_frame))
        self.animaciones["walk_left"].append(sprite_util.obtener_imagen(4, 1, self.ancho_frame, self.alto_frame))


        self.estado_actual = "idle_front"
        self.current_frame = 0
        self.image = self.animaciones[self.estado_actual][self.current_frame]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = 4
        
        self.ultimo_cambio = pygame.time.get_ticks()
        self.velocidad_animacion = 200 

    def mover(self, dx, dy, lista_obstaculos):
        if dx > 0:
            self.estado_actual = "walk_right"
        elif dx < 0:
            self.estado_actual = "walk_left"
        elif dy > 0:
            self.estado_actual = "walk_down"
        elif dy < 0:
            self.estado_actual = "walk_up"
        else:
            if self.estado_actual == "walk_up":
                self.estado_actual = "idle_back"
            elif self.estado_actual in ["walk_down", "walk_right", "walk_left"]:
                self.estado_actual = "idle_front"

        if dx != 0:
            self.mover_eje_x(dx, lista_obstaculos)
        if dy != 0:
            self.mover_eje_y(dy, lista_obstaculos)

        self.actualizar_animacion()

    def mover_eje_x(self, dx, lista_obstaculos):
        # Solo alteramos X
        self.rect.x += dx * self.velocidad
        for obstaculo in lista_obstaculos:
            if self.rect.colliderect(obstaculo):
                if dx > 0:  # Moviéndose a la derecha
                    self.rect.right = obstaculo.left
                if dx < 0:  # Moviéndose a la izquierda
                    self.rect.left = obstaculo.right

    def mover_eje_y(self, dy, lista_obstaculos):
        # Solo alteramos Y
        self.rect.y += dy * self.velocidad
        for obstaculo in lista_obstaculos:
            if self.rect.colliderect(obstaculo):
                if dy > 0:  # Moviéndose hacia abajo
                    self.rect.bottom = obstaculo.top
                if dy < 0:  # Moviéndose hacia arriba
                    self.rect.top = obstaculo.bottom

    def actualizar_animacion(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_cambio > self.velocidad_animacion:
            self.current_frame = (self.current_frame + 1) % len(self.animaciones[self.estado_actual])
            self.image = self.animaciones[self.estado_actual][self.current_frame]
            self.ultimo_cambio = tiempo_actual

class Gimli(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        sprite_util = Spritesheet("game/assets/tabernero2.png")

        self.limite_izquierdo = 120
        self.limite_derecho = 1200

        self.ancho_frame = 90
        self.alto_frame = 150

        self.animaciones = {
            "idle_back": [],
            "idle_front": [],
            "walk_right": [],
            "walk_left": []
        }

        self.animaciones["idle_back"].append(sprite_util.obtener_imagen(1, 0, self.ancho_frame, self.alto_frame))

        self.animaciones["idle_front"].append(sprite_util.obtener_imagen(0, 0, self.ancho_frame, self.alto_frame))

        self.animaciones["walk_right"].append(sprite_util.obtener_imagen(2, 0, self.ancho_frame, self.alto_frame))

        self.animaciones["walk_right"].append(sprite_util.obtener_imagen(2, 1, self.ancho_frame, self.alto_frame))

        self.animaciones["walk_left"].append(sprite_util.obtener_imagen(0, 1, self.ancho_frame, self.alto_frame))
        self.animaciones["walk_left"].append(sprite_util.obtener_imagen(1, 1, self.ancho_frame, self.alto_frame))


        self.estado_actual = "idle_front"
        self.current_frame = 0
        self.image = self.animaciones[self.estado_actual][self.current_frame]

        self.dx = 0
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = 2
        
        self.ultimo_cambio = pygame.time.get_ticks()
        self.velocidad_animacion = 200 

        self.ultimo_cambio_decision = pygame.time.get_ticks()
        self.cooldown_decision = random.randint(1500, 3500)

    def pensar_comportamiento(self):
        
        tiempo_actual = pygame.time.get_ticks()
        
        if tiempo_actual - self.ultimo_cambio_decision > self.cooldown_decision:
            acciones = ["idle_front", "idle_back", "walk_left", "walk_right"]
            self.estado_actual = random.choice(acciones)
            
            if self.estado_actual == "walk_left":
                self.dx = -1
            elif self.estado_actual == "walk_right":
                self.dx = 1
            else:
                self.dx = 0 

            self.ultimo_cambio_decision = tiempo_actual
            self.cooldown_decision = random.randint(1500, 4000)

    def actualizar_autonomo(self, is_talking=False):
        if is_talking:
            self.estado_actual = "idle_front"
            self.dx = 0
            self.ultimo_cambio_decision = pygame.time.get_ticks()
        else:
            self.pensar_comportamiento()

        self.rect.x += self.dx * self.velocidad

        if self.rect.x < self.limite_izquierdo:
            self.rect.x = self.limite_izquierdo
            self.estado_actual = "idle_front"
            self.dx = 0
        elif self.rect.x > self.limite_derecho:
            self.rect.x = self.limite_derecho
            self.estado_actual = "idle_front"
            self.dx = 0

        self.actualizar_animacion()


    def actualizar_animacion(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_cambio > self.velocidad_animacion:
            self.current_frame = (self.current_frame + 1) % len(self.animaciones[self.estado_actual])
            self.image = self.animaciones[self.estado_actual][self.current_frame]
            self.ultimo_cambio = tiempo_actual

class Elena(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        sprite_util = Spritesheet("game/assets/elena_spritesheet.png")
        
        self.ancho_frame = 90
        self.alto_frame = 150

        self.animaciones = {
            "idle_front": [],
            "playing": []
        }

        self.animaciones["idle_front"].append(sprite_util.obtener_imagen(0, 0, self.ancho_frame, self.alto_frame))

        self.animaciones["playing"].append(sprite_util.obtener_imagen(0, 1, self.ancho_frame, self.alto_frame))
        self.animaciones["playing"].append(sprite_util.obtener_imagen(1, 0, self.ancho_frame, self.alto_frame))
        self.animaciones["playing"].append(sprite_util.obtener_imagen(1, 1, self.ancho_frame, self.alto_frame))

        self.estado_actual = "idle_front"
        self.current_frame = 0
        self.image = self.animaciones[self.estado_actual][self.current_frame]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.ultimo_cambio_frame = pygame.time.get_ticks()
        self.velocidad_animacion = 900
        self.ultimo_cambio_estado = pygame.time.get_ticks()
        self.duracion_estado_actual = random.randint(3000, 6000)

    def actualizar_comportamiento(self, is_talking=False):
        if is_talking:
            self.estado_actual = "idle_front"
            self.ultimo_cambio_estado = pygame.time.get_ticks()
        else:
            tiempo_actual = pygame.time.get_ticks()
        
            if tiempo_actual - self.ultimo_cambio_estado > self.duracion_estado_actual:
                self.ultimo_cambio_estado = tiempo_actual
                self.current_frame = 0  
                
                if self.estado_actual == "idle_front":
                    self.estado_actual = "playing"
                    self.duracion_estado_actual = random.randint(4000, 8000)
                else:
                    self.estado_actual = "idle_front"
                    self.duracion_estado_actual = random.randint(5000, 10000)
        self.actualizar_animacion()

    def actualizar_animacion(self):
        tiempo_actual = pygame.time.get_ticks()
        
        if tiempo_actual - self.ultimo_cambio_frame > self.velocidad_animacion:
            self.current_frame = (self.current_frame + 1) % len(self.animaciones[self.estado_actual])
            self.image = self.animaciones[self.estado_actual][self.current_frame]
            self.ultimo_cambio_frame = tiempo_actual