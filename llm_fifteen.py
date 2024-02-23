import pygame
import sys

# Inicializace Pygame
pygame.init()

# Nastavení okna
window_size = 400
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("4x4 Grid Game - Swap with Empty")

# Barvy
background_color = (255, 255, 255)
text_color = (0, 0, 0)
line_color = (0, 0, 0)

# Nastavení mřížky a prázdného políčka
grid_size = 4
cell_size = window_size // grid_size
font = pygame.font.Font(None, 40)
empty_tile = (grid_size - 1, grid_size - 1)  # Pozice prázdného políčka


def draw_grid():
    screen.fill(background_color)

    # Vykreslení čísel a čar, kromě prázdného políčka
    for row in range(grid_size):
        for col in range(grid_size):
            if (row, col) != empty_tile:
                number = row * grid_size + col + 1
                text = font.render(str(number), True, text_color)
                screen.blit(text, (col * cell_size + cell_size // 3, row * cell_size + cell_size // 4))

    for x in range(1, grid_size):
        pygame.draw.line(screen, line_color, (x * cell_size, 0), (x * cell_size, window_size))
        pygame.draw.line(screen, line_color, (0, x * cell_size), (window_size, x * cell_size))

    pygame.display.flip()


def swap_tiles(position):
    global empty_tile
    row, col = position
    if row == empty_tile[0] and abs(col - empty_tile[1]) == 1 or \
            col == empty_tile[1] and abs(row - empty_tile[0]) == 1:
        # Výměna políček
        empty_tile = position


def get_click_position(pos):
    x, y = pos
    row = y // cell_size
    col = x // cell_size
    return (row, col)


# Hlavní smyčka hry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Levé tlačítko myši
            click_pos = get_click_position(event.pos)
            swap_tiles(click_pos)

    draw_grid()

pygame.quit()
sys.exit()