import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Halo")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Загрузка изображений
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (40, 40))
bonus_img = pygame.image.load("bonus.png")
bonus_img = pygame.transform.scale(bonus_img, (30, 30))


# Игровые состояния
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
game_state = STATE_MENU  # Начинаем с меню

# Класс игрока
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 70
        self.width = 50
        self.height = 50
        self.speed = 7
        self.lives = 3  

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        self.x = max(0, min(self.x, WIDTH - self.width))
        self.y = max(0, min(self.y, HEIGHT - self.height))

    def draw(self):
        screen.blit(player_img, (self.x, self.y))

# Класс пули игрока
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.width = 5
        self.height = 15

    def move(self):
        self.y -= self.speed  

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

# Класс пули врага
class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.width = 5
        self.height = 15

    def move(self):
        self.y += self.speed  

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

# Класс врага (НЛО)
class Enemy:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)  
        self.speed_x = random.choice([-2, 2])  
        self.width = 40
        self.height = 40
        self.change_direction_time = pygame.time.get_ticks() + random.randint(1000, 3000)  
        self.shoot_time = pygame.time.get_ticks() + random.randint(2000, 4000)  

    def move(self):
        self.y += self.speed_y  
        self.x += self.speed_x  

        if self.x < 0 or self.x > WIDTH - self.width:
            self.speed_x = -self.speed_x  

        if pygame.time.get_ticks() > self.change_direction_time:
            self.speed_x = random.choice([-2, 2])
            self.change_direction_time = pygame.time.get_ticks() + random.randint(1000, 3000)

    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))

    def shoot(self, enemy_bullets):
        if pygame.time.get_ticks() > self.shoot_time:
            enemy_bullets.append(EnemyBullet(self.x + self.width // 2, self.y + self.height))
            self.shoot_time = pygame.time.get_ticks() + random.randint(2000, 4000)

# Класс бонусного блока
class Bonus:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(-100, -40)
        self.speed = 2
        self.width = 30
        self.height = 30
        self.type = random.choice(["extra_life", "double_points", "fast_shooting"])  

    def move(self):
        self.y += self.speed  

    def draw(self):
        screen.blit(bonus_img, (self.x, self.y))

# Функция проверки столкновений
def check_collision(obj1, obj2):
    return (
        obj1.x < obj2.x + obj2.width and
        obj1.x + obj1.width > obj2.x and
        obj1.y < obj2.y + obj2.height and
        obj1.y + obj1.height > obj2.y
    )

# Создаём игрока и массивы объектов
player = Player()
bullets = []
enemy_bullets = []  
enemies = []
bonuses = []
score = 0  
double_points = False
fast_shooting = False
last_shot_time = 0

# Таймеры
enemy_spawn_time = pygame.time.get_ticks()
bonus_spawn_time = pygame.time.get_ticks()
font = pygame.font.Font(None, 36)  


bonus_end_time = {"double_points": 0, "fast_shooting": 0} 
# Проверяем, истекло ли время бонусов
current_time = time.time()
if current_time > bonus_end_time["double_points"]:
    double_points = False
if current_time > bonus_end_time["fast_shooting"]:
    fast_shooting = False

# Отображение активных бонусов
bonus_text_y = 100
if double_points:
    text = font.render("🔥 Double Points!", True, GREEN)
    screen.blit(text, (10, bonus_text_y))
    bonus_text_y += 30  # Сдвигаем вниз, если есть ещё бонусы

if fast_shooting:
    text = font.render("⚡ Fast Shooting!", True, GREEN)
    screen.blit(text, (10, bonus_text_y))


# Игровой цикл
running = True
clock = pygame.time.Clock()

# Функция для отрисовки текста
def draw_text(text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Главное меню
def show_menu():
    screen.fill(BLACK)
    draw_text("SPACE HALO", 64, WIDTH // 2 - 150, HEIGHT // 2 - 100)
    draw_text("Press ENTER to Start", 36, WIDTH // 2 - 120, HEIGHT // 2 + 20, GREEN)
    pygame.display.flip()

    # Экран "Game Over"
def show_game_over():
    screen.fill(BLACK)
    draw_text("GAME OVER", 64, WIDTH // 2 - 150, HEIGHT // 2 - 50)
    draw_text("Press R to Restart", 36, WIDTH // 2 - 120, HEIGHT // 2 + 20, RED)
    pygame.display.flip()

    # Функция сброса игры
def reset_game():
    global player, bullets, enemies, bonuses, score, game_state
    player = Player()
    bullets = []
    enemies = []
    bonuses = []
    score = 0
    game_state = STATE_PLAYING

    
while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == STATE_MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = STATE_PLAYING  # Начать игру

        elif game_state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()  # Перезапуск игры

        elif game_state == STATE_PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    current_time = pygame.time.get_ticks()
                    if fast_shooting or current_time - last_shot_time > 500:
                        bullets.append(Bullet(player.x + player.width // 2 - 2, player.y))
                        last_shot_time = current_time

    # Логика в зависимости от состояния игры
    if game_state == STATE_MENU:
        show_menu()

    elif game_state == STATE_PLAYING:
        player.move(keys)
        player.draw()

        # Генерация врагов
        if pygame.time.get_ticks() - enemy_spawn_time > random.randint(1500, 2500):
            enemies.append(Enemy())
            enemy_spawn_time = pygame.time.get_ticks()

        # Генерация бонусов
        if pygame.time.get_ticks() - bonus_spawn_time > random.randint(8000, 12000):
            bonuses.append(Bonus())
            bonus_spawn_time = pygame.time.get_ticks()

        # Обновляем пули игрока
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            if bullet.y < 0:
                bullets.remove(bullet)

        # Обновляем врагов
        for enemy in enemies[:]:
            enemy.move()
            enemy.draw()
            enemy.shoot(enemy_bullets)
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                player.lives -= 1

            for bullet in bullets[:]:
                if check_collision(bullet, enemy):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 20 if double_points else 10

        # Обновляем бонусы
        for bonus in bonuses[:]:
            bonus.move()
            bonus.draw()
        
            # Проверяем попадание пули в бонус
            for bullet in bullets[:]:
                if check_collision(bullet, bonus):
                    if bonus.type == "extra_life":
                        player.lives += 1  # 🔥 +1 жизнь
                    elif bonus.type == "double_points":
                        double_points = True
                        bonus_end_time["double_points"] = time.time() + 10  # 🔥 Бонус на 10 сек
                    elif bonus.type == "fast_shooting":
                        fast_shooting = True
                        bonus_end_time["fast_shooting"] = time.time() + 5  # 🔥 Бонус на 5 сек
                    
                    bullets.remove(bullet)  # Удаляем пулю
                    bonuses.remove(bonus)  # Удаляем бонус после попадания
                    break  # Выходим из цикла, чтобы избежать двойного удаления

        # Проверяем, истекло ли время бонусов
        current_time = time.time()
        if current_time > bonus_end_time["double_points"]:
            double_points = False
        if current_time > bonus_end_time["fast_shooting"]:
            fast_shooting = False

        # Отображение активных бонусов
        bonus_text_y = 100
        if double_points:
            draw_text("🔥 Double Points!", 36, 10, bonus_text_y, GREEN)
            bonus_text_y += 30  # 🔥 Сдвигаем вниз, если есть ещё бонусы
        if fast_shooting:
            draw_text("⚡ Fast Shooting!", 36, 10, bonus_text_y, GREEN)

        # Отображение очков и жизней
        draw_text(f"Score: {score}", 36, 10, 10)
        draw_text(f"Lives: {player.lives}", 36, 10, 50, RED)

        if player.lives <= 0:
            game_state = STATE_GAME_OVER
    elif game_state == STATE_GAME_OVER:
        show_game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()