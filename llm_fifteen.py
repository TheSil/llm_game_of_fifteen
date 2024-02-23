import pygame
import sys
import random

# Inicializace Pygame
pygame.init()

# Nastavení okna
window_size = 400
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("4x4 Grid Game - Tiles Keep Their Numbers")

# Barvy
background_color = (255, 255, 255)
text_color = (0, 0, 0)
line_color = (0, 0, 0)

# Nastavení mřížky
grid_size = 4
cell_size = window_size // grid_size
font = pygame.font.Font(None, 40)

# Inicializace stavu políček
tiles = list(range(1, grid_size * grid_size)) + [0]  # 0 reprezentuje prázdné políčko
empty_tile_index = tiles.index(0)  # Index prázdného políčka


def draw_grid():
    screen.fill(background_color)

    # Vykreslení čísel a čar
    for index, tile in enumerate(tiles):
        if tile != 0:
            row, col = divmod(index, grid_size)
            text = font.render(str(tile), True, text_color)
            screen.blit(text, (col * cell_size + cell_size // 3, row * cell_size + cell_size // 4))

    for x in range(1, grid_size):
        pygame.draw.line(screen, line_color, (x * cell_size, 0), (x * cell_size, window_size))
        pygame.draw.line(screen, line_color, (0, x * cell_size), (window_size, x * cell_size))

    pygame.display.flip()


def swap_tiles(clicked_index):
    global empty_tile_index
    row_empty, col_empty = divmod(empty_tile_index, grid_size)
    row_clicked, col_clicked = divmod(clicked_index, grid_size)

    # Kontrola, jestli je kliknuté políčko vedle prázdného
    if abs(row_empty - row_clicked) + abs(col_empty - col_clicked) == 1:
        # Prohodit čísla v seznamu tiles
        tiles[empty_tile_index], tiles[clicked_index] = tiles[clicked_index], tiles[empty_tile_index]
        empty_tile_index = clicked_index


def shuffle_grid():
    global empty_tile_index
    moves = [1, -1, grid_size, -grid_size]  # Možné indexové posuny
    for _ in range(100):  # Počet zamíchání
        possible_moves = [empty_tile_index + move for move in moves if 0 <= empty_tile_index + move < grid_size ** 2]
        # Filtr pro validní tahy
        possible_moves = [move for move in possible_moves if
                          (empty_tile_index % grid_size != 0 or move - empty_tile_index != -1) and (
                                      empty_tile_index % grid_size != grid_size - 1 or move - empty_tile_index != 1)]
        selected_move = random.choice(possible_moves)
        tiles[empty_tile_index], tiles[selected_move] = tiles[selected_move], tiles[empty_tile_index]
        empty_tile_index = selected_move


def get_click_position(pos):
    x, y = pos
    row = y // cell_size
    col = x // cell_size
    return row * grid_size + col


shuffle_grid()  # Zamíchání puzzle při startu

# Hlavní smyčka hry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Levé tlačítko myši
            clicked_index = get_click_position(event.pos)
            swap_tiles(clicked_index)

    draw_grid()

pygame.quit()
sys.exit()