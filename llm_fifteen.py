import pygame
import random

# Initialize Pygame
pygame.init()

# Window settings
window_size = 400
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("LLM - Game of Fifteen")

# Define colors
background_color = (255, 255, 255)  # White background
tile_color = (0, 0, 255)  # Blue tiles
empty_tile_color = (170, 170, 170)  # Gray for empty tile
text_color = (255, 255, 255)  # White text for better contrast on blue tiles
border_color = (0, 0, 0)  # Black border for tiles

# Define border thickness
border_thickness = 3

# Grid settings
grid_size = 4
cell_size = window_size // grid_size
tile_numbers = []

# Animation settings
is_animating = False
animation_duration = 200  # Duration in milliseconds
animation_start_time = 0
moving_tile_index = None
moving_tile_number = None
animation_target_pos = ()
animation_start_pos = ()

# Font settings
font = pygame.font.SysFont("comicsansms", 30)


def init_tiles():
    global tile_numbers
    tile_numbers = list(range(1, grid_size * grid_size)) + [0]  # Last tile is empty
    shuffle_tiles()


def shuffle_tiles():
    empty_index = grid_size * grid_size - 1
    for _ in range(1000):
        neighbor_indexes = [empty_index - 1 if empty_index % grid_size != 0 else None,  # Left
                            empty_index + 1 if empty_index % grid_size != grid_size - 1 else None,  # Right
                            empty_index - grid_size if empty_index >= grid_size else None,  # Up
                            empty_index + grid_size if empty_index < grid_size * (grid_size - 1) else None]  # Down
        neighbor_indexes = [index for index in neighbor_indexes if index is not None]
        chosen_index = random.choice(neighbor_indexes)
        tile_numbers[empty_index], tile_numbers[chosen_index] = tile_numbers[chosen_index], tile_numbers[empty_index]
        empty_index = chosen_index


def draw_tile(x, y, number, is_moving=False):
    # Determine the color based on whether the tile is empty
    color = empty_tile_color if number == 0 else tile_color

    # Calculate the tile's rectangle area
    rect = pygame.Rect(x, y, cell_size, cell_size)

    # Draw the tile
    pygame.draw.rect(screen, color, rect)  # Use the determined color

    # Draw border for all tiles
    pygame.draw.rect(screen, border_color, rect, border_thickness)

    # Draw the number for non-empty tiles
    if number > 0:
        text_surface = font.render(str(number), True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

# Make sure to call draw_grid_lines() at the end of the draw_grid() function if not animating
def draw_grid(skip_index=None):
    global tile_numbers
    for i in range(grid_size):
        for j in range(grid_size):
            index = i * grid_size + j
            if index != skip_index:  # Skip drawing the tile at skip_index
                x, y = j * cell_size, i * cell_size
                draw_tile(x, y, tile_numbers[index])


def start_animation(from_index, to_index):
    global is_animating, animation_start_time, moving_tile_index, moving_tile_number, animation_target_pos, animation_start_pos
    is_animating = True
    animation_start_time = pygame.time.get_ticks()
    moving_tile_index = from_index
    moving_tile_number = tile_numbers[from_index]
    animation_start_pos = (from_index % grid_size * cell_size, from_index // grid_size * cell_size)
    animation_target_pos = (to_index % grid_size * cell_size, to_index // grid_size * cell_size)


def draw_grid_lines():
    # Draw grid lines
    for i in range(grid_size + 1):
        pygame.draw.line(screen, line_color, (0, i * cell_size), (window_size, i * cell_size))
        pygame.draw.line(screen, line_color, (i * cell_size, 0), (i * cell_size, window_size))


def update_animation():
    global is_animating
    now = pygame.time.get_ticks()
    progress = min(1, (now - animation_start_time) / animation_duration)

    if progress < 1:
        # Calculate current animated tile position
        current_x = animation_start_pos[0] + (animation_target_pos[0] - animation_start_pos[0]) * progress
        current_y = animation_start_pos[1] + (animation_target_pos[1] - animation_start_pos[1]) * progress
        # Draw everything except the moving tile
        screen.fill(background_color)  # Clear screen
        draw_grid(skip_index=moving_tile_index)  # Draw the static tiles, skipping the moving tile's original position
        # Draw moving tile on top
        draw_tile(current_x, current_y, moving_tile_number, is_moving=True)
    else:
        # Animation complete, finalize state
        is_animating = False
        finalize_move()

    pygame.display.flip()  # Update the display

def finalize_move():
    # Swap tiles in the list to reflect the new state
    empty_index = tile_numbers.index(0)
    tile_numbers[moving_tile_index], tile_numbers[empty_index] = 0, moving_tile_number
    # Redraw the grid to reflect the new state
    screen.fill(background_color)
    draw_grid()
    pygame.display.flip()

init_tiles()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not is_animating:
            x, y = pygame.mouse.get_pos()
            clicked_index = x // cell_size + (y // cell_size) * grid_size
            empty_index = tile_numbers.index(0)
            # Check if the clicked tile is adjacent to the empty tile
            if clicked_index in [empty_index - 1, empty_index + 1, empty_index - grid_size, empty_index + grid_size]:
                start_animation(clicked_index, empty_index)

    screen.fill(background_color)
    if is_animating:
        update_animation()
    else:
        draw_grid()
    pygame.display.flip()

pygame.quit()