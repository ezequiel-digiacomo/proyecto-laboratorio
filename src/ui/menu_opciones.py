'''
TAREAS PROPIAS: 
* Cambiar la facha de modal_salir
* Meter funciones de volumen y cambio de resolución / fullscreen
* Cambiar el ícono en el borde de la ventana por alguno fachero
* Disfruta el proceso flaco y divertite - Te kiero <3
'''
import pygame, sys, math, random, os
import config
from config import *
from src.ui.slider import Slider
from src.ui.modal_salir import ModalSalir
from src.ui.menu_principal import Menu


class MenuOpciones:
    def __init__(self):
        pygame.init()
        self.opciones = ["Volumen", "Modo de pantalla", "Volver"]
        self.reloj = pygame.time.Clock()
        self.pantalla = aplicar_modo_pantalla()
        self.volumen = 50



        ruta_sonido_hover = os.path.join("assets", "sfx", "options-click.wav")
        self.sonido_hover = pygame.mixer.Sound(ruta_sonido_hover)
        self.sonido_hover.set_volume(0.3)  # volumen entre 0.0 y 1.0
        self.boton_actual = None  # para evitar que suene varias veces seguidas

        # === SLIDER ===
        self.slider = Slider(ANCHO//2 + 200, 260 - 3, valor_inicial=self.volumen,
                             color_base=colores["Belge"], color_fill=colores["Warm"])

        # Ícono
        icono = pygame.image.load("assets/images/revolver_icon2.png")
        pygame.display.set_icon(icono)

        self.fondo = pygame.image.load("assets/images/optionsmenu_background.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))

        self.overlay = pygame.Surface((ANCHO, ALTO))
        self.overlay.fill((0,0,0))

        self.areas = [None for _ in self.opciones]
        self.modal_salir = ModalSalir(self.pantalla)

        pygame.display.set_caption("Opciones")

    def dibujar_titulo(self, texto, x, y):
        superficie = font_title.render(texto, True, colores["Warm"])
        rect = superficie.get_rect(center=(x, y))
        self.pantalla.blit(superficie, rect)

    def dibujar_opciones(self):
        pos_mouse = pygame.mouse.get_pos()

        BASE_Y = 260
        ESPACIO = 100

        SUB_X = ANCHO // 2 + 250  # columna de la derecha (ajustá este valor a tu gusto)

        for i, texto in enumerate(self.opciones):
            area_actual = self.areas[i]
            esta_sobre = area_actual and area_actual.collidepoint(pos_mouse)

            color = colores["Warm"] if esta_sobre else colores["Belge"]
            superficie = font_subtitle_opt.render(texto, True, color)

            pos_y = BASE_Y + i * ESPACIO

            # texto principal
            rect = superficie.get_rect(center=(ANCHO // 2 - 150, pos_y))  
            self.pantalla.blit(superficie, rect)
            self.areas[i] = rect

            # -----------------------------------------
            # SLIDER A LA DERECHA DEL TEXTO "Volumen"
            # -----------------------------------------
            if texto == "Volumen":
                slider_y = pos_y - 3
                slider_x = SUB_X - self.slider.rect.width // 2  # centrado en la columna SUB_X

                self.slider.rect.topleft = (slider_x, slider_y)
                self.slider.y = slider_y
                self.slider.knob_y = slider_y + self.slider.height // 2

                self.slider.draw(self.pantalla)

            # -----------------------------------------
            # TEXTO "Pantalla Completa/Ventana"
            # -----------------------------------------
            if texto == "Modo de pantalla":
                estado = "Pantalla Completa" if config.FULLSCREEN else "Ventana"
                fuente_mas_chica = pygame.font.Font("./assets/fonts/AndadaPro-VariableFont_wght.ttf", 20)
                surf_estado = fuente_mas_chica.render(estado, True, colores["Belge"])

                rect_estado = surf_estado.get_rect(center=(SUB_X, pos_y))
                self.pantalla.blit(surf_estado, rect_estado)

    def ejecutar(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # Reiniciar el cursor
        while True:

            # === EVENTOS ===
            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # SLIDER MANEJA SUS PROPIOS EVENTOS
                self.slider.handle_event(evento)
                self.volumen = self.slider.valor
                pygame.mixer.music.set_volume(self.volumen / 100)

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    click = evento.pos

                    if self.areas[1] and self.areas[1].collidepoint(click):
                        config.FULLSCREEN = not config.FULLSCREEN
                        self.pantalla = config.aplicar_modo_pantalla()

                    elif self.areas[2] and self.areas[2].collidepoint(click):
                        menu = Menu()
                        menu.ejecutar()
                        return

            # === DIBUJAR ===
            self.pantalla.blit(self.fondo, (0,0))

            brillo = 40 + abs(math.sin(pygame.time.get_ticks()*0.002)) * 80
            if random.random() < 0.02: brillo = random.randint(100,200)
            self.overlay.set_alpha(brillo)
            self.pantalla.blit(self.overlay,(0,0))

            self.dibujar_titulo("Opciones", ANCHO//2, 80)
            self.dibujar_opciones()
            
            pos_mouse = pygame.mouse.get_pos()

            hover_modo_pantalla = self.areas[1] and self.areas[1].collidepoint(pos_mouse)
            hover_volver = self.areas[2] and self.areas[2].collidepoint(pos_mouse)
            hover_knob = self.slider.esta_sobre_knob()

            if hover_modo_pantalla or hover_volver or hover_knob:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.update()
            self.reloj.tick(FPS)
