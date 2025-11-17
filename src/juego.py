from config import *
from src.utils.diccionario_textos import *
import pygame, sys

class NewGame():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Final Sentence")
        self.pantalla =  pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()

        self.fondo = pygame.image.load("assets/images/gameplay_background.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))

        ANCHO_MAXIMO_FRASE = ANCHO - 500 # (1280 - 300 = 980px)

        # Obtenemos las frases largas originales
        frases_largas = selector()

        # Creamos la lista de frases formateadas
        self.frase = []
        for frase_original in frases_largas:
            renglones_formateados = self.formatear_frase(frase_original, ANCHO_MAXIMO_FRASE) #formatea
            self.frase.extend(renglones_formateados)# mete los renglones o el renglon original

        self.frase_activa = 0

        self.vivo = True 

        self.tambor = [False] * 6   # 6 cámaras EX VARIABLE self.cargador
        self.pos_tambor = 0         # posición actual del disparo
    
        self.cuenta_regresiva = 240 # en segundos : 4 minutos
        self.tiempo_inicio = pygame.time.get_ticks()
        tiempo_restante_formateado = "04:00"

        self.ronda = 0

        self.errores = 0
        self.errores_activos = [False] * 3  

        self.puntaje = 0

        self.input = ""
        self.indice = 0
        self.errores_posiciones = []  # Posiciones donde hubo error

        #Variables para animación de retroceso
        self.animando_retroceso = False
        self.tiempo_ultima_animacion = 0
        self.velocidad_retroceso = 45  # ms por letra (ajustable)
        self.indice_a_borrar = 0

    def dibujar_texto(self, texto: str, x: int, y: int):
        superficie = font_title.render(texto, True, colores["Belge"]) 
        rectangulo_texto = superficie.get_rect()
        rectangulo_texto = (x,y) 
        self.pantalla.blit(superficie, rectangulo_texto)

    def formatear_frase(self, frase_activa: str, ancho_maximo: int):

        lista_palabras = frase_activa.split()   
        frase = []
        linea = ""    

        for palabra in lista_palabras:
            if linea == "":
                linea_actual = palabra # Valida si la primer la primer palabra pertenece a la frase o no 
            else:
                linea_actual = linea + " " + palabra # En caso de tener una palabra la linea siguiente que debe de agregar la linea y la palabra siguiente

            ancho_frase = font_title.size(linea_actual)[0] # Guardo el valor del espacio que almacena la palabra

            if ancho_frase <= ancho_maximo: # Valido que mi frase recien almacenada supere mi limite especificado
                linea = linea_actual # Guardo la palabra formada ["HOLA COMO ESTAS"] y deja de estar en la segunda vuelta vacio la linea
            else:
                frase.append(linea) # En caso de que la frase supere el valor de mi ancho_maximo agrego la palabra en una lista aparte
                linea = palabra # La palabra que supero el ancho_maximo lo guardo en la variable linea para generar la siguiente linea

        if linea:
            frase.append(linea) # Agrego toda la frase completa divida según mi ancho_maximo

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
                    self.tiempo_ultima_animacion = ahora
                    self.indice_a_borrar -= 1  # borrar una letra por frame

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
            # Formatear el texto del timer
            minutos = tiempo_restante // 60
            segundos = tiempo_restante % 60
            texto_timer = f"{minutos:02}:{segundos:02}"
            self.dibujar_texto(texto_timer, 100, ALTO - 70)
            self.dibujar_tambor(1140, 100)
            self.dibujar_errores_activos(270, 170)

            # Comprobar si se acabó el tiempo
            if tiempo_restante <= 0:
                self.vivo = False # Marcamos el fin de la partida
                running = False # Salimos del bucle 'while True', volviendo al menú

            #self.dibujar_texto(f"Errores: {self.errores}", 100, 10)
            #self.dibujar_texto(f"Puntaje: {self.puntaje}", 1000, 10) por las dudas

            # Lógica para obtener y dibujar las 3 frases
            frase_actual_str = ""
            frase_siguiente_1 = ""
            frase_siguiente_2 = ""

            try:
                # Obtenemos la frase actual
                frase_actual_str = self.frase[self.frase_activa]
                
                # Obtenemos las siguientes (si existen)
                if self.frase_activa + 1 < len(self.frase):
                    frase_siguiente_1 = self.frase[self.frase_activa + 1]
                if self.frase_activa + 2 < len(self.frase):
                    frase_siguiente_2 = self.frase[self.frase_activa + 2]
            except IndexError:
                pass # Pasa si la lista de frases está vacía o si ganamos, falta logica cuando termina osea gané

            Y_ACTUAL = 225 # Coordenada Y para la frase activa
            X_INICIO = 250 # Coordenada X para la frase activa

            # Renderizar frase completa carácter por carácter
            x_actual = X_INICIO
            for i, char in enumerate(frase_actual_str):
                if i < self.indice:
                    # Ya tipeado correctamente
                    color = colores["Warm"]
                elif i in self.errores_posiciones:
                    # Error en esta posición
                    color = colores["Red"]
                else:
                    # Aún no tipeado
                    color = colores["Belge"]

                superficie_char = font_title.render(char, True, color)

                # Si es un error, dibujar rectángulo
                if i in self.errores_posiciones:
                    rect_char = superficie_char.get_rect(topleft=(x_actual, Y_ACTUAL))
                    pygame.draw.rect(self.pantalla, colores["Red"], rect_char, 2)

                self.pantalla.blit(superficie_char, (x_actual, Y_ACTUAL))
                x_actual += superficie_char.get_width()

            # Guardar el ancho total de la parte tipeada para el caret
            rect_tipeado_width = font_title.size(frase_actual_str[:self.indice])[0] if self.indice > 0 else 0

            parpadeo_caret = (pygame.time.get_ticks() // 500) % 2 == 0 # cada medio segundo 500ms, me fijo si es par

            if parpadeo_caret: #cada 500ms esto es True
                # posicion en x de la barrita que parpadea
                caret_x = X_INICIO + rect_tipeado_width
                
                # Usamos la altura de la fuente (en lugar de la del rect) para que se 
                # dibuje correctamente incluso cuando el input está vacío.
                font_height = font_title.get_height() 
                caret_y_start = Y_ACTUAL
                caret_y_end = Y_ACTUAL + font_height

                # Dibujar la línea (cursor) de color "Warm" y 2px de ancho
                pygame.draw.line(self.pantalla, colores["Warm"], (caret_x, caret_y_start), (caret_x, caret_y_end), 2)

            self.dibujar_texto(frase_siguiente_1, X_INICIO, Y_ACTUAL + 60) # 60 píxeles abajo
            self.dibujar_texto(frase_siguiente_2, X_INICIO, Y_ACTUAL + 120) # 120 píxeles abajo

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Si está animando para borrar, bloquear input
                if self.animando_retroceso:
                    continue

                if evento.type == pygame.KEYDOWN: # evento pulsacion de tecla

                    if not evento.unicode: # si no es un caracter imprimible crtl, shift
                        continue 

                    print(self.frase[self.frase_activa])
                    self.input += str(evento.unicode) # se escribe en el atributo la tecla
                    self.indice += 1 # indica el indice que estamos escribiendo
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


            pygame.display.update()
            self.reloj.tick(FPS)