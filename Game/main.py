import pygame  # імпорт бібліотеки для створення ігор
import random  #  імпорт генератора рандомних чисел
import os  # імпорт модуля для роботи із ОС

# імпортуємо константу для виходу із вікна гри і бібліотеки pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

# запускаємо бібліотеку pygame
pygame.init()
FPS = pygame.time.Clock()  # швидкість руху гравця

# Задаємо розміри екрану
HEIGTH = 800
WIDTH = 1200
FIELD_COLOR = (0, 0, 0)
img_background = pygame.image.load("./img/background.png")  # завантаження картинки фону
BG = pygame.transform.scale(
    img_background, (WIDTH, HEIGTH)
)  # вписування картинки фону у екран
bg_X1 = 0  # координата початку першої картинки
bg_X2 = BG.get_width()  # координата початку другої картинки
bg_move = 3  # швидкість руху картинки
main_display = pygame.display.set_mode((WIDTH, HEIGTH))

# створюємо інтерактивного гусака
IMAGE_PATH = "./img/goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
print(PLAYER_IMAGES)
CHANGE_IMAGES = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGES, 200)

# задаємо шрифт для системи
FONT = pygame.font.SysFont("Verdana", 20)
FONT_COLOR = (0, 0, 0)

# Create player
PLAYER_COLOR = (0, 0, 0)
PLAYER_SIZE = (20, 20)
player = pygame.image.load("./img/player.png").convert_alpha()  # розмір гравця
# player_coordinates = player.get_rect()  # координати розмішення гравця, на початку гри
player_coordinates = pygame.Rect(
    0, HEIGTH / 2, *PLAYER_SIZE
)  # координати розмішення гравця, на початку гри
player_move_up = [0, -4]
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_left = [-4, 0]

# Create enemy
ENEMY_COLOR = (0, 0, 255)
ENEMY_SIZE = (30, 30)


# Створюємо функцію для створення ворогів
def create_enemy():
    enemy = pygame.image.load("./img/enemy.png").convert_alpha()
    enemy_coordinates = pygame.Rect(
        WIDTH, random.randint(100, HEIGTH - 100), *ENEMY_SIZE
    )
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_coordinates, enemy_move]


CREATE_ENEMY = pygame.USEREVENT + 1  # кількість ворогів
pygame.time.set_timer(CREATE_ENEMY, 1500)  # інтервал створення ворогів

enemies = []  # для зберігання створених ворогів

# Створюємо бонуси
BONUS_COLOR = (255, 0, 0)
BONUS_SIZE = (30, 30)


# Створюємо функцію для створення бонусів
def create_bonus():
    bonus = pygame.image.load("./img/bonus.png").convert_alpha()
    bonus_coordinates = pygame.Rect(random.randint(100, WIDTH - 100), 0, *BONUS_SIZE)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_coordinates, bonus_move]


CREATE_BONUS = pygame.USEREVENT + 2  # кількість бонусів
pygame.time.set_timer(CREATE_BONUS, 2500)  # інтервал створення ворогів

bonuses = []  # для зберігання створених бонусів

# Створюємо подію, яка відповідає за закриттся гри
playing = True

# Набарні бали
score = 0

image_index = 0

while playing:
    FPS.tick(300)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMAGES:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1

            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -BG.get_width():
        bg_X1 = BG.get_width()

    if bg_X2 < -BG.get_width():
        bg_X2 = BG.get_width()

    main_display.blit(BG, (bg_X1, 0))  # створюємо задній фон зони гри
    main_display.blit(BG, (bg_X2, 0))  # створюємо задній фон зони гри

    key = pygame.key.get_pressed()  # визначаємо яка клавіша була натиснена

    # Створюємо керування гравцем
    if key[K_UP] and player_coordinates.top > 0:
        player_coordinates = player_coordinates.move(player_move_up)

    if key[K_DOWN] and player_coordinates.bottom < HEIGTH:
        player_coordinates = player_coordinates.move(player_move_down)

    if key[K_RIGHT] and player_coordinates.right < WIDTH:
        player_coordinates = player_coordinates.move(player_move_right)

    if key[K_LEFT] and player_coordinates.left > 0:
        player_coordinates = player_coordinates.move(player_move_left)

    # розмішення ворогів
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        # відслідковуємо стикання об`єктів
        if player_coordinates.colliderect(enemy[1]):
            playing = False  # закінчуємо гру

    # розмішення бонусів
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        # відслідковуємо стикання об`єктів
        if player_coordinates.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(player, player_coordinates)  # розмішення гравця на полі
    main_display.blit(
        FONT.render(str(score), True, FONT_COLOR), (WIDTH - 50, 20)
    )  # виведення зароблених балів на екран

    pygame.display.flip()  # оновлення екрану гри

    # видалення ворогів, які вже пройшли по екрану
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    # видалення бонусів, які вже пройшли по екрану
    for bonus in bonuses:
        if bonus[1].bottom > HEIGTH:
            bonuses.pop(bonuses.index(bonus))
