import pygame, sys, math, random
from config import *
from src.juego import *
from src.ui.modal_salir import ModalSalir


class Menu():
    def __init__(self):
        pygame.init()
        self.opciones= ["Jugar", "Opciones", "Salir"]
        self.reloj = pygame.time.Clock()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))

        # Agregado de fondo y "capa de titileo"
        self.fondo = pygame.image.load("assets/images/mainmenu_background.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        self.overlay = pygame.Surface((ANCHO, ALTO))
        self.overlay.fill((0, 0, 0))
        
        self.area_opcion0 = None
        self.area_opcion1 = None
        self.area_opcion2 = None
        self.modal_salir = ModalSalir(self.pantalla)
        pygame.display.set_caption("Menu Principal")

    def dibujar_opciones(self):
        pos_mouse = pygame.mouse.get_pos() # Obtengo la posición del mouse

        for i, texto in enumerate(self.opciones):
            # Detectar si el mouse está sobre la opción
            area_actual = getattr(self, f"area_opcion{i}")
            esta_sobre = area_actual and area_actual.collidepoint(pos_mouse)

            # Color y escala base
            color = colores["Belge"]
            escala = 1.0

            # Si el mouse pasa por arriba, aplicar efecto
            if esta_sobre:
                color = colores["Warm"]  # Cambiá por el color x más contraste
                escala = 1.05  # Leve aumento 

            # Renderizar texto normal y luego escalarlo
            superficie = font_title.render(texto, True, color)
            if escala != 1.0:
                ancho = int(superficie.get_width() * escala)
                alto = int(superficie.get_height() * escala)
                superficie = pygame.transform.smoothscale(superficie, (ancho, alto))

            # Calcular posición (alinear por la derecha)
            parametro = superficie.get_rect(topright=(ANCHO - 100, 200 + i * 80))
            self.pantalla.blit(superficie, parametro)

            if esta_sobre:
                start = (parametro.left, parametro.bottom + 5)
                end = (parametro.right, parametro.bottom + 5)
                pygame.draw.line(self.pantalla, color, start, end, 3)

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
            #self.pantalla.fill(colores["Negro"]) #Con esto limpio el modal
            self.pantalla.blit(self.fondo, (0, 0)) # Reemplacé el fondo negro por la imágen

            # Efecto de titileo de luz
            brillo = 15 + abs(math.sin(pygame.time.get_ticks() * 0.001)) * 80
            if random.random() < 0.02:
                brillo = random.randint(100, 200)
            self.overlay.set_alpha(brillo)
            self.pantalla.blit(self.overlay, (0, 0))

            self.dibujar_titulo("Final Sentences", 450, 80)
            self.dibujar_opciones()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                #Aca veririfico las acciones del Modal Salir
                accion_modal = self.modal_salir.manejar_eventos(evento)
                if accion_modal == 'salir':
                    pygame.quit()
                    sys.exit()
                elif accion_modal == 'cancelar':
                    continue

                if not self.modal_salir.activo and evento.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = evento.pos
                    if self.area_opcion0.collidepoint(click_pos):
                        ejecutar_juego()
                        print(click_pos)
                    elif self.area_opcion2.collidepoint(click_pos):
                        self.modal_salir.abrir()

            self.modal_salir.dibujar()

            pygame.display.update()
            self.reloj.tick(FPS)
