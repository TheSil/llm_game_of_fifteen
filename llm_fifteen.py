import pygame
import sys

# Inicializace Pygame
pygame.init()

# Nastavení okna
window_size = 400
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("4x4 Grid Game - Empty Last Square")

# Barvy
background_color = (255, 255, 255)
text_color = (0, 0, 0)
line_color = (0, 0, 0)

# Nastavení mřížky
grid_size = 4
cell_size = window_size // grid_size
font = pygame.font.Font(None, 40)


def draw_grid():
    # Vyčištění obrazovky
    screen.fill(background_color)

    # Vykreslení čísel a čar, kromě posledního políčka
    for row in range(grid_size):
        for col in range(grid_size):
            number = row * grid_size + col + 1
            if number < grid_size * grid_size:  # Pokud to není poslední číslo, vykresli ho
                text = font.render(str(number), True, text_color)
                screen.blit(text, (col * cell_size + cell_size // 3, row * cell_size + cell_size // 4))

    # Vykreslení čar mřížky
    for x in range(1, grid_size):
        pygame.draw.line(screen, line_color, (x * cell_size, 0), (x * cell_size, window_size))
        pygame.draw.line(screen, line_color, (0, x * cell_size), (window_size, x * cell_size))

    pygame.display.flip()


# Hlavní smyčka hry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_grid()

pygame.quit()
sys.exit()