import pygame

pygame.init()

#COLORES
colores = {
    "Negro": (0,0,0,0),
    "Maroon": (142,22,22),
    "Belge": (232, 201, 153),
    "Warm": (248, 238, 223)
}

#PANTALLA
ANCHO = 1280
ALTO = 720
FPS = 60

#Fuentes
font_title = pygame.font.Font("./Sources/SpecialElite-Regular.ttf", 40)
font_text = pygame.font.Font("./Sources/AndadaPro-VariableFont_wght.ttf", 12)