import pygame
import random
import sys
import time

def ejecutar_juego():
    pygame.init()

    # --- Configuración general ---
    ANCHO, ALTO = 800, 400
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Final Sentence - Juego de Escritura")

    # Colores
    NEGRO = (0, 0, 0)
    AZUL = (0, 150, 255)
    AZUL_OSCURO = (0, 100, 200)
    ROJO = (255, 80, 80)

    # Fuentes
    fuente_titulo = pygame.font.Font(None, 60)
    fuente_texto = pygame.font.Font(None, 40)
    fuente_info = pygame.font.Font(None, 30)
    fuente_gameover = pygame.font.Font(None, 70)

    # Listas para generar frases
    sujetos = ["La naturaleza", "El programador", "Una mente curiosa", "El conocimiento", "La paciencia", "El arte", "La ciencia"]
    verbos = ["crea", "inspira", "transforma", "enseña", "guía", "fortalece", "descubre", "encuentra"]
    complementos = ["el camino correcto", "una solución nueva", "la armonía interior", "el poder del cambio", "la belleza de lo natural", "la esencia de la vida", "la fuerza del equilibrio"]

    def generar_frase():
        return f"{random.choice(sujetos)} {random.choice(verbos)} {random.choice(complementos)}."

    puntaje = 0
    ronda = 1
    entrada_usuario = ""
    frase_actual = generar_frase()
    tiempo_total = 30
    inicio_tiempo = None
    juego_activo = True

    def dibujar_texto(texto, fuente, color, x, y):
        superficie = fuente.render(texto, True, color)
        pantalla.blit(superficie, (x, y))

    def reiniciar_ronda():
        nonlocal frase_actual, entrada_usuario, ronda
        ronda += 1
        entrada_usuario = ""
        frase_actual = generar_frase()

    def mostrar_game_over():
        pantalla.fill(NEGRO)
        dibujar_texto("⏰ ¡Tiempo agotado!", fuente_gameover, ROJO, 180, 130)
        dibujar_texto(f"Puntaje final: {puntaje}", fuente_texto, AZUL, 270, 230)
        dibujar_texto("Presioná ENTER para volver al menú", fuente_info, AZUL, 200, 300)
        pygame.display.flip()

    # --- Bucle principal del juego ---
    while True:
        pantalla.fill(NEGRO)

        if juego_activo:
            if inicio_tiempo:
                tiempo_restante = tiempo_total - (time.time() - inicio_tiempo)
            else:
                tiempo_restante = tiempo_total

            if tiempo_restante <= 0:
                juego_activo = False
                continue

            color = AZUL if frase_actual.startswith(entrada_usuario) else ROJO

            dibujar_texto("FINAL SENTENCE", fuente_titulo, AZUL, 230, 30)
            dibujar_texto(f"Ronda: {ronda}", fuente_info, AZUL, 30, 100)
            dibujar_texto(f"Puntaje: {puntaje}", fuente_info, AZUL, 650, 100)
            dibujar_texto(f"Tiempo: {int(tiempo_restante)}s", fuente_info, AZUL, 350, 100)

            dibujar_texto("Escribí esta frase:", fuente_texto, AZUL_OSCURO, 50, 160)
            dibujar_texto(frase_actual, fuente_texto, AZUL, 50, 200)
            dibujar_texto(entrada_usuario, fuente_texto, color, 50, 260)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return  # volver al menú
                    elif evento.key == pygame.K_RETURN:
                        if entrada_usuario == frase_actual:
                            puntaje += 20
                            tiempo_total += 20
                            reiniciar_ronda()
                        else:
                            puntaje -= 5
                        entrada_usuario = ""
                    elif evento.key == pygame.K_BACKSPACE:
                        entrada_usuario = entrada_usuario[:-1]
                    else:
                        entrada_usuario += evento.unicode
                        if not inicio_tiempo:
                            inicio_tiempo = time.time()
                        if not frase_actual.startswith(entrada_usuario):
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
