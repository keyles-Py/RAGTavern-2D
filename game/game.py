import pygame
import sys
from game.classes import Player, Gimli, Elena
from rag.rag import generate_rag_response

SCREEN_WIDTH = 1408
SCREEN_HEIGHT = 768
barra_pos = (100, 263)
caliz_pos = (1200, 610)

def run():
    pygame.init()

    pygame.display.set_caption("La Taberna del Drunken Dragon")

    screen =  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    wallpaper = pygame.image.load("game/assets/smallerBackground.png").convert()
    barra = pygame.image.load("game/assets/barra2.png").convert_alpha()

    clock = pygame.time.Clock()

    player = Player(SCREEN_WIDTH/2 - 50,SCREEN_HEIGHT-200)
    gimli = Gimli(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.25)
    elena = Elena(SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.35)

    show_hitboxes : bool = False
    talking_to_gimli :  bool = False
    talking_to_elena : bool = False

    obstaculos = [
        elena.rect,
        pygame.Rect(0, 270, SCREEN_WIDTH, 10),
        pygame.Rect(90, 0, 10, SCREEN_HEIGHT),  
        pygame.Rect(1320, 0, 10, SCREEN_HEIGHT),
        pygame.Rect(0, SCREEN_HEIGHT-1, SCREEN_WIDTH, 10),

        pygame.Rect(400, 600, 200, 100),  
        pygame.Rect(400, 450, 200, 100),  

        pygame.Rect(800, 600, 200, 100),  
        pygame.Rect(800, 450, 200, 100),  

        pygame.Rect(50, 600, 200, 100),  
        pygame.Rect(50, 450, 200, 100),  

        pygame.Rect(1200, 600, 200, 100),  
        pygame.Rect(1200, 450, 200, 100),  
    ]

    area_elena = elena.rect.inflate(100, 100)

    fuente_chat = pygame.font.SysFont("Arial", 20)
    texto_usuario = ""
    lineas_respuesta_npc = []
    nombre_npc = ""

    while True:
        clock.tick(60)

        area_gimli = gimli.rect.inflate(100, 100)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    if player.rect.colliderect(area_gimli):
                        talking_to_gimli = not talking_to_gimli
                        talking_to_elena = False 
                        texto_usuario = ""
                        lineas_respuesta_npc = []
                    elif player.rect.colliderect(area_elena):
                        talking_to_elena = not talking_to_elena
                        talking_to_gimli = False
                        texto_usuario = ""
                        lineas_respuesta_npc = []

                if event.key == pygame.K_1:
                    show_hitboxes = not show_hitboxes

            if talking_to_gimli or talking_to_elena:
                if event.type == pygame.TEXTINPUT:
                    if lineas_respuesta_npc:
                        lineas_respuesta_npc = []
                    texto_usuario += event.text
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        texto_usuario = texto_usuario[:-1]
                        
                    elif event.key == pygame.K_RETURN:
                        
                        if texto_usuario.strip():
                            nombre_npc = "Elena" if talking_to_elena else "Gimli" if talking_to_gimli else "Desconocido"
                            response = generate_rag_response(texto_usuario, nombre_npc)
                            respuesta_npc = response

                            lineas_respuesta_npc = []
                            palabras = respuesta_npc.split(' ')
                            linea_actual = ""
                            for palabra in palabras:
                                if len(linea_actual) + len(palabra) < 150:
                                    linea_actual += palabra + " "
                                else:
                                    lineas_respuesta_npc.append(linea_actual)
                                    linea_actual = palabra + " "
                            if linea_actual:
                                lineas_respuesta_npc.append(linea_actual)
                            
                        texto_usuario = ""

        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  
            dx = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
            dx = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:    
            dy = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  
            dy = 1  

        if not talking_to_elena and not talking_to_gimli:
            player.mover(dx, dy, obstaculos)
        gimli.actualizar_autonomo(talking_to_gimli)
        elena.actualizar_comportamiento(talking_to_elena)
        
        screen.blit(wallpaper,(0,0))
        screen.blit(gimli.image, gimli.rect)
        screen.blit(barra, barra_pos)
        screen.blit(elena.image, elena.rect)
        screen.blit(player.image, player.rect)

        if talking_to_gimli or talking_to_elena:
            caja_rect = pygame.Rect(50, SCREEN_HEIGHT - 180, SCREEN_WIDTH - 100, 150)
            pygame.draw.rect(screen, (0, 0, 0), caja_rect)
            pygame.draw.rect(screen, (255, 255, 255), caja_rect, 2) 

            y_offset = 35
            for i, linea in enumerate(lineas_respuesta_npc):
                texto_linea = f"[{nombre_npc}]: {linea}" if i == 0 else f"          {linea}"
                superficie_npc = fuente_chat.render(texto_linea, True, (0, 255, 255))
                screen.blit(superficie_npc, (caja_rect.x + 10, caja_rect.y + y_offset))
                y_offset += 25

            superficie_texto = fuente_chat.render(f"Tú: {texto_usuario}", True, (255, 255, 255))
            screen.blit(superficie_texto, (caja_rect.x + 10, caja_rect.y + 10))
        
        if show_hitboxes:
            pygame.draw.rect(screen, (255,0,0), player.rect, 2)
            pygame.draw.rect(screen, (0,0,255), gimli.rect, 2)
            pygame.draw.rect(screen, (0,0,255), elena.rect, 2)
            pygame.draw.rect(screen, (128,0,128), area_elena, 2)
            pygame.draw.rect(screen, (128,0,128), area_gimli, 2)
            for i in range(len(obstaculos)):
                pygame.draw.rect(screen, (255,0,0), obstaculos[i], 2)

        pygame.display.flip()

run()