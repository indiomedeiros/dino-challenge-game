import pgzrun
import random


WIDTH = 1280
HEIGHT = 720
TITLE = "Ninja Dino Challenge"

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
        self.idle_img_list = []
        self.current_frame = 0
        self.current_frame_idle = 0
        self.animation_speed = 0.6
        self.animation_speed_idle = 0.04
        self.moving = False
        self.jumping = False
        self.flip = False
        self.life = 5

    def reset_moviment(self):
        self.moving = False

    def limit_moviment(self, width):
        if self.x < 30 or self.x > width - 30:
            self.x = self.original_x

    def move_right(self, width):
        self.flip = False
        self.x += self.velocity_x
        self.moving = True
        self.limit_moviment(width)

    def move_left(self, width):
        self.flip = True
        self.x -= self.velocity_x
        self.moving = True
        self.limit_moviment(width)

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

    def reset_game(self, life):
        self.life = life
        self.x = 30

    def remove_life(self, enemy_list, damage, reset_x, reset_y):
        for enemy in enemy_list:
            if self.colliderect(enemy) or self.y > HEIGHT:
                sounds.damage.play()
                self.x = reset_x
                self.y = reset_y
                self.life -= damage

    def update_animation(self, jump_right, jump_left):
        if self.moving:
            #running character animation
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
            #animation of the character standing still and breathing
            self.current_frame_idle += self.animation_speed_idle
            if self.current_frame_idle > len(self.idle_img_list):
                self.current_frame_idle = 0
            else:
                self.image = self.idle_img_list[int(self.current_frame_idle)]

        if not self.on_ground:
            #changes the direction of the jump
            if self.flip:
                self.image = jump_left
            else:
                self.image = jump_right

    def load_sprites(self, prefix, default, sufix, frame_start, frame_end):
        images = []
        for frame in range(frame_start, frame_end):
            sprite_name = f"{prefix}{default}{frame}{sufix}"
            images.append(sprite_name)
        
        if "idle" in default:
            self.idle_img_list = images
        elif 'left' in sufix:
            self.run_img_left = images
        else:
            self.run_img_right = images


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
        self.load_sprites('dino', '_run', '', 1, 8)
        self.load_sprites('dino', '_run', '_left', 1, 8)

    def update(self, grounds):
        self.reset_moviment()
        self.ai_moviment(200)
        self.apply_gravity(0.5)
        self.update_animation('dino_jump5', 'dino_jump5_left')
        self.check_ground_collision('dino_jump5_left', 676, grounds, 39)


class Stage:
    def __init__(self):
        self.enemy_list = []
        self.position_enemy = [750, 500, 250, 1000, 900, 350]
        self.grounds = []
        self.complete = False
        self.level = 2  # Changes the stage level, reaching up to number 5

    def generate_stage(self):
        for index in range(self.level):
            enemy = Dino(self.position_enemy[index], 600)
            self.enemy_list.append(enemy)

        for x in range(40):
            ground = Actor("ground")
            ground.x = x * 32 + 16
            ground.y = HEIGHT - 7
            self.grounds.append(ground)

        self.finish = Actor('flag_finish', (WIDTH - 64, 662))


# Inicialização do jogo
stage = Stage()

game_state = "menu"
stage.generate_stage()
option_selected = 0
sounds.background_intro.play(-1)

player = Character("p_idle__000", 30, 550)
player.load_sprites('p', '_run__00', '', 0, 9)
player.load_sprites('p', '_run__00', '_left', 0, 9)
player.load_sprites('p', '_idle__00','', 0, 2)


def update():
    player.update_position()
    player.reset_moviment()

    if keyboard.right:
        player.move_right(WIDTH)

    if keyboard.left:
        player.move_left(WIDTH)

    player.apply_gravity(0.5)
    player.check_ground_collision("p_jump__004", 1000, stage.grounds, 46)
    player.update_animation('p_jump__004', 'p_jump__004_left')
    
    for enemy in stage.enemy_list:
        enemy.update(stage.grounds)

    player.remove_life(stage.enemy_list, 1, 32, 660)

    if stage.finish.colliderect(player):
        sounds.game_win.play()
        stage.complete = True
        player.reset_game(3)


def on_key_down(key):
    global option_selected, game_state

    if key == keys.SPACE and player.on_ground:
        player.jump(-10.3)
    if key == keys.F5 and (player.life == 0 or stage.complete):
        player.reset_game(5)
        stage.complete = False
        sounds.play_game_sound.play()
        sounds.stage_one.play()
    if key == keys.ESCAPE:
        quit()

    if game_state == "menu":
        if key == keys.DOWN:
            sounds.menu_select_sound.play()
            option_selected = (option_selected + 1) % 2
        elif key == keys.UP:
            sounds.menu_select_sound.play()
            option_selected = (option_selected - 1) % 2

        if key == keys.RETURN:
            if option_selected == 0:
                sounds.background_intro.stop()
                sounds.play_game_sound.play()
                game_state = "scene_one"
                sounds.stage_one.play()
            elif option_selected == 1:
                quit()


def draw():
    screen.fill((140, 201, 225))
    for ground in stage.grounds:
        ground.draw()

    if game_state == "menu":
        screen.draw.text(
            "Iniciar o Game",
            color=(143, 75, 8) if option_selected == 0 else "black",
            center=(WIDTH/2, HEIGHT/2),
            fontsize=70 if option_selected == 0 else 50,
            fontname="title"
        )
        
        screen.draw.text(
            "SAIR",
            color=(143, 75, 8) if option_selected == 1 else "black",
            center=(WIDTH/2, HEIGHT/2 + 50),
            fontsize=70 if option_selected == 1 else 50,
            fontname="title"
        )
    else:
        for enemy in stage.enemy_list:
            enemy.draw()

        stage.finish.draw()

        if player.life > 0 and not stage.complete:
            sounds.game_win.stop()
            player.draw()
            screen.draw.text(
                " Vida = " + str(player.life),
                [30, 30], color="black", fontsize=60
            )
            screen.draw.text("""
                CONTROLES:
                Setas do teclado = Movimentar para esquerda/direita.
                Espaço  = Pular
                ESC = Sair do jogo

                OBJETIVO:
                Capture a bandeira!""",
                [0, 100], color="black", fontsize=20
            )
        elif stage.complete:
            screen.draw.text(
                "Parabéns, Vitória!",
                center=(WIDTH/2, HEIGHT/2),
                color="black",
                fontsize=120
            )
            screen.draw.text(
                "Aperte F5 para reiniciar",
                center=(WIDTH/2, HEIGHT/2 + 50),
                color="black",
                fontsize=40
            )
            sounds.stage_one.stop()
        else:
            screen.draw.text(
                "GAME OVER!",
                center=(WIDTH/2, HEIGHT/2),
                color="red",
                fontsize=120
            )
            screen.draw.text(
                "Aperte F5 para reiniciar",
                center=(WIDTH/2, HEIGHT/2 + 50),
                color="black",
                fontsize=40
            )
            sounds.stage_one.stop()


pgzrun.go()