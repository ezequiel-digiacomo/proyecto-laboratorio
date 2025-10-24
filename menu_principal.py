import pygame, sys
from final_sentence import ejecutar_juego   #  importa el juego

ANCHO = 900
ALTO = 500
FPS = 60

class MenuPrincipal:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Menu Principal - Proyecto Laboratorio 2")
        self.reloj = pygame.time.Clock()

        # --- Fuentes ---
        self.fuente_titulo = pygame.font.SysFont("arial", 48, bold=True)
        self.fuente_boton = pygame.font.SysFont("arial", 30)

        # --- Colores ---
        self.color_fondo = (20, 20, 30)
        self.color_titulo = (255, 255, 255)
        self.color_boton = (120, 200, 255)
        self.color_boton_hover = (180, 240, 255)

    def centrar_titulo(self, texto, fuente, color, y):
        superficie_titulo = fuente.render(texto, True, color)
        ubicacion_titulo = superficie_titulo.get_rect(center=(ANCHO // 2, y))
        self.pantalla.blit(superficie_titulo, ubicacion_titulo)

    def dibujar_boton(self, texto, y, posicion_mouse):
        ubicacion_boton = pygame.Rect(0, 0, 220, 60)
        ubicacion_boton.center = (ANCHO // 2, y)

        color = self.color_boton_hover if ubicacion_boton.collidepoint(posicion_mouse) else self.color_boton
        pygame.draw.rect(self.pantalla, color, ubicacion_boton, border_radius=10)

        superficie_texto = self.fuente_boton.render(texto, True, (0, 0, 0))
        ubicacion_texto = superficie_texto.get_rect(center=ubicacion_boton.center)
        self.pantalla.blit(superficie_texto, ubicacion_texto)
        return ubicacion_boton

    def ejecutar_menu(self):
        bandera = True
        while bandera:
            posicion_mouse = pygame.mouse.get_pos()
            self.pantalla.fill(self.color_fondo)
            self.centrar_titulo("Final Sentence", self.fuente_titulo, self.color_titulo, 100)

            boton_jugar = self.dibujar_boton("Jugar", 220, posicion_mouse)
            boton_config = self.dibujar_boton("Configuración", 300, posicion_mouse)
            boton_salir = self.dibujar_boton("Salir", 380, posicion_mouse)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    bandera = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_jugar.collidepoint(evento.pos):
                        ejecutar_juego()  # abre el juego
                    elif boton_config.collidepoint(evento.pos):
                        print("Botón Configuración presionado")
                    elif boton_salir.collidepoint(evento.pos):
                        bandera = False

            pygame.display.flip()
            self.reloj.tick(FPS)

        pygame.quit()
        sys.exit()
