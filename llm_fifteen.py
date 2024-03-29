import pygame
import random
import sys
import numpy
import time

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Generate a simple "beep" sound
def generate_beep_sound(frequency=220, volume=0.1, duration=50):
    """
    Generates a simple beep sound with adjusted parameters for a less loud and annoying experience.
    :param frequency: Frequency of the beep in Hz. Lowered to 220 for a deeper sound.
    :param volume: Volume of the beep, from 0.0 to 1.0. Reduced to 0.1 for lower volume.
    :param duration: Duration of the beep in milliseconds. Shortened to 50ms for a quicker beep.
    :return: A Pygame Sound object.
    """
    sample_rate = 44100
    n_samples = int(round(duration * sample_rate / 1000))
    buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
    max_sample = 2**(16 - 1) - 1
    for s in range(n_samples):
        t = float(s) / sample_rate  # Time in seconds
        buf[s][0] = int(round(max_sample * volume * numpy.sin(2 * numpy.pi * frequency * t)))  # Left channel
        buf[s][1] = int(round(max_sample * volume * numpy.sin(2 * numpy.pi * frequency * t)))  # Right channel
    sound = pygame.sndarray.make_sound(buf)
    return sound

# Create a beep sound
beep_sound = generate_beep_sound()

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
highlight_color = (175, 238, 238)  # Lighter version for the highlight
shadow_color = (95, 158, 160)  # Darker version for the shadow
overlay_color = (0, 0, 0, 128)  # Semi-transparent overlay color

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
win_font = pygame.font.SysFont("comicsansms", 40)  # Larger font for winning message

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

    # Play beep sound
    beep_sound.play()

def draw_empty_tile_border(x, y):
    rect = pygame.Rect(x, y, cell_size, cell_size)
    pygame.draw.rect(screen, empty_tile_color, rect)  # Fill with empty tile color

    # Highlight (Top and Left edges)
    pygame.draw.line(screen, highlight_color, rect.topleft, rect.topright, border_thickness)  # Top edge
    pygame.draw.line(screen, highlight_color, rect.topleft, rect.bottomleft, border_thickness)  # Left edge

    # Shadow (Bottom and Right edges)
    pygame.draw.line(screen, shadow_color, rect.bottomleft, rect.bottomright, border_thickness)  # Bottom edge
    pygame.draw.line(screen, shadow_color, rect.topright, rect.bottomright, border_thickness)  # Right edge

    pygame.draw.rect(screen, border_color, rect, border_thickness)  # Draw border

def check_win_condition():
    if tile_numbers[:-1] == list(range(1, grid_size * grid_size)) and tile_numbers[-1] == 0:
        display_win_message()
        pygame.display.flip()  # Ensure the win message is displayed
        time.sleep(2)  # Pause for 2 seconds to show the win message
        init_tiles()  # Restart the game by re-initializing the tiles

def display_win_message():
    overlay = pygame.Surface((window_size, window_size), pygame.SRCALPHA)  # Create a transparent surface
    overlay.fill(overlay_color)  # Fill the surface with the semi-transparent color
    screen.blit(overlay, (0, 0))  # Draw the overlay on the screen

    win_text = "You Win!"
    text_surface = win_font.render(win_text, True, text_color)
    text_rect = text_surface.get_rect(center=(window_size // 2, window_size // 2))
    screen.blit(text_surface, text_rect)

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
        draw_tile(current_x, current_y, moving_tile_number, is_moving=True)
    else:
        # Animation finished
        is_animating = False
        # Update the tile positions in the list
        target_index = moving_tile_index + (animation_target_pos[1] // cell_size - animation_start_pos[1] // cell_size) * grid_size + (animation_target_pos[0] // cell_size - animation_start_pos[0] // cell_size)
        tile_numbers[moving_tile_index], tile_numbers[target_index] = tile_numbers[target_index], tile_numbers[moving_tile_index]
        check_win_condition()  # Check if the puzzle is solved
def handle_mouse_click(position):
    x, y = position
    col, row = x // cell_size, y // cell_size
    index_clicked = row * grid_size + col
    empty_index = tile_numbers.index(0)

    # Check if the clicked tile is adjacent to the empty space
    if index_clicked == empty_index - 1 and empty_index % grid_size != 0 or \
       index_clicked == empty_index + 1 and empty_index % grid_size != grid_size - 1 or \
       index_clicked == empty_index - grid_size or \
       index_clicked == empty_index + grid_size:
        start_animation(index_clicked, empty_index)

def main():
    init_tiles()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not is_animating:
                # Handle left click
                if event.button == 1:  # Left mouse button
                    handle_mouse_click(event.pos)

        if not is_animating:
            # Update and draw logic when not animating
            screen.fill(background_color)
            draw_grid()
        else:
            # Handle animation
            update_animation()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()