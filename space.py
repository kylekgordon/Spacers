import pygame
import random

pygame.init()
timer = pygame.time.Clock()
fps = 60

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Rock Game")

# Color library
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Set up the fonts
# small_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 50)
# smaller_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 30)
# big_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 75)
# bigger_font = pygame.font.Font(r'assets/misc/Roboto-Bold.ttf', 90)

class Spaceship(pygame.sprite.Sprite):
    MANEUVERABILITY = 3

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/space_ship8.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speed = 5
        self.speed_x = 0
        self.speed_y = 0
    
    def move(self, direction):
        if direction == "left":
            self.speed_x -= 5
        elif direction == "right":
            self.speed_x += 5
        elif direction == "up":
            self.speed_y -= 5
        elif direction == "down":
            self.speed_y += 5

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        self.angle = self.MANEUVERABILITY * sign
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

class SpaceRock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/asteroid.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 8)
    
    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > height + 10:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)


# NEW_SPACE_ROCK = pygame.USEREVENT + 1
# pygame.time.set_timer(NEW_SPACE_ROCK, 1000)
background = pygame.image.load("sprites/BackgroundSupernova.png")
background_width = background.get_width()
background_height= background.get_height()
background_x = 0
background_y = 0

#Adding the spaceship and the space rock to the sprite groups
space1 = Spaceship()
spaceship = pygame.sprite.Group()
spaceship.add(space1)            
new_rock = SpaceRock()
space_rock_group = pygame.sprite.Group()
space_rock_group.add(new_rock)


running = True
while running:
    timer.tick(fps)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                space1.move("left")
            elif event.key == pygame.K_RIGHT:
                space1.move("right")
            elif event.key == pygame.K_UP:
                space1.move("up")
            elif event.key == pygame.K_DOWN:
                space1.move("down")
        # elif event.type == NEW_SPACE_ROCK:

    # Scroll the map
    # background_x -= 5
    # if background_x < -background.get_width():
    #     background_x = 0

    # Scroll the map based on the player position
    if space1.rect.x > screen.get_width() / 2:
        background_x -= space1.speed
    if space1.rect.x < screen.get_width() / 2:
        background_x += space1.speed
    if space1.rect.y > screen.get_height() / 2:
        background_y -= space1.speed
    elif space1.rect.y < screen.get_height() / 2:
        background_y += space1.speed

    # Keep the map within bounds
    if background_x < -background.get_width() + screen.get_width():
        background_x = -background.get_width() + screen.get_width()
    if background_x > 0:
        background_x = 0
    if background_y < -background.get_height() + screen.get_height():
        background_y = -background.get_height() + screen.get_height()
    elif background_y > 0:
        background_y = 0

    screen.blit(background, (background_x, background_y))

    spaceship.draw(screen)
    space_rock_group.draw(screen)

    spaceship.update()
    space_rock_group.update()

    pygame.display.update()


pygame.quit()
exit()
