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

pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Vacuum Cleaner Intelligent Agent")

font = pygame.font.SysFont(None, 32)

# ------------------------------------------------------------
# Load Images
# ------------------------------------------------------------
vacuum_img = pygame.image.load("vacuum.png")
vacuum_img = pygame.transform.scale(vacuum_img, (100, 100))

dirt_img = pygame.image.load("dirt.png")
dirt_img = pygame.transform.scale(dirt_img, (100, 100))

clean_color = (220, 220, 220)

# ------------------------------------------------------------
# Environment
# ------------------------------------------------------------
class Environment:
    def __init__(self, size):
        self.size = size
        # 1 = dirty, 0 = clean
        self.grid = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]

    def is_dirty(self, x, y):
        return self.grid[y][x] == 1

    def clean(self, x, y):
        self.grid[y][x] = 0

# ------------------------------------------------------------
# Agent
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
# Drawing
# ------------------------------------------------------------
def draw(environment, agent):
    window.fill(WHITE)

    for y in range(environment.size):
        for x in range(environment.size):
            cell_x = x * CELL_SIZE
            cell_y = y * CELL_SIZE

            # Draw background
            pygame.draw.rect(window, clean_color, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(window, BLACK, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 2)

            # Draw dirt if dirty
            if environment.is_dirty(x, y):
                window.blit(dirt_img, (cell_x + 25, cell_y + 25))

    # Draw vacuum image centered in its cell
    agent_x = agent.x * CELL_SIZE + 25
    agent_y = agent.y * CELL_SIZE + 25
    window.blit(vacuum_img, (agent_x, agent_y))

    pygame.display.update()

# ------------------------------------------------------------
# Simulation
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

        # Stop when everything is clean
        if all(environment.grid[r][c] == 0 for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
            print("All cells cleaned! Simulation complete.")
            time.sleep(2)
            running = False

    pygame.quit()

# ------------------------------------------------------------
# Run
# ------------------------------------------------------------
if __name__ == "__main__":
    run_simulation()
