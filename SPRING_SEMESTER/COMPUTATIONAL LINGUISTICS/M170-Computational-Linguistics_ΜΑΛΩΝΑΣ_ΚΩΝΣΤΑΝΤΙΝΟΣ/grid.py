import pygame
import win32gui
import win32con
import win32api

pygame.init()
# Get the actual screen size
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

# Calculate an appropriate grid size based on screen dimensions
GRID_SIZE = min(SCREEN_WIDTH // 20, SCREEN_HEIGHT // 20)  # Adjust the divisor as needed for the desired grid density

GRID_COLOR = (100, 100, 100)  # RGB color for grid lines

def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def grid():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("Grid Lines")

    # Set window transparency (Windows only)
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

    clock = pygame.time.Clock()

    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             print('HERE')
    #             pygame.quit()
    #             #sys.exit()

    screen.fill((0, 0, 0, 0))  # Fill the screen with fully transparent color
    draw_grid(screen)  # Draw the grid lines on top of the transparent screen
    pygame.display.update()

    clock.tick(60)  # Limit the frame rate to 60 FPS

def close():
    pygame.display.quit()