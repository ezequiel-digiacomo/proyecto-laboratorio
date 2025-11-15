import pygame

pygame.init()

#COLORES
colores = {
    "Negro": (0,0,0,0),
    "Maroon": (142,22,22),
    "Belge": (232, 201, 153),
    "Warm": (248, 238, 223),

    # Colores nuevos facheros facheritos
    "DarkWood": (59, 47, 47),
    "Mahogany": (92, 47, 31),
    "OldPaper": (201, 178, 138),
    "BurnedEdge": (29, 21, 18)
}

#PANTALLA
ANCHO = 1280
ALTO = 720
FPS = 60

# Estado global de pantalla
FULLSCREEN = False

def aplicar_modo_pantalla():
    global FULLSCREEN
    if FULLSCREEN:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode((ANCHO, ALTO))

#Fuentes
font_title = pygame.font.Font("./assets/fonts/SpecialElite-Regular.ttf", 46) # Aumenté tamaño del Título
font_subtitle_main = pygame.font.Font("./assets/fonts/SpecialElite-Regular.ttf", 40) # Cree subtitulos para el principal
font_subtitle_opt = pygame.font.Font("./assets/fonts/SpecialElite-Regular.ttf", 32) # y para el menu de opciones
font_text = pygame.font.Font("./assets/fonts/AndadaPro-VariableFont_wght.ttf", 12)
