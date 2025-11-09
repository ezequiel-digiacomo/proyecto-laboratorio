"""
Tarea Pendiente juego.py: 

    - Realizar funciones: Puntaje y Reinicio de partida
    - Mejorar la generación de texto en cuanto lo visual
    - Limpiar el bucle de ejecución haciendo más legible el código
    - Implementar: Sónidos e imagenes al juego 
    - Comprobación: Verificar que la función generador_frases ubicada en la carpeta palabras.py funcione

"""

#Ignoren las advertencias porque a lo último estuve quitando código haciendo que posiblemente se rompa

from config import *
from src.utils.palabras import *
import pygame
import sys
import time



def ejecutar_juego():

    pygame.init()
    pygame.display.set_caption("Final Sentence - Juego")

    entrada_usuario = ""
    ronda = 1
    tiempo_total = 30
    inicio_tiempo = None
    juego_activo = True
    frase = generador_frases("https://poetrydb.org/author/Ernest Dowson")

    def reinicio():
        nonlocal ronda, entrada_usuario, frase
        ronda += 1
        entrada_usuario = ""
        frase = texto_generico()

    def mostrar_game_over():
        pantalla.fill(colores["Maroon"])
        dibujar_texto("⏰ ¡Tiempo agotado!", font_title, colores["Warm"], 180, 130)
        dibujar_texto(f"Puntaje final: {puntaje}", font_text, colores["Maroon"], 270, 230)
        dibujar_texto("Presioná ENTER para volver al menú", font_text, colores["Maroon"], 200, 300)
        pygame.display.flip()

    # --- Bucle principal del juego ---
    while True:
        pantalla.fill(colores["Negro"])

        if juego_activo:
            if inicio_tiempo:
                tiempo_restante = tiempo_total - (time.time() - inicio_tiempo)
            else:
                tiempo_restante = tiempo_total

            if tiempo_restante <= 0:
                juego_activo = False
                continue

            dibujar_texto("FINAL SENTENCE", font_title, colores["Maroon"], 230, 30)
            dibujar_texto(f"Ronda: {ronda}", font_text, colores["Maroon"], 30, 100)
            dibujar_texto(f"Puntaje: {puntaje}", font_text, colores["Maroon"], 650, 100)
            dibujar_texto(f"Tiempo: {int(tiempo_restante)}s", font_title, colores["Maroon"], 350, 100)

            dibujar_texto("Escribí esta frase:", font_text, colores["Belge"], 50, 160)
            dibujar_texto(frase, font_text, colores["Belge"], 50, 200)
            dibujar_texto(entrada_usuario, font_text, colores["Belge"], 50, 260)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return  # volver al menú
                    elif evento.key == pygame.K_RETURN:
                        if entrada_usuario == frase:
                            puntaje += 20
                            tiempo_total += 20
                            reinicio()
                        else:
                            puntaje -= 5
                        entrada_usuario = ""
                    elif evento.key == pygame.K_BACKSPACE:
                        entrada_usuario = entrada_usuario[:-1]
                    else:
                        entrada_usuario += evento.unicode
                        if not inicio_tiempo:
                            inicio_tiempo = time.time()
                        if not frase.startswith(entrada_usuario):
                            puntaje -= 1

        else:
            mostrar_game_over()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    return  # volver al menú

        pygame.display.flip()