import pygame
import random


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


game_over = False
food_eaten = False
flag = False
snake_len = 1
x1, y1 = 0, 0


class Food(pygame.sprite.Sprite):
    def __init__(self, radius):
        super().__init__(all_sprites)
        self.image = pygame.Surface((radius * 2, radius * 2),
                                    pygame.SRCALPHA)
        self.radius = radius
        self.x = random.randrange(radius * 2, width - radius * 2)
        self.y = random.randrange(radius * 2, height - radius * 2)
        pygame.draw.circle(self.image, (random.randrange(0, 255),
                                        random.randrange(0, 255),
                                        random.randrange(0, 255)), (radius, radius), radius)
        self.rect = pygame.Rect(self.x, self.y, radius * 2, radius * 2)
        self.add(food)

    def update(self, key):
        global food_eaten
        if food_eaten:
            pygame.draw.circle(self.image, (random.randrange(self.radius * 2, 255),
                                            random.randrange(self.radius * 2, 255),
                                            random.randrange(self.radius * 2, 255)),
                               (self.radius, self.radius), self.radius)
            self.rect = pygame.Rect(random.randrange(self.radius * 2, width - self.radius * 2),
                                    random.randrange(self.radius * 2, height - self.radius * 2),
                                    self.radius * 2, self.radius * 2)
            food_eaten = False


class Snake(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__(all_sprites)
        self.image = pygame.Surface((side, side),
                                    pygame.SRCALPHA)
        pygame.draw.rect(self.image, (200, 200, 200), (0, 0, side, side), 0)
        self.diff = side
        self.rect = pygame.Rect(width // 2 - side // 2, height // 2 - side // 2, side, side)

    def get_pos(self):
        return [self.rect.x, self.rect.y]

    def update(self, key):
        global game_over, food_eaten, snake_len, x1, y1
        if key == pygame.K_RIGHT:
            self.rect = self.rect.move(13, 0)
        elif key == pygame.K_LEFT:
            self.rect = self.rect.move(-13, 0)
        elif key == pygame.K_UP:
            self.rect = self.rect.move(0, -13)
        elif key == pygame.K_DOWN:
            self.rect = self.rect.move(0, 13)
        if pygame.sprite.spritecollideany(self, borders):
            game_over = True
        if pygame.sprite.spritecollideany(self, food):
            food_eaten = True
            snake_len += 1


while not game_over:
    all_sprites = pygame.sprite.Group()
    borders = pygame.sprite.Group()
    food = pygame.sprite.Group()
    side = 15

    snake = Snake(side)
    Food(7)

    Border(0, 0, width, 0)
    Border(0, height, width, height)
    Border(0, 0, 0, height)
    Border(width, 0, width, height)

    snakelist = []
    clock = pygame.time.Clock()

    running = True
    key = None
    old_key = key

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            if event.type == pygame.KEYDOWN:
                key = event.key
            if game_over:
                screen.fill((0, 0, 0))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    snakelist = []
                    snake_len = 1
                    game_over = False
                    running = False
                break
        screen.fill((0, 0, 0))
        snakelist.append(snake.get_pos())

        if key not in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            key = old_key
        else:
            old_key = key

        if len(snakelist) > snake_len:
            del snakelist[0]
        if snake.get_pos() in snakelist[:-1]:
            game_over = True
        for el in snakelist:
            if snakelist.index(el) > 0:
                pygame.draw.rect(screen, (200, 200, 200), [el[0], el[1], side, side])

        all_sprites.draw(screen)
        all_sprites.update(key)

        if game_over:
            screen.fill((255, 255, 255))
            font = pygame.font.SysFont(None, 50)
            text = font.render("Game Over", True, pygame.Color('red'))
            screen.blit(text, (width // 2 - text.get_width() // 2,
                               height // 2 - text.get_height()))
            text2 = font.render("Press R to Restart", True, pygame.Color('red'))
            screen.blit(text2, (width // 2 - text2.get_width() // 2,
                                height // 2 + text.get_height() // 2))
        else:
            font = pygame.font.SysFont(None, 30)
            text = font.render(f'Your Score: {snake_len - 1}', True, pygame.Color('green'))
            screen.blit(text, (0, 0))

        pygame.display.flip()
        pygame.time.Clock().tick(25)
pygame.quit()
