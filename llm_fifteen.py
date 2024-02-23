import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Window settings
window_size = 400
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("LLM - Game of Fifteen")

# Define colors
tile_color = (135, 206, 250)  # Light Sky Blue
empty_tile_color = (200, 200, 200)  # Gray for the empty tile
border_color = (0, 0, 0)  # Black for borders
text_color = (255, 255, 255)  # White for text
background_color = (230, 230, 230)  # Light grey color

# Define border thickness
border_thickness = 3

# Grid settings
grid_size = 4
cell_size = window_size // grid_size
tile_numbers = []

# Animation settings
is_animating = False
animation_duration = 100  # Duration in milliseconds
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
    color = empty_tile_color if number == 0 else tile_color
    rect = pygame.Rect(x, y, cell_size, cell_size)
    pygame.draw.rect(screen, color, rect)  # Draw the tile

    # Shadow and highlight colors
    highlight_color = (175, 238, 238)  # Lighter version for the highlight
    shadow_color = (95, 158, 160)  # Darker version for the shadow

    # Highlight (Top and Left edges)
    pygame.draw.line(screen, highlight_color, rect.topleft, rect.topright, border_thickness)  # Top edge
    pygame.draw.line(screen, highlight_color, rect.topleft, rect.bottomleft, border_thickness)  # Left edge

    # Shadow (Bottom and Right edges)
    pygame.draw.line(screen, shadow_color, rect.bottomleft, rect.bottomright, border_thickness)  # Bottom edge
    pygame.draw.line(screen, shadow_color, rect.topright, rect.bottomright, border_thickness)  # Right edge

    pygame.draw.rect(screen, border_color, rect, 3)  # Draw the border

    if number > 0:  # Only draw numbers for non-empty tiles
        text_surface = font.render(str(number), True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)


# Make sure to call draw_grid_lines() at the end of the draw_grid() function if not animating
def draw_grid():
    global tile_numbers  # Ensure tile_numbers is accessible
    for i in range(grid_size):
        for j in range(grid_size):
            index = i * grid_size + j
            if is_animating and index == moving_tile_index:
                # Draw only the border and background for the empty spot
                x, y = j * cell_size, i * cell_size
                draw_empty_tile_border(x, y)
            else:
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
    # Draw the empty tile space in gray immediately
    draw_tile(*animation_target_pos, 0, is_moving=True)  # Pass the position and 0 for the empty tile


def draw_empty_tile_border(x, y):
    rect = pygame.Rect(x, y, cell_size, cell_size)

    # Shadow and highlight colors
    highlight_color = (175, 238, 238)  # Lighter version for the highlight
    shadow_color = (95, 158, 160)  # Darker version for the shadow

    pygame.draw.rect(screen, empty_tile_color, rect)  # Fill with empty tile color

    # Highlight (Top and Left edges)
    pygame.draw.line(screen, highlight_color, rect.topleft, rect.topright, border_thickness)  # Top edge
    pygame.draw.line(screen, highlight_color, rect.topleft, rect.bottomleft, border_thickness)  # Left edge

    # Shadow (Bottom and Right edges)
    pygame.draw.line(screen, shadow_color, rect.bottomleft, rect.bottomright, border_thickness)  # Bottom edge
    pygame.draw.line(screen, shadow_color, rect.topright, rect.bottomright, border_thickness)  # Right edge

    pygame.draw.rect(screen, border_color, rect, border_thickness)  # Draw border

def update_animation():
    global is_animating
    now = pygame.time.get_ticks()
    progress = min(1, (now - animation_start_time) / animation_duration)

    screen.fill(background_color)  # Clear the screen
    draw_grid()  # Draw the grid, including the empty tile with its border

    if progress < 1:
        # Calculate the moving tile's current position
        current_x = animation_start_pos[0] + (animation_target_pos[0] - animation_start_pos[0]) * progress
        current_y = animation_start_pos[1] + (animation_target_pos[1] - animation_start_pos[1]) * progress
        draw_tile(current_x, current_y, moving_tile_number, is_moving=True)  # Draw moving tile on top
    else:
        is_animating = False
        finalize_move()

    pygame.display.flip()  # Refresh the display


def check_win_condition():
    # Check if all tiles are in the correct order
    return tile_numbers == list(range(1, grid_size * grid_size)) + [0]

def display_win_message():
    # Create a semi-transparent surface
    overlay = pygame.Surface((window_size, window_size), pygame.SRCALPHA)  # Use SRCALPHA to support alpha transparency
    overlay.fill((0, 255, 0, 128))  # Green overlay with alpha (128 for semi-transparent)

    # Blit the semi-transparent overlay onto the screen
    screen.blit(overlay, (0, 0))

    # Draw the win text directly onto the screen, over the overlay
    win_text = "You Win!"
    text_surface = font.render(win_text, True, (255, 255, 255))  # White text
    text_rect = text_surface.get_rect(center=(window_size / 2, window_size / 2))
    screen.blit(text_surface, text_rect)  # Blit text onto the screen, not the overlay

    pygame.display.flip()
    pygame.time.wait(1000)  # Short wait to display the message before resetting

def finalize_move():
    # Swap tiles in the list to reflect the new state
    empty_index = tile_numbers.index(0)
    tile_numbers[moving_tile_index], tile_numbers[empty_index] = 0, moving_tile_number
    # Check for win condition
    if check_win_condition():
        display_win_message()
        pygame.time.wait(2000)  # Wait for 2 seconds to let the player see the win message
        init_tiles()  # Reinitialize the game to start a new one
    else:
        # If not won, continue as usual
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