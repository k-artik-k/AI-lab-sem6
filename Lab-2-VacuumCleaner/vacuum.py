import pygame
import random
import time

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
GRID_SIZE = 3
CELL_SIZE = 150
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DIRTY = (180, 50, 50)
CLEAN = (200, 200, 200)

pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Vacuum Cleaner Intelligent Agent")

font = pygame.font.SysFont(None, 32)

# ------------------------------------------------------------
# Load Vacuum Cleaner Image
# ------------------------------------------------------------
vacuum_img = pygame.image.load("vacuum.png")     # <-- Must exist in folder
vacuum_img = pygame.transform.scale(vacuum_img, (100, 100))  # Resize to fit cell

# ------------------------------------------------------------
# Environment Definition
# ------------------------------------------------------------
class Environment:
    def __init__(self, size):
        self.size = size
        self.grid = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]

    def is_dirty(self, x, y):
        return self.grid[y][x] == 1

    def clean(self, x, y):
        self.grid[y][x] = 0

# ------------------------------------------------------------
# Agent Definition
# ------------------------------------------------------------
class VacuumAgent:
    def __init__(self, env: Environment):
        self.env = env
        self.x = 0
        self.y = 0
        self.path = self.generate_path()
        self.path_index = 0

    def generate_path(self):
        path = []
        for row in range(self.env.size):
            if row % 2 == 0:
                for col in range(self.env.size):
                    path.append((col, row))
            else:
                for col in reversed(range(self.env.size)):
                    path.append((col, row))
        return path

    def sense_dirty(self):
        return self.env.is_dirty(self.x, self.y)

    def act(self):
        if self.sense_dirty():
            print(f"Cleaning cell {self.x},{self.y}")
            self.env.clean(self.x, self.y)
            return

        if self.path_index < len(self.path) - 1:
            self.path_index += 1
            self.x, self.y = self.path[self.path_index]
            print(f"Moving to {self.x},{self.y}")

# ------------------------------------------------------------
# Drawing Function
# ------------------------------------------------------------
def draw(environment, agent):
    window.fill(WHITE)

    for y in range(environment.size):
        for x in range(environment.size):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = DIRTY if environment.is_dirty(x, y) else CLEAN
            pygame.draw.rect(window, color, rect)
            pygame.draw.rect(window, BLACK, rect, 2)

    # Draw vacuum cleaner image (centered in cell)
    img_x = agent.x * CELL_SIZE + (CELL_SIZE // 2 - 40)  # center image
    img_y = agent.y * CELL_SIZE + (CELL_SIZE // 2 - 40)
    window.blit(vacuum_img, (img_x, img_y))

    pygame.display.update()

# ------------------------------------------------------------
# Main Simulation
# ------------------------------------------------------------
def run_simulation():
    environment = Environment(GRID_SIZE)
    agent = VacuumAgent(environment)

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(1)  # 1 step per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        agent.act()
        draw(environment, agent)

        if all(environment.grid[row][col] == 0 for row in range(GRID_SIZE) for col in range(GRID_SIZE)):
            print("All cells cleaned! Simulation complete.")
            time.sleep(2)
            running = False

    pygame.quit()

# ------------------------------------------------------------
# Run
# ------------------------------------------------------------
if __name__ == "__main__":
    run_simulation()
