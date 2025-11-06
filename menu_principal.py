import pygame, sys
from config import *

class Menu():
    def __init__(self):
        pygame.init()
        self.opciones= ["Jugar", "Opciones", "Salir"]
        self.reloj = pygame.time.Clock()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Menu Principal")

    def dibujar_opciones(self):
        for i, texto in enumerate(self.opciones):
            superficie = font_title.render(texto, False, colores["Belge"])
            parametro = superficie.get_rect(topright=(ANCHO - 100, 200 + i * 80)) #mejorar
            self.pantalla.blit(superficie, parametro)
    
    def dibujar_titulo(self, texto, x, y):
        superficie = font_title.render(texto, True, colores["Warm"]) #Convierte el texto en 'superficie'
        rectangulo_texto = superficie.get_rect() #Obtengo las dimensiones de donde voy a poner el texto en pantall
        rectangulo_texto = (x,y) #Le digo donde poner el texto
        self.pantalla.blit(superficie, rectangulo_texto) #Lo coloco


    def ejecutar(self):
        while True:

            self.dibujar_titulo("Final Sentences", 450, 80)
            self.dibujar_opciones()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.reloj.tick(FPS)

