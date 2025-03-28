import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
W, H = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake Game")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Настройки змейки
snake = [(100, 100), (90, 100), (80, 100)]  # Начальная позиция
snake_dir = (CELL_SIZE, 0)  # Начальное движение (вправо)

# Настройки еды
food = None
food_timer = 0
food_weight = 1
food_expiration = 300  # Время исчезновения еды (в кадрах)

def generate_food():
    global food_timer, food_weight
    while True:
        new_food = (random.randint(0, (W // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (H // CELL_SIZE) - 1) * CELL_SIZE)
        if new_food not in snake:  # Исключаем появление еды на змейке
            food_timer = food_expiration  # Сброс таймера еды
            food_weight = random.randint(1, 3)  # Генерация случайного веса еды
            return new_food

# Начальная генерация еды
food = generate_food()

# Настройки игры
score = 0
level = 1
speed = 10  # Начальная скорость игры

# Шрифты
font = pygame.font.SysFont("comicsansms", 20)

clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Управление змейкой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and snake_dir != (CELL_SIZE, 0):
        snake_dir = (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and snake_dir != (-CELL_SIZE, 0):
        snake_dir = (CELL_SIZE, 0)
    if keys[pygame.K_UP] and snake_dir != (0, CELL_SIZE):
        snake_dir = (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and snake_dir != (0, -CELL_SIZE):
        snake_dir = (0, CELL_SIZE)
    
    # Движение змейки
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    
    # Проверка на столкновение со стенами
    if new_head[0] < 0 or new_head[0] >= W or new_head[1] < 0 or new_head[1] >= H:
        running = False
    
    # Проверка на столкновение с собой
    if new_head in snake:
        running = False
    
    snake.insert(0, new_head)
    
    # Проверка на съедение еды
    if new_head == food:
        score += food_weight
        if score % 3 == 0:  # Уровень повышается каждые 3 очка
            level += 1
            speed += 2  # Увеличение скорости
        food = generate_food()
    else:
        snake.pop()
    
    # Таймер еды
    if food_timer > 0:
        food_timer -= 1
    else:
        food = generate_food()  # Перегенерация еды при истечении таймера
    
    # Отрисовка еды с разным цветом по весу
    food_color = RED if food_weight == 1 else BLUE if food_weight == 2 else WHITE
    pygame.draw.rect(screen, food_color, (food[0], food[1], CELL_SIZE, CELL_SIZE))
    
    # Отрисовка змейки
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    
    # Отображение счета и уровня
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
