import random
import pygame


class FrasesMenu:
    def __init__(self):
        self.frases = [
            "La justicia no existe aquí, solo la venganza y el metal caliente.",
            "Cada bala tiene un nombre. Cada disparo cuenta una historia.",
            "El desierto guarda secretos que los vivos prefieren olvidar.",
            "No hay redención para quien cruza la línea del bien y el mal.",
            "La pólvora nunca miente, revela verdades que el hombre oculta.",
            "El pasado siempre cobra sus deudas, nadie escapa de él.",
            "Solo sobreviven los que disparan primero y hablan después.",
            "Las últimas palabras son las más honestas que dirá un hombre.",
            "Bajo el sol del mediodía se deciden destinos de vida o muerte.",
            "Este juego fue hecho con esfuerzo, café y esperanza de aprobar.",
            "Los bugs también tienen sentimientos, por favor aprueben con piedad.",
            "Si encuentran un error, considérenlo una característica especial.",
            "Este proyecto tuvo más revisiones que tiroteos en el salvaje oeste.",
            "Programar en Python es como duelo al mediodía: rápido o te debuggean.",
            "Gracias profes, ustedes son el sheriff que trae orden a nuestro código."
        ]
        self.frase_actual = random.choice(self.frases)
        self.tiempo_cambio = pygame.time.get_ticks()
        self.intervalo = 20000

    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_cambio >= self.intervalo:
            self.frase_actual = random.choice(self.frases)
            self.tiempo_cambio = tiempo_actual

    def obtener_frase_actual(self):
        return self.frase_actual
