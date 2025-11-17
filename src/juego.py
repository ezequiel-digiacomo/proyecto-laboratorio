from config import *
from src.utils.diccionario_textos import *
import pygame, sys, random, os

class NewGame():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Final Sentence")
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()

        self.fondo = pygame.image.load("assets/images/gameplay_background.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))

        ANCHO_MAXIMO_FRASE = ANCHO - 500 # (1280 - 300 = 980px)
        # Musica del juego 
        pygame.mixer.music.load("assets/sounds/musica_juego.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # loop infinito

        # Sonidos de tipeo 
        ruta_base = os.path.join("assets", "sfx")
        self.sonidos_teclas = []
        for i in range(1, 9):  # del 1 al 8
            ruta = os.path.join(ruta_base, f"typewriter{i}.wav")
            if os.path.exists(ruta):
                self.sonidos_teclas.append(pygame.mixer.Sound(ruta))
        for s in self.sonidos_teclas:
            s.set_volume(0.4)

        ANCHO_MAXIMO_FRASE = ANCHO - 500
        frases_largas = selector()

        ruta_error = os.path.join("assets", "sfx", "error_sound.wav")
        self.error_sound = pygame.mixer.Sound(ruta_error)
        self.error_sound.set_volume(0.4)

        self.frase = []
        for frase_original in frases_largas:
            renglones_formateados = self.formatear_frase(frase_original, ANCHO_MAXIMO_FRASE)
            self.frase.extend(renglones_formateados)

        self.frase_activa = 0

        self.vivo = True 

        self.tambor = [False] * 6   # 6 cámaras EX VARIABLE self.cargador
        self.pos_tambor = 0         # posición actual del disparo
    
        self.cuenta_regresiva = 240 # en segundos : 4 minutos
        self.cargador = [False] * 6
        
        self.tiempo_inicio = pygame.time.get_ticks()
        self.ronda = 0
        self.errores = 0
        self.errores_activos = [False] * 3
        self.puntaje = 0
        self.input = ""
        self.indice = 0
        self.errores_posiciones = []

        #Variables para animación de retroceso
        self.animando_retroceso = False
        self.tiempo_ultima_animacion = 0
        self.velocidad_retroceso = 45  # ms por letra (ajustable)
        self.indice_a_borrar = 0

    def dibujar_texto(self, texto: str, x: int, y: int):
        superficie = font_title.render(texto, True, colores["Belge"])
        self.pantalla.blit(superficie, (x, y))

    def formatear_frase(self, frase_activa: str, ancho_maximo: int):
        lista_palabras = frase_activa.split()
        frase = []
        linea = ""
        for palabra in lista_palabras:
            linea_actual = palabra if linea == "" else linea + " " + palabra
            ancho_frase = font_title.size(linea_actual)[0]
            if ancho_frase <= ancho_maximo:
                linea = linea_actual
            else:
                frase.append(linea)
                linea = palabra
        if linea:
            frase.append(linea)
        return frase

    def cargar_disparar(self):
        # cargar bala random
        cams_vacias = [i for i, c in enumerate(self.tambor) if not c]
        if cams_vacias:
            self.tambor[random.choice(cams_vacias)] = True

        # avanzar tambor una posición
        self.pos_tambor = (self.pos_tambor + 1) % 6

        bala = self.tambor[self.pos_tambor]

        if bala:
            self.tambor[self.pos_tambor] = False

        return not bala
    
    def dibujar_tambor(self, x, y, radio=18):
        # Posiciones circulares reales (hexágono) para el tambor
        posiciones = [
            (0, -40),       # arriba
            (35, -20),      # arriba derecha
            (35, 20),       # abajo derecha
            (0, 40),        # abajo
            (-35, 20),      # abajo izquierda
            (-35, -20),     # arriba izquierda
        ]

        for i, (dx, dy) in enumerate(posiciones):
            cx = x + dx
            cy = y + dy

            if self.tambor[i]:
                color = (200, 20, 20)  # rojo = bala
            else:
                color = (220, 220, 220)  # vacío

            pygame.draw.circle(self.pantalla, color, (cx, cy), radio)

            # Cámara activa (la que dispara)
            if i == self.pos_tambor:
                pygame.draw.circle(self.pantalla, (255, 215, 0), (cx, cy), radio + 4, 2)  # bordecito

    def dibujar_errores_activos(self, x, y, radio=10):
        separacion = 35  # entre los circulitos

        for i in range(3):
            cx = x + i * separacion
            cy = y

            if self.errores_activos[i]:
                color = (200, 40, 40)  # rojo = error marcado
            else:
                color = (180, 180, 180)  # gris vacío

            pygame.draw.circle(self.pantalla, color, (cx, cy), radio)

    def ejecutar_juego(self):
        running = True
        while running:
            # Apartado de animación de retroceso
            if self.animando_retroceso:
                ahora = pygame.time.get_ticks()

                if ahora - self.tiempo_ultima_animacion > self.velocidad_retroceso:

                    #Sonido de Error:
                    if ahora - self.tiempo_ultima_animacion > self.velocidad_retroceso:
                        self.error_sound.play(maxtime=80)
                        self.tiempo_ultima_animacion = ahora
                        self.indice_a_borrar -= 1

                    if self.indice_a_borrar < 0:
                        # Animación terminada
                        self.animando_retroceso = False
                        self.input = ""
                        self.indice = 0
                        self.errores_posiciones = []
                    else:
                        self.indice = self.indice_a_borrar 
                        self.input = self.input[:self.indice]


            self.pantalla.blit(self.fondo, (0, 0))
            # Calcular tiempo
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio) // 1000
            tiempo_restante = self.cuenta_regresiva - tiempo_transcurrido
            minutos = tiempo_restante // 60
            segundos = tiempo_restante % 60
            texto_timer = f"{minutos:02}:{segundos:02}"
            self.dibujar_texto(texto_timer, 100, ALTO - 70)
            self.dibujar_tambor(1140, 100)
            self.dibujar_errores_activos(270, 170)

            # Comprobar si se acabó el tiempo
            if tiempo_restante <= 0:
                self.vivo = False
                running = False

            #self.dibujar_texto(f"Errores: {self.errores}", 100, 10)
            #self.dibujar_texto(f"Puntaje: {self.puntaje}", 1000, 10) por las dudas

            # Frases actuales
            frase_actual_str = ""
            frase_siguiente_1 = ""
            frase_siguiente_2 = ""
            try:
                frase_actual_str = self.frase[self.frase_activa]
                if self.frase_activa + 1 < len(self.frase):
                    frase_siguiente_1 = self.frase[self.frase_activa + 1]
                if self.frase_activa + 2 < len(self.frase):
                    frase_siguiente_2 = self.frase[self.frase_activa + 2]
            except IndexError:
                pass

            Y_ACTUAL = 225
            X_INICIO = 250
            x_actual = X_INICIO
            for i, char in enumerate(frase_actual_str):
                if i < self.indice:
                    color = colores["Warm"]
                elif i in self.errores_posiciones:
                    color = colores["Red"]
                else:
                    color = colores["Belge"]

                superficie_char = font_title.render(char, True, color)
                if i in self.errores_posiciones:
                    rect_char = superficie_char.get_rect(topleft=(x_actual, Y_ACTUAL))
                    pygame.draw.rect(self.pantalla, colores["Red"], rect_char, 2)
                self.pantalla.blit(superficie_char, (x_actual, Y_ACTUAL))
                x_actual += superficie_char.get_width()

            rect_tipeado_width = font_title.size(frase_actual_str[:self.indice])[0] if self.indice > 0 else 0
            parpadeo_caret = (pygame.time.get_ticks() // 500) % 2 == 0
            if parpadeo_caret:
                caret_x = X_INICIO + rect_tipeado_width
                font_height = font_title.get_height()
                pygame.draw.line(self.pantalla, colores["Warm"],
                                 (caret_x, Y_ACTUAL),
                                 (caret_x, Y_ACTUAL + font_height), 2)

            self.dibujar_texto(frase_siguiente_1, X_INICIO, Y_ACTUAL + 60)
            self.dibujar_texto(frase_siguiente_2, X_INICIO, Y_ACTUAL + 120)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Si está animando para borrar, bloquear input
                if self.animando_retroceso:
                    continue

 
                if evento.type == pygame.KEYDOWN: # evento pulsacion de tecla
                    if not evento.unicode:
                        continue

                    # Sonido de tipeo
                    if self.sonidos_teclas:
                        random.choice(self.sonidos_teclas).play()

                    print(self.frase[self.frase_activa])
                    self.input += str(evento.unicode)
                    self.indice += 1
                    print(self.input)

                    if not self.input[0:self.indice] == self.frase[self.frase_activa][0:self.indice]: # si la frase hasta ahora conincide
                        # Error: marca posición y acumula errores
                        if (self.indice - 1) not in self.errores_posiciones:
                            self.errores_posiciones.append(self.indice - 1) # Error del rojo
                        self.animando_retroceso = True
                        self.indice_a_borrar = self.indice  # Retrocede desde donde ibas
                        self.tiempo_ultima_animacion = pygame.time.get_ticks()
                        self.input = ""
                        self.indice = 0
                        # Marcar visualmente el error en errores_activos
                        slot = (self.errores % 3)  # 0, 1, 2 slot de errores
                        self.errores_activos[slot] = True

                        self.errores += 1

                        # Cada 3 errores -> disparo
                        if self.errores % 3 == 0:
                            running = self.cargar_disparar()
                            self.errores_activos = [False] * 3  # reset visual

                if self.input == self.frase[self.frase_activa]: # si la frase completa coincide
                    self.frase_activa += 1 # paso a la linea que sigue
                    self.input = "" # reincio input del usuario
                    self.indice = 0 # reinicio indice del input del usuario
                    self.errores_posiciones = []  # Limpia errores al pasar de línea

                if self.input == self.frase[self.frase_activa]:
                    self.frase_activa += 1
                    self.input = ""
                    self.indice = 0
                    self.errores_posiciones = []

            pygame.display.update()
            self.reloj.tick(FPS)
