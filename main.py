import pgzrun
import random

WIDTH = 1280
HEIGHT = 720


class Character(Actor):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.x = x
        self.y = y
        self.original_x = 0
        self.original_y = 0
        self.gravity = 0
        self.velocity_y = 0
        self.velocity_x = 2
        self.on_ground = False
        self.run_img_right = []
        self.run_img_left = []
        self.current_frame = 0
        self.animation_speed = 0.6
        self.moving = False
        self.jumping = False
        self.flip = False
        self.life = 3

    def reset_moviment(self):
        self.moving = False

    def limit_moviment(self, WIDTH):
        if self.x < 30 or self.x > WIDTH - 30:
            self.x = self.original_x

    def move_right(self, WIDTH):
        self.flip = False
        self.x += self.velocity_x
        self.moving = True
        self.limit_moviment(WIDTH)

    def move_left(self, WIDTH):
        self.flip = True
        self.x -= self.velocity_x
        self.moving = True
        self.limit_moviment(WIDTH)

    def update_position(self):
        self.original_x = self.x
        self.original_y = self.y

    def apply_gravity(self, value):
        self.velocity_y += value
        self.y += self.velocity_y

    def check_ground_collision(self, jump_img, character_y, grounds, ground_y):
        for ground in grounds:
            if self.colliderect(ground):
                if self.velocity_y > 0 and self.y < ground.y:
                    self.y = ground.y - ground_y
                    self.velocity_y = 0
                    self.on_ground = True

        if self.y > character_y:
            self.y = character_y
            self.velocity_y = 0
            self.on_ground = True
        if not self.on_ground:
            self.image = jump_img

    def jump(self, y):
        self.velocity_y = y
        self.on_ground = False

        if not self.on_ground:
            self.image = 'p_jump__004'

    def reset_life(self, value):
        self.life = value

    def remove_life(self, enemy_list, damage, reset_x, reset_y):
        for enemy in enemy_list:
            if self.colliderect(enemy) or self.y > HEIGHT:
                self.x = reset_x
                self.y = reset_y
                self.life -= damage

    def update_animation(self, idle_image, jump_right, jump_left):
        if self.moving:
            self.current_frame += self.animation_speed
            if self.flip:
                if self.current_frame > len(self.run_img_left):
                    self.current_frame = 0

                self.image = self.run_img_left[int(self.current_frame)]
            else:
                if self.current_frame > len(self.run_img_right):
                    self.current_frame = 0

                self.image = self.run_img_right[int(self.current_frame)]

        else:
            self.image = idle_image

        if not self.on_ground:
            if self.flip:
                self.image = jump_left
            else:
                self.image = jump_right

    def load_run_sprites(self, prefix, default, sufix, frame_start, frame_end):
        run_images = []
        for frame in range(frame_start, frame_end):
            sprite_name = f"{prefix}{default}{frame}{sufix}"
            run_images.append(sprite_name)

        if 'left' in sufix:
            self.run_img_left = run_images
        else:
            self.run_img_right = run_images


class Enemy(Character):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.move_count = 0
        self.animation_speed = 0.2
        self.velocity_x = 1.2

    def ai_moviment(self, move):
        choice = random.randint(1, 3)
        if self.move_count > 0:
            self.update_position()
            self.move_count = self.move_count - 1

            if self.move_count < move / 2:
                self.move_right(WIDTH)

            else:
                self.move_left(WIDTH)
        elif choice == 1:
            self.move_count = move
        else:
            self.jump(-10)


class Dino(Enemy):
    def __init__(self, x, y):
        super().__init__("dino_idle1_left", x, y)
        self.load_run_sprites('dino', '_run', '', 1, 8)
        self.load_run_sprites('dino', '_run', '_left', 1, 8)

    def update(self, grounds):
        self.reset_moviment()
        self.ai_moviment(200)
        self.apply_gravity(0.5)
        self.update_animation('dino_idle1_left', 'dino_jump5', 'dino_jump5_left')
        self.check_ground_collision('dino_jump5_left', 676, grounds, 39)


player = Character("p_idle__000", 30, 550)
player.load_run_sprites('p', '_run__00', '', 0, 9)
player.load_run_sprites('p', '_run__00', '_left', 0, 9)


class Stage:
    def __init__(self):
        self.enemy_list = []
        self.position_enemy = [750, 500, 250, 1000]
        self.grounds = []

    def generate_stage(self, level):
        for index in range(level):
            enemy = Dino(self.position_enemy[index], 600)
            self.enemy_list.append(enemy)

        for x in range(40):
            ground = Actor("ground")
            ground.x = x * 32 + 16
            ground.y = HEIGHT - 7
            self.grounds.append(ground)


stage = Stage()
stage.generate_stage(4)


def update():
    player.update_position()
    player.reset_moviment()

    if keyboard.right:
        player.move_right(WIDTH)

    if keyboard.left:
        player.move_left(WIDTH)

    player.apply_gravity(0.5)

    player.check_ground_collision("p_jump__004", 1000, stage.grounds, 46)

    player.update_animation('p_idle__000', 'p_jump__004', 'p_jump__004_left')
    for enemy in stage.enemy_list:
        enemy.update(stage.grounds)

    player.remove_life(stage.enemy_list, 1, 32, 660)


def on_key_down(key):
    if key == key.SPACE and player.on_ground:
        player.jump(-10.3)
    if key == key.F5 and player.life == 0:
        player.reset_life(3)


def draw():
    screen.fill((167, 201, 225))

    for enemy in stage.enemy_list:
        enemy.draw()

    for ground in stage.grounds:
        ground.draw()

    if player.life > 0:
        player.draw()
        screen.draw.text(" LIFE: " + str(player.life), [30, 30], color=(0, 0, 0), fontsize=40)

    else:
        screen.draw.text("GAME OVER!", [WIDTH / 4, HEIGHT / 2], color=(0, 0, 0), fontsize=120)
        screen.draw.text("Aperte F5 para reiniciar", [WIDTH / 4, HEIGHT / 2 + 100], color=(0, 0, 0), fontsize=60)


pgzrun.go()



