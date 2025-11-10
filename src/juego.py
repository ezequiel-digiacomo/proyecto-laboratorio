"""
Tarea Pendiente juego.py: 

    - Realizar funciones: Puntaje y Reinicio de partida
    - Mejorar la generación de texto en cuanto lo visual
    - Limpiar el bucle de ejecución haciendo más legible el código
    - Implementar: Sónidos e imagenes al juego 
    - Comprobación: Verificar que la función generador_frases ubicada en la carpeta palabras.py funcione

"""

from config import *
from utils.diccionario_textos import *
import pygame, sys

class NewGame():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Final Sentence")
        self.pantalla =  pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()
        self.frase = obtener_frases_api("https://api.breakingbadquotes.xyz/v1/quotes/20")
        self.frase_activa = self.frase[0]
        self.ronda = 0
        self.errores = 0
        self.puntaje = 0
    
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

                
    def ejecutar_juego(self):
        while True:

            self.dibujar_texto(f"Errores: {self.errores}", 100, 10)
            self.dibujar_texto(f"Puntaje: {self.puntaje}", 1000, 10)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
     
            lineas = self.formatear_frase(self.frase_activa, 500)
            
            y = 150
            for linea in lineas:
                ancho_linea = font_title.size(linea)[0]
                x = (ANCHO - ancho_linea) // 2 
    
                self.dibujar_texto(linea, x, y)
                y += 40

            pygame.display.update()
            self.reloj.tick(FPS)
