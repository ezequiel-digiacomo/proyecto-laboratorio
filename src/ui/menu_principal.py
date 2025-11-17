import pygame, sys, math, random
from config import *
from src.juego import NewGame
from src.ui.modal_salir import ModalSalir
from src.utils.frases_menu import FrasesMenu


class Menu():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()   # inicializa audio

        #  musica de fondo 
        pygame.mixer.music.load(sounds / "musica-menu.ogg")  # ruta desde config
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # loop infinito
        
        
        self.opciones= ["Jugar", "Opciones", "Salir"]
        self.reloj = pygame.time.Clock()
        self.pantalla = aplicar_modo_pantalla()

        # Agregué el ícono pa desbordar facha
        icono = pygame.image.load("assets/images/revolver_icon2.png")
        pygame.display.set_icon(icono)

        # Agregado de fondo y "capa de titileo"
        self.fondo = pygame.image.load("assets/images/mainmenu_background.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        self.overlay = pygame.Surface((ANCHO, ALTO))
        self.overlay.fill((0, 0, 0))

        self.area_opcion0 = None
        self.area_opcion1 = None
        self.area_opcion2 = None
        self.modal_salir = ModalSalir(self.pantalla)
        self.frases_menu = FrasesMenu()

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
            superficie = font_subtitle_main.render(texto, True, color)
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

    def dibujar_titulo(self, texto, x, y):
        superficie = font_title.render(texto, True, colores["Warm"])
        rectangulo_texto = superficie.get_rect()
        rectangulo_texto = (x,y)
        self.pantalla.blit(superficie, rectangulo_texto)

    def dividir_en_lineas(self, texto, ancho_max):
        palabras, lineas, linea = texto.split(), [], ""
        for palabra in palabras:
            prueba = linea + palabra + " "
            if font_leyenda.size(prueba)[0] <= ancho_max:
                linea = prueba
            else:
                if linea:
                    lineas.append(linea.strip())
                linea = palabra + " "
        if linea:
            lineas.append(linea.strip())
        return lineas

    def dibujar_frase(self):
        for i, linea in enumerate(self.dividir_en_lineas(self.frases_menu.obtener_frase_actual(), 230)):
            superficie = pygame.transform.rotate(font_leyenda.render(linea, True, (35, 25, 15)), 5)
            self.pantalla.blit(superficie, (175 + i * 2, 200 + i * 20))


    def ejecutar(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # Reiniciar el cursor
        while True:
            #self.pantalla.fill(colores["Negro"]) #Con esto limpio el modal
            self.pantalla.blit(self.fondo, (0, 0)) # Reemplacé el fondo negro por la imágen

            # Efecto de titileo de luz
            brillo = 15 + abs(math.sin(pygame.time.get_ticks() * 0.001)) * 80
            if random.random() < 0.02:
                brillo = random.randint(100, 200)
            self.overlay.set_alpha(brillo)
            self.pantalla.blit(self.overlay, (0, 0))

            # Actualizar frases
            self.frases_menu.actualizar()

            self.dibujar_titulo("Final Sentences", 450, 80)
            self.dibujar_opciones()
            self.dibujar_frase()

            # Mouse de la manito pa los botones
            pos_mouse = pygame.mouse.get_pos()

            if (self.area_opcion0 and self.area_opcion0.collidepoint(pos_mouse)) or \
            (self.area_opcion1 and self.area_opcion1.collidepoint(pos_mouse)) or \
            (self.area_opcion2 and self.area_opcion2.collidepoint(pos_mouse)):

                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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
                        inicio = NewGame()
                        inicio.ejecutar_juego()
                    elif self.area_opcion1.collidepoint(click_pos):  # ✅ nueva conexión
                        from src.ui.menu_opciones import MenuOpciones
                        menu_opciones = MenuOpciones()
                        menu_opciones.ejecutar()
                    elif self.area_opcion2.collidepoint(click_pos):
                        self.modal_salir.abrir()

            self.modal_salir.dibujar()

            pygame.display.update()
            self.reloj.tick(FPS)
