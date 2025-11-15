import pygame, random
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
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) #Para que desaparezca el cursor de mano

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
    
    def es_hover(self, rect):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return rect.collidepoint(mouse_x, mouse_y)
    
    def oscurecer(self, color, factor=40):
        r = max(color[0] - factor, 0)
        g = max(color[1] - factor, 0)
        b = max(color[2] - factor, 0)
        return (r, g, b)


    def dibujar(self):
        if not self.activo:
            return

        self.pantalla.blit(self.fondo_oscuro, (0, 0))

        rect_modal = (self.x, self.y, self.ancho_modal, self.alto_modal)
        pygame.draw.rect(self.pantalla, colores["Negro"], rect_modal)
        pygame.draw.rect(self.pantalla, colores["BurnedEdge"], rect_modal, 3)

        superficie_titulo = font_title.render("¿Seguro que desea Salir?", True, colores["Belge"])
        self.pantalla.blit(superficie_titulo, superficie_titulo.get_rect(center=(self.x + self.ancho_modal // 2, self.y + 60)))

        # ========= HOVER Y CURSOR =========

        # if hover en cualquiera -> cursor de mano
        if self.es_hover(self.boton_cancelar) or self.es_hover(self.boton_salir):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Botón "Cancelar" con efecto hover
        color_cancelar = colores["Belge"]
        escala_cancelar = 1.0
        if self.es_hover(self.boton_cancelar):
            color_cancelar = colores["Warm"]
            escala_cancelar = 1.05

        superficie_cancelar = font_button_modal.render("Cancelar", True, color_cancelar)
        if escala_cancelar != 1.0:
            ancho = int(superficie_cancelar.get_width() * escala_cancelar)
            alto = int(superficie_cancelar.get_height() * escala_cancelar)
            superficie_cancelar = pygame.transform.smoothscale(superficie_cancelar, (ancho, alto))

        rect_cancelar = superficie_cancelar.get_rect(center=self.boton_cancelar.center)
        self.pantalla.blit(superficie_cancelar, rect_cancelar)

        if self.es_hover(self.boton_cancelar):
            start = (rect_cancelar.left, rect_cancelar.bottom + 5)
            end = (rect_cancelar.right, rect_cancelar.bottom + 5)
            pygame.draw.line(self.pantalla, color_cancelar, start, end, 3)

        # Botón "Salir" con efecto hover
        color_salir = colores["Belge"]
        escala_salir = 1.0
        if self.es_hover(self.boton_salir):
            color_salir = colores["Warm"]
            escala_salir = 1.05

        superficie_salir = font_button_modal.render("Salir", True, color_salir)
        if escala_salir != 1.0:
            ancho = int(superficie_salir.get_width() * escala_salir)
            alto = int(superficie_salir.get_height() * escala_salir)
            superficie_salir = pygame.transform.smoothscale(superficie_salir, (ancho, alto))

        rect_salir = superficie_salir.get_rect(center=self.boton_salir.center)
        self.pantalla.blit(superficie_salir, rect_salir)

        if self.es_hover(self.boton_salir):
            start = (rect_salir.left, rect_salir.bottom + 5)
            end = (rect_salir.right, rect_salir.bottom + 5)
            pygame.draw.line(self.pantalla, color_salir, start, end, 3)