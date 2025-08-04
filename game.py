import pgzrun
from random import randint
from pygame import Rect

WIDTH = 800
HEIGHT = 600
ENEMY_SPAWN_INTERVAL_MIN = 2.5
ENEMY_SPAWN_INTERVAL_MAX = 4.0
enemy_spawn_interval = 3.0
COIN_SPAWN_INTERVAL = 1.0

game_state = 'menu'
score = 0
enemy_speed_multiplier = 1.0
last_coin_spawn_time = 0
last_enemy_spawn_time = 0
music_enabled = True
sounds_enabled = True

class GameObject:
    def __init__(self, image, x, y, velocity_x=0, velocity_y=0):
        self.actor = Actor(image, (x, y))
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def update(self, dt):
        self.actor.x += self.velocity_x * dt
        self.actor.y += self.velocity_y * dt

class Hero(GameObject):
    def __init__(self, x, y):
        super().__init__('heroi_parado', x, y)
        self.run_speed = 200
        self.jump_speed = 350
        self.gravity = 700
        self.velocity_y = 0
        self.on_ground = False
        self.anim_state = 'idle'
        self.anim_sprites = {
            'idle': 'heroi_parado',
            'running': 'heroi_correndo'
        }

    def update(self, dt):
        self.velocity_x = 0
        self.anim_state = 'idle'

        if keyboard.right or keyboard.left:
            self.velocity_x = self.run_speed if keyboard.right else -self.run_speed
            self.anim_state = 'running'

        if keyboard.up and self.on_ground:
            self.velocity_y = -self.jump_speed
            self.on_ground = False
            if sounds_enabled:
                sounds.jump.play()

        self.velocity_y += self.gravity * dt
        self.actor.x += self.velocity_x * dt
        self.actor.y += self.velocity_y * dt

        self.actor.left = max(0, self.actor.left)
        self.actor.right = min(WIDTH, self.actor.right)

        for platform in platforms:
            self.check_platform_collision(platform)

        self.actor.image = self.anim_sprites[self.anim_state]

    def check_platform_collision(self, platform):
        if self.actor.colliderect(platform.actor):
            if self.velocity_y > 0 and self.actor.bottom <= platform.actor.top + 20:
                self.actor.bottom = platform.actor.top
                self.velocity_y = 0
                self.on_ground = True

class Enemy(GameObject):
    def __init__(self, x, y, velocity_x):
        super().__init__('inimigo1', x, y, velocity_x, 0)
        self.last_anim_frame_time = 0
        self.anim_frame = 0
        self.anim_frame_rate = 0.2
        self.anim_sprites = ['inimigo1', 'inimigo2']

    def update(self, dt):
        super().update(dt)
        self.last_anim_frame_time += dt
        if self.last_anim_frame_time > self.anim_frame_rate:
            self.anim_frame = (self.anim_frame + 1) % len(self.anim_sprites)
            self.actor.image = self.anim_sprites[self.anim_frame]
            self.last_anim_frame_time = 0

class Coin(GameObject):
    def __init__(self, x, y):
        super().__init__('moeda1', x, y, -50, 0)
        self.last_anim_frame_time = 0
        self.anim_frame = 0
        self.anim_frame_rate = 0.1
        self.anim_sprites = ['moeda1', 'moeda2']

    def update(self, dt):
        super().update(dt)
        self.last_anim_frame_time += dt
        if self.last_anim_frame_time > self.anim_frame_rate:
            self.anim_frame = (self.anim_frame + 1) % len(self.anim_sprites)
            self.actor.image = self.anim_sprites[self.anim_frame]
            self.last_anim_frame_time = 0

platforms = [
    GameObject('plataforma', WIDTH / 2, 500)
]

hero = Hero(100, platforms[0].actor.top - 40)
hero.on_ground = True

enemies = []
coins = []

start_button = Rect(WIDTH / 2 - 100, 250, 200, 50)
quit_button = Rect(WIDTH / 2 - 100, 350, 200, 50)
music_button = Rect(WIDTH / 2 - 100, 450, 200, 50)

background = Actor('fundo', (WIDTH / 2, HEIGHT / 2))
menu_background = Actor('menu_fundo', (WIDTH / 2, HEIGHT / 2))

def create_enemy():
    global last_enemy_spawn_time, enemy_spawn_interval
    x = WIDTH + 50
    y = platforms[0].actor.top - 20
    speed = -100 * enemy_speed_multiplier
    enemies.append(Enemy(x, y, speed))
    last_enemy_spawn_time = 0
    enemy_spawn_interval = randint(int(ENEMY_SPAWN_INTERVAL_MIN * 100), int(ENEMY_SPAWN_INTERVAL_MAX * 100)) / 100

def create_coin():
    global last_coin_spawn_time
    x = WIDTH + 50
    y_min = platforms[0].actor.top - 120
    y_max = platforms[0].actor.top - 50
    y = randint(y_min, y_max)
    coins.append(Coin(x, y))
    last_coin_spawn_time = 0

def toggle_music():
    global music_enabled
    music_enabled = not music_enabled
    if music_enabled:
        music.play('background_music')
    else:
        music.stop()

def on_mouse_down(pos):
    global game_state, score, enemy_speed_multiplier, last_coin_spawn_time, last_enemy_spawn_time, enemies, coins
    if game_state == 'menu':
        if start_button.collidepoint(pos):
            game_state = 'playing'
            score = 0
            enemies = []
            coins = []
            hero.actor.pos = (100, platforms[0].actor.top - 40)
            hero.on_ground = True
            enemy_speed_multiplier = 1.0
            last_coin_spawn_time = 0
            last_enemy_spawn_time = 0
            if music_enabled:
                music.play('background_music')
        elif quit_button.collidepoint(pos):
            exit()
        elif music_button.collidepoint(pos):
            toggle_music()

def on_key_down(key):
    global game_state, score, enemies, coins, enemy_speed_multiplier
    if game_state in ['game_over', 'win'] and key == keys.ESCAPE:
        game_state = 'menu'
        score = 0
        enemies = []
        coins = []
        hero.actor.pos = (100, platforms[0].actor.top - 40)
        hero.on_ground = True
        enemy_speed_multiplier = 1.0
        music.stop()

def update(dt):
    global game_state, score, enemy_speed_multiplier, last_coin_spawn_time, last_enemy_spawn_time

    if game_state == 'playing':
        hero.update(dt)

        last_enemy_spawn_time += dt
        if last_enemy_spawn_time > enemy_spawn_interval:
            create_enemy()

        last_coin_spawn_time += dt
        if last_coin_spawn_time > COIN_SPAWN_INTERVAL:
            create_coin()

        for enemy in enemies[:]:
            enemy.update(dt)
            if hero.actor.colliderect(enemy.actor):
                game_state = 'game_over'
            if enemy.actor.x < -100:
                enemies.remove(enemy)

        for coin in coins[:]:
            coin.update(dt)
            if hero.actor.colliderect(coin.actor):
                coins.remove(coin)
                score += 1
                if score > 0 and score % 5 == 0:
                    enemy_speed_multiplier += 0.2
                if sounds_enabled:
                    sounds.moeda.play()
                if score >= 50:
                    game_state = 'win'
                    music.stop()
            elif coin.actor.x < -100:
                coins.remove(coin)

def draw():
    screen.clear()
    if game_state == 'menu':
        menu_background.draw()
        screen.draw.text("Aventura do Colecionador", center=(WIDTH / 2, 150), fontsize=80, color='black')
        screen.draw.filled_rect(start_button, 'green')
        screen.draw.text("Comecar Jogo", center=start_button.center, fontsize=30, color='black')
        screen.draw.filled_rect(quit_button, 'red')
        screen.draw.text("Encerrar", center=quit_button.center, fontsize=30, color='black')
        music_text = "Som: LIGADO" if music_enabled else "Som: DESLIGADO"
        screen.draw.filled_rect(music_button, 'blue')
        screen.draw.text(music_text, center=music_button.center, fontsize=30, color='white')

    elif game_state == 'playing':
        background.draw()
        for platform in platforms:
            platform.actor.draw()
        hero.actor.draw()
        for enemy in enemies:
            enemy.actor.draw()
        for coin in coins:
            coin.actor.draw()
        screen.draw.text(f"Moedas: {score}", topleft=(10, 10), fontsize=30, color='red')

    elif game_state == 'game_over':
        background.draw()
        screen.draw.text("Fim do Jogo", center=(WIDTH / 2, HEIGHT / 2 - 50), fontsize=60, color='red')
        screen.draw.text(f"Voce pegou: {score} moedas", center=(WIDTH / 2, HEIGHT / 2 + 20), fontsize=40, color='yellow')
        screen.draw.text("Pressione ESC para retornar ao menu", center=(WIDTH / 2, HEIGHT / 2 + 80), fontsize=20, color='black')

    elif game_state == 'win':
        background.draw()
        screen.draw.text("VOCE VENCEU!!!", center=(WIDTH / 2, HEIGHT / 2 - 50), fontsize=60, color='yellow')
        screen.draw.text(f"Voce pegou {score} moedas!", center=(WIDTH / 2, HEIGHT / 2 + 20), fontsize=40, color='white')
        screen.draw.text("Pressione ESC para retornar ao menu", center=(WIDTH / 2, HEIGHT / 2 + 80), fontsize=20, color='black')

pgzrun.go()