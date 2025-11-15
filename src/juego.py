"""
Tarea Pendiente juego.py: 

    - Realizar funciones: Puntaje y Reinicio de partida
    - Mejorar la generación de texto en cuanto lo visual
    - Limpiar el bucle de ejecución haciendo más legible el código
    - Implementar: Sónidos e imagenes al juego 
    - Comprobación: Verificar que la función generador_frases ubicada en la carpeta palabras.py funcione

"""


from config import *
from src.utils.diccionario_textos import *
import pygame, sys

class NewGame():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Final Sentence")
        self.pantalla =  pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()

        self.frase = selector()
        self.frase_activa = 0

        self.cargador = [False] * 6 # CAPACIDAD DEL CARGADOR DE LA RULETA
        self.vivo = True 
    
        self.cuenta_regresiva = 240 # en segundos : 4 minutos
        self.tiempo_inicio = pygame.time.get_ticks()
        tiempo_restante_formateado = "04:00"

        self.ronda = 0

        self.errores = 0
        self.errores_activos = [False] * 3 # 

        self.puntaje = 0

        self.input = ""
        self.indice = 0
    
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
            # --- AÑADIR ESTE BLOQUE PARA EL TIMER ---
            # Calcular tiempo
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio) // 1000
            tiempo_restante = self.cuenta_regresiva - tiempo_transcurrido

            # Comprobar si se acabó el tiempo
            if tiempo_restante <= 0:
                self.vivo = False # Marcamos el fin de la partida
                break # Salimos del bucle 'while True', volviendo al menú

            # Formatear el texto del timer
            minutos = tiempo_restante // 60
            segundos = tiempo_restante % 60
            texto_timer = f"{minutos:02}:{segundos:02}"
            
            # Dibujar el timer (abajo a la izquierda)
            self.dibujar_texto(texto_timer, 100, ALTO - 70)
            # --- FIN DEL BLOQUE AÑADIDO ---

            self.dibujar_texto(f"Errores: {self.errores}", 100, 10)
            self.dibujar_texto(f"Puntaje: {self.puntaje}", 1000, 10)

            # --- AÑADIDO ---
            # 2. Lógica para obtener y dibujar las 3 frases
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
                pass # Pasa si la lista de frases está vacía o si ganamos

            # --- DIBUJAR LÍNEA ACTUAL (con progreso) ---
            Y_ACTUAL = 200 # Coordenada Y para la línea principal
            X_INICIO = 150
            
            # 2a. Parte ya tipeada (en color "Warm")
            texto_tipeado = self.input
            superficie_tipeada = font_title.render(texto_tipeado, True, colores["Warm"])
            rect_tipeado = superficie_tipeada.get_rect(topleft=(X_INICIO, Y_ACTUAL))
            self.pantalla.blit(superficie_tipeada, rect_tipeado)
            
            # 2b. Parte restante (en color "Belge")
            texto_restante = frase_actual_str[self.indice:]
            superficie_restante = font_title.render(texto_restante, True, colores["Belge"])
            x_restante = X_INICIO + rect_tipeado.width # La ponemos justo después de la parte tipeada
            rect_restante = superficie_restante.get_rect(topleft=(x_restante, Y_ACTUAL))
            self.pantalla.blit(superficie_restante, rect_restante)


            # --- DIBUJAR LÍNEAS SIGUIENTES ---
            # (Usamos tu función dibujar_texto, que usa la fuente grande y color Belge)
            self.dibujar_texto(frase_siguiente_1, X_INICIO, Y_ACTUAL + 60) # 60 píxeles abajo
            self.dibujar_texto(frase_siguiente_2, X_INICIO, Y_ACTUAL + 120) # 120 píxeles abajo
            # --- FIN DEL BLOQUE AÑADIDO ---

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN: 

                    if not evento.unicode:
                        continue 

                    print(self.frase[self.frase_activa])
                    self.input += str(evento.unicode)
                    self.indice += 1
                    print(self.input)
                    if self.input[0:self.indice] == self.frase[self.frase_activa][0:self.indice]:
                        continue
                    else:
                        self.input = ""
                        self.indice = 0
                        self.errores += 1
                        if self.errores % 3 == 0 :
                            running = self.cargar_disparar()
                if self.input == self.frase[self.frase_activa]:
                    self.frase_activa += 1
                    self.input = ""
                    self.indice = 0


            pygame.display.update()
            self.reloj.tick(FPS)