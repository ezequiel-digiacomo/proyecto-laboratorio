import pygame
from config import *

class ModalSalir:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.activo = False
        self.ancho_modal = 600
        self.alto_modal = 200
        self.x = (ANCHO - self.ancho_modal) // 2
        self.y = (ALTO - self.alto_modal) // 2
        self.fondo_oscuro = pygame.Surface((ANCHO, ALTO))
        self.fondo_oscuro.set_alpha(180)
        self.fondo_oscuro.fill((0, 0, 0))
        y_botones = self.y + self.alto_modal - 60
        espacio = 100
        centro_x = self.x + self.ancho_modal // 2
        self.boton_cancelar = pygame.Rect(centro_x - 120 - espacio // 2, y_botones, 120, 40)
        self.boton_salir = pygame.Rect(centro_x + espacio // 2, y_botones, 120, 40)

    def abrir(self):
        self.activo = True

    def cerrar(self):
        self.activo = False

    def manejar_eventos(self, evento):
        if not self.activo:
            return None

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.cerrar()
            return 'cancelar'

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.boton_cancelar.collidepoint(evento.pos):
                self.cerrar()
                return 'cancelar'
            elif self.boton_salir.collidepoint(evento.pos):
                self.cerrar()
                return 'salir'

        return None

    def dibujar(self):
        if not self.activo:
            return

        self.pantalla.blit(self.fondo_oscuro, (0, 0))

        rect_modal = (self.x, self.y, self.ancho_modal, self.alto_modal)
        pygame.draw.rect(self.pantalla, colores["Warm"], rect_modal)
        pygame.draw.rect(self.pantalla, colores["Maroon"], rect_modal, 3)

        superficie_titulo = font_title.render("¿Seguro que desea Salir?", True, colores["Maroon"])
        self.pantalla.blit(superficie_titulo, superficie_titulo.get_rect(center=(self.x + self.ancho_modal // 2, self.y + 60)))

        pygame.draw.rect(self.pantalla, colores["Belge"], self.boton_cancelar)
        pygame.draw.rect(self.pantalla, colores["Maroon"], self.boton_cancelar, 2)
        superficie_cancelar = font_text.render("CANCELAR", True, colores["Maroon"])
        self.pantalla.blit(superficie_cancelar, superficie_cancelar.get_rect(center=self.boton_cancelar.center))

        pygame.draw.rect(self.pantalla, colores["Maroon"], self.boton_salir)
        pygame.draw.rect(self.pantalla, colores["Warm"], self.boton_salir, 2)
        superficie_salir = font_text.render("SALIR", True, colores["Warm"])
        self.pantalla.blit(superficie_salir, superficie_salir.get_rect(center=self.boton_salir.center))
