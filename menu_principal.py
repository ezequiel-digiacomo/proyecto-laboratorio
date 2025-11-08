import pygame, sys
from config import *
from juego import ejecutar_juego


class Menu():
    def __init__(self):
        pygame.init()
        self.opciones= ["Jugar", "Opciones", "Salir"]
        self.reloj = pygame.time.Clock()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.area_opcion0 = None
        self.area_opcion1 = None
        self.area_opcion2 = None
        pygame.display.set_caption("Menu Principal")

    def dibujar_opciones(self):
        for i, texto in enumerate(self.opciones):
            superficie = font_title.render(texto, False, colores["Belge"])
            parametro = superficie.get_rect(topright=(ANCHO - 100, 200 + i * 80)) 
            self.pantalla.blit(superficie, parametro)

            if i == 0:
                self.area_opcion0 = parametro
            elif i == 1:
                self.area_opcion1 = parametro
            elif i == 2:
                self.area_opcion2 = parametro

            print(parametro)

    def dibujar_titulo(self, texto, x, y):
        superficie = font_title.render(texto, True, colores["Warm"]) 
        rectangulo_texto = superficie.get_rect()
        rectangulo_texto = (x,y) 
        self.pantalla.blit(superficie, rectangulo_texto)


    def ejecutar(self):
        while True:

            self.dibujar_titulo("Final Sentences", 450, 80)
            self.dibujar_opciones()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = evento.pos
                    if self.area_opcion0.collidepoint(click_pos): 
                        ejecutar_juego()
                        print(click_pos)
                
            pygame.display.update()
            self.reloj.tick(FPS)
