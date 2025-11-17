from config import *
from src.utils.diccionario_textos import *
import pygame, sys, random, os

class NewGame():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Final Sentence")
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()

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

        self.frase = []
        for frase_original in frases_largas:
            renglones_formateados = self.formatear_frase(frase_original, ANCHO_MAXIMO_FRASE)
            self.frase.extend(renglones_formateados)

        self.frase_activa = 0
        self.cargador = [False] * 6
        self.vivo = True
        self.cuenta_regresiva = 240
        self.tiempo_inicio = pygame.time.get_ticks()
        self.ronda = 0
        self.errores = 0
        self.errores_activos = [False] * 3
        self.puntaje = 0
        self.input = ""
        self.indice = 0
        self.errores_posiciones = []

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
        for i in range(len(self.cargador)):
            if self.cargador[i] is False:
                self.cargador[i] = True
                break
        bala_actual = random.choice(self.cargador)
        self.errores_activos = [False] * 3
        if bala_actual == True:
            print(f"estado de bala {bala_actual}")
        return not bala_actual

    def ejecutar_juego(self):
        running = True
        while running:
            self.pantalla.fill(colores["Negro"])

            # Calcular tiempo
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio) // 1000
            tiempo_restante = self.cuenta_regresiva - tiempo_transcurrido
            minutos = tiempo_restante // 60
            segundos = tiempo_restante % 60
            texto_timer = f"{minutos:02}:{segundos:02}"
            self.dibujar_texto(texto_timer, 100, ALTO - 70)

            # Comprobar si se acabó el tiempo
            if tiempo_restante <= 0:
                self.vivo = False
                running = False

            self.dibujar_texto(f"Errores: {self.errores}", 100, 10)
            self.dibujar_texto(f"Puntaje: {self.puntaje}", 1000, 10)

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

                if evento.type == pygame.KEYDOWN:
                    if not evento.unicode:
                        continue

                    # Sonido de tipeo
                    if self.sonidos_teclas:
                        random.choice(self.sonidos_teclas).play()

                    print(self.frase[self.frase_activa])
                    self.input += str(evento.unicode)
                    self.indice += 1
                    print(self.input)

                    if not self.input[0:self.indice] == self.frase[self.frase_activa][0:self.indice]:
                        if (self.indice - 1) not in self.errores_posiciones:
                            self.errores_posiciones.append(self.indice - 1)
                        self.input = ""
                        self.indice = 0
                        self.errores += 1
                        if self.errores % 3 == 0:
                            running = self.cargar_disparar()

                if self.input == self.frase[self.frase_activa]:
                    self.frase_activa += 1
                    self.input = ""
                    self.indice = 0
                    self.errores_posiciones = []

            pygame.display.update()
            self.reloj.tick(FPS)
