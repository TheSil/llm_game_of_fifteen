import pygame
import random

# Initialize Pygame
pygame.init()

# Window settings
window_size = 400
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("LLM - Game of Fifteen")

# Colors
background_color = (230, 230, 230)  # Light gray for empty space
text_color = (255, 255, 255)  # White for text
tile_color = (0, 120, 215)  # Blue for tiles
line_color = (0, 0, 0)  # Black for lines

# Grid settings
grid_size = 4
cell_size = window_size // grid_size
font = pygame.font.Font(None, 40)

# Initialize tile states
tiles = list(range(1, grid_size * grid_size)) + [0]  # 0 represents the empty space
empty_tile_index = tiles.index(0)  # Index of the empty space


def draw_grid():
    screen.fill(background_color)

    # Draw tiles with background color
    for index, tile in enumerate(tiles):
        row, col = divmod(index, grid_size)
        rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
        if tile != 0:
            pygame.draw.rect(screen, tile_color, rect)  # Background color for tiles
            text = font.render(str(tile), True, text_color)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, background_color, rect)  # Light gray for empty space

    # Draw grid lines
    for x in range(1, grid_size):
        pygame.draw.line(screen, line_color, (x * cell_size, 0), (x * cell_size, window_size))
        pygame.draw.line(screen, line_color, (0, x * cell_size), (window_size, x * cell_size))

    pygame.display.flip()


def swap_tiles(clicked_index):
    global empty_tile_index
    row_empty, col_empty = divmod(empty_tile_index, grid_size)
    row_clicked, col_clicked = divmod(clicked_index, grid_size)

    # Check if the clicked tile is adjacent to the empty space
    if abs(row_empty - row_clicked) + abs(col_empty - col_clicked) == 1:
        # Swap numbers in the tiles list
        tiles[empty_tile_index], tiles[clicked_index] = tiles[clicked_index], tiles[empty_tile_index]
        empty_tile_index = clicked_index


def shuffle_grid():
    global empty_tile_index
    moves = [1, -1, grid_size, -grid_size]  # Possible index moves
    for _ in range(100):  # Number of shuffles
        possible_moves = [empty_tile_index + move for move in moves if 0 <= empty_tile_index + move < grid_size ** 2]
        # Filter for valid moves
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


shuffle_grid()  # Shuffle the puzzle at the start
draw_grid()  # Draw the initial shuffled grid

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = get_click_position(pygame.mouse.get_pos())
            swap_tiles(click_pos)
            draw_grid()

pygame.quit()