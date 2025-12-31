import pygame
import sys

pygame.init()

# Window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monkey Banana 2.5D 🐒🍌")
clock = pygame.time.Clock()

# Load images
def load_img(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except Exception as e:
        print("Image load error:", path)
        pygame.quit()
        sys.exit()

monkey_img = load_img("images/monkey.png", (60, 60))
monkey_banana_img = load_img("images/monkey_banana.png", (60, 60))
box_img = load_img("images/box.png", (80, 80))
banana_img = load_img("images/banana.png", (40, 40))
door_img = load_img("images/door.png", (80, 80))

# Game objects
class GameObject:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = image
        self.height = 0  # for climb/stacking

    def iso_pos(self):
        """Convert x,y to isometric screen position"""
        iso_x = self.rect.x - self.rect.y
        iso_y = (self.rect.x + self.rect.y)/2 - self.height
        return int(iso_x + WIDTH//2 - 200), int(iso_y + 100)

    def draw(self, surface):
        x, y = self.iso_pos()
        surface.blit(self.image, (x, y))

# Create objects
monkey = GameObject(50, 350, 60, 60, monkey_img)
box = GameObject(350, 350, 80, 80, box_img)
banana = GameObject(380, 120, 40, 40, banana_img)
door = GameObject(700, 50, 80, 80, door_img)

monkey_on_box = False
has_banana = False

# Walls for collision (rectangles, top-down logic)
walls = [
    pygame.Rect(0, 0, WIDTH, 10),
    pygame.Rect(0, 0, 10, HEIGHT),
    pygame.Rect(0, HEIGHT-10, WIDTH, 10),
    pygame.Rect(WIDTH-10, 0, 10, HEIGHT)
]

FONT = pygame.font.SysFont(None, 26)
MOVE = 5

def draw():
    screen.fill((200, 220, 240))

    # Draw walls (as 2D top-down overlay for reference)
    for wall in walls:
        pygame.draw.rect(screen, (100,100,100), wall)

    # Sort objects by y for proper isometric layering
    objects = [banana, box, monkey, door]
    objects.sort(key=lambda obj: obj.rect.y + obj.height)
    for obj in objects:
        obj.draw(screen)

    info = FONT.render(
        "Arrows Move | P Push | C Climb | G Grab | R Reset",
        True, (0,0,0)
    )
    screen.blit(info, (20, 20))
    pygame.display.update()

def reset_game():
    global monkey_on_box, has_banana
    monkey.rect.topleft = (50, 350)
    box.rect.topleft = (350, 350)
    banana.rect.topleft = (380, 120)
    monkey.height = 0
    monkey_on_box = False
    has_banana = False

# Collision check helper
def check_collision(rect):
    for wall in walls:
        if rect.colliderect(wall):
            return True
    return False

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx = -MOVE
    if keys[pygame.K_RIGHT]:
        dx = MOVE
    if keys[pygame.K_UP]:
        dy = -MOVE
    if keys[pygame.K_DOWN]:
        dy = MOVE

    # Push box and stick monkey
    if keys[pygame.K_p] and monkey.rect.colliderect(box.rect) and not monkey_on_box:
        # Try moving box
        box.rect.x += dx
        box.rect.y += dy
        if check_collision(box.rect):
            box.rect.x -= dx
            box.rect.y -= dy
            dx = dy = 0
        # Monkey sticks to box
        monkey.rect.x += dx
        monkey.rect.y += dy
    else:
        # Move monkey normally
        monkey.rect.x += dx
        monkey.rect.y += dy
        if check_collision(monkey.rect):
            monkey.rect.x -= dx
            monkey.rect.y -= dy

    # Climb box
    if keys[pygame.K_c] and monkey.rect.colliderect(box.rect):
        monkey_on_box = True
        monkey.height = 50  # visually above box

    # Grab banana
    if keys[pygame.K_g] and monkey_on_box and monkey.rect.colliderect(banana.rect):
        has_banana = True
        monkey.image = monkey_banana_img

    # Reset game
    if keys[pygame.K_r]:
        reset_game()
        monkey.image = monkey_img

    # End game if monkey with banana touches door
    if has_banana and monkey.rect.colliderect(door.rect):
        screen.fill((0,0,0))
        msg = FONT.render("Monkey got the banana! Game Ends!", True, (255,255,0))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    draw()
