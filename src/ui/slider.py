import pygame

class Slider:
    def __init__(self, x, y, width=200, height=6, valor_inicial=50,
                 color_base=(200,200,200), color_fill=(255,255,255)):

        # Caja del slider
        self.rect = pygame.Rect(x, y, width, height)
        self.length = width
        self.height = height

        # Valor
        self.valor = valor_inicial  # 0 – 100 exacto
        
        # Colores
        self.color_base = color_base
        self.color_fill = color_fill

        # Knob
        self.knob_radius = 8
        self.arrastrando = False

    def draw(self, pantalla):
        # === DIBUJAR LA BARRA ===
        pygame.draw.rect(pantalla, self.color_base, self.rect)

        # === BARRA LLENA EN BASE AL VALOR ===
        fill_w = int((self.valor / 100) * self.length)
        barra_llena = pygame.Rect(self.rect.x, self.rect.y, fill_w, self.height)
        pygame.draw.rect(pantalla, self.color_fill, barra_llena)

        # === KNOB ===
        knob_x = self.rect.x + fill_w
        knob_y = self.rect.y + self.height // 2
        pygame.draw.circle(pantalla, self.color_fill, (knob_x, knob_y), self.knob_radius)

        # Guardamos la posición exacta del knob para colisiones
        self.knob_pos = pygame.Rect(knob_x - self.knob_radius,
                                    knob_y - self.knob_radius,
                                    self.knob_radius*2,
                                    self.knob_radius*2)

    def handle_event(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_pos.collidepoint(evento.pos):
                self.arrastrando = True

        if evento.type == pygame.MOUSEBUTTONUP:
            self.arrastrando = False

        if evento.type == pygame.MOUSEMOTION and self.arrastrando:
            mx = evento.pos[0]

            # === LIMITAR ENTRE LOS BORDES DEL SLIDER ===
            mx = max(self.rect.x, min(mx, self.rect.x + self.length))

            # === CALCULAR EL VALOR NUEVO ===
            rel = mx - self.rect.x
            self.valor = int((rel / self.length) * 100)
