import pygame
import random

# Initialize Pygame
pygame.init()

# Window settings
window_size = 400
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("LLM - Game of Fifteen")

# Colors
background_color = (200, 200, 200)  # Slightly darker gray for the empty space
text_color = (255, 255, 255)  # White for text
tile_color = (0, 120, 215)  # Blue for tiles
line_color = (0, 0, 0)  # Black for lines
win_overlay_color = (0, 200, 0, 127)  # Green with transparency for the win overlay

# Grid settings
grid_size = 4
cell_size = window_size // grid_size

# Try to load a more playful system font
font_name = "Comic Sans MS"  # Comic Sans is generally considered more "playful"
font_size = 40
font = pygame.font.SysFont(font_name, font_size)


def initialize_tiles():
    global tiles, empty_tile_index
    tiles = list(range(1, grid_size * grid_size)) + [0]  # 0 represents the empty space
    empty_tile_index = tiles.index(0)  # Index of the empty space


initialize_tiles()


def draw_grid():
    screen.fill(background_color)

    for index, tile in enumerate(tiles):
        row, col = divmod(index, grid_size)
        rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
        if tile != 0:
            pygame.draw.rect(screen, tile_color, rect)
            text = font.render(str(tile), True, text_color)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, background_color, rect)  # Light gray for empty space

    for x in range(1, grid_size):
        pygame.draw.line(screen, line_color, (x * cell_size, 0), (x * cell_size, window_size))
        pygame.draw.line(screen, line_color, (0, x * cell_size), (window_size, x * cell_size))

    pygame.display.flip()


def display_win_message():
    overlay = pygame.Surface((window_size, window_size))  # Create a transparent overlay
    overlay.set_alpha(128)  # Transparency level
    overlay.fill(win_overlay_color)
    screen.blit(overlay, (0, 0))

    win_text = "You Win!"
    win_font = pygame.font.Font(None, 80)
    win_render = win_font.render(win_text, True, text_color)
    win_rect = win_render.get_rect(center=(window_size // 2, window_size // 2))
    screen.blit(win_render, win_rect)
    pygame.display.flip()


def check_win_condition():
    return tiles == list(range(1, grid_size * grid_size)) + [0]


def swap_tiles(clicked_index):
    global empty_tile_index
    row_empty, col_empty = divmod(empty_tile_index, grid_size)
    row_clicked, col_clicked = divmod(clicked_index, grid_size)

    if abs(row_empty - row_clicked) + abs(col_empty - col_clicked) == 1:
        tiles[empty_tile_index], tiles[clicked_index] = tiles[clicked_index], tiles[empty_tile_index]
        empty_tile_index = clicked_index


def shuffle_grid():
    global empty_tile_index
    moves = [1, -1, grid_size, -grid_size]
    for _ in range(100):
        possible_moves = [empty_tile_index + move for move in moves if 0 <= empty_tile_index + move < grid_size ** 2]
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


def reset_game():
    initialize_tiles()
    shuffle_grid()
    draw_grid()


shuffle_grid()
draw_grid()

running = True
win_displayed = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if win_displayed:
                win_displayed = False  # Reset the win_displayed flag
                reset_game()  # Reset and shuffle the puzzle for a new game
            else:
                click_pos = get_click_position(pygame.mouse.get_pos())
                swap_tiles(click_pos)
                draw_grid()
                if check_win_condition():
                    display_win_message()
                    win_displayed = True

pygame.quit()