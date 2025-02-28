import pygame
import os
import sys

# Инициализация Pygame
pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 550, 550
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((255, 255, 255))
FPS = 50


def load_image(file_name, colorkey=None):
    full_path = os.path.join(file_name)
    if not os.path.isfile(full_path):
        print(f"Файл изображения '{full_path}' не найден")
        sys.exit()
    img = pygame.image.load(full_path)
    if colorkey is not None:
        img = img.convert()
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey)
    else:
        img = img.convert_alpha()
    return img


def exit_game():
    pygame.quit()
    sys.exit()


def read_level(file_path):
    if not os.path.isfile(file_path):
        print(f"Файл уровня '{file_path}' не найден")
        sys.exit()
    with open(file_path, 'r') as file:
        level_data = [line.strip() for line in file]
    max_length = max(map(len, level_data))
    return [line.ljust(max_length, '.') for line in level_data]


def display_start_screen():
    intro_lines = ["ДОБРО ПОЖАЛОВАТЬ", "",
                   "Правила игры",
                   "Если в правилах несколько строк,",
                   "они будут отображаться по одной"]

    background = pygame.transform.scale(load_image('fon.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    y_offset = 50
    for line in intro_lines:
        rendered_text = font.render(line, 1, pygame.Color('black'))
        text_rect = rendered_text.get_rect()
        y_offset += 10
        text_rect.top = y_offset
        text_rect.x = 10
        y_offset += text_rect.height
        screen.blit(rendered_text, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


display_start_screen()

# Загрузка изображений
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

TILE_SIZE = 50
player_instance = None

all_sprites = pygame.sprite.Group()
tiles = pygame.sprite.Group()
players = pygame.sprite.Group()

# Чтение уровня
level_file = input("Введите путь к файлу уровня: ")
level_data = read_level(level_file)


class GameTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(tiles, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(TILE_SIZE * x, TILE_SIZE * y)


class GamePlayer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(players, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(TILE_SIZE * x + 15, TILE_SIZE * y + 5)
        self.position = (x, y)

    def move(self, x, y):
        self.rect = self.image.get_rect().move(TILE_SIZE * x + 15, TILE_SIZE * y + 5)
        self.position = (x, y)


def handle_movement(player, direction):
    x, y = player.position
    if direction == 'up' and y > 0 and level_data[y - 1][x] == '.':
        player.move(x, y - 1)
    elif direction == 'down' and y < len(level_data) - 1 and level_data[y + 1][x] == '.':
        player.move(x, y + 1)
    elif direction == 'right' and x < len(level_data[y]) - 1 and level_data[y][x + 1] == '.':
        player.move(x + 1, y)
    elif direction == 'left' and x > 0 and level_data[y][x - 1] == '.':
        player.move(x - 1, y)


def create_level(level):
    new_player, player_x, player_y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                GameTile('empty', x, y)
            elif level[y][x] == '#':
                GameTile('wall', x, y)
            elif level[y][x] == '@':
                GameTile('empty', x, y)
                new_player = GamePlayer(x, y)
    return new_player, player_x, player_y


player_instance, level_x, level_y = create_level(level_data)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                handle_movement(player_instance, 'up')
            elif event.key == pygame.K_DOWN:
                handle_movement(player_instance, 'down')
            elif event.key == pygame.K_RIGHT:
                handle_movement(player_instance, 'right')
            elif event.key == pygame.K_LEFT:
                handle_movement(player_instance, 'left')

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    players.draw(screen)
    pygame.display.flip()

pygame.quit()