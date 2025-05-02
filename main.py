import pgzrun

WIDTH = 1320
HEIGHT = 600

class Character(Actor):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.x = x
        self.y = y
        self.original_x = 0
        self.origial_y = 0
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
        

    def limit_moviment(self, WIDTH):
         if self.x < 30 or self.x > WIDTH -30:
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

    def check_ground_collision(self, jump_img):
         if self.y > 550:
            self.y = 550
            self.velocity_y = 0
            self.on_ground = True
         if not self.on_ground:
            self.image = jump_img

    def jump(self):
         self.velocity_y = -10
         self.on_ground = False 

         if not self.on_ground:
            self.image = 'p_jump__004'

    def update_animation(self, idle_image, jump_right, jump_left):
         if self.moving:
             self.current_frame += self.animation_speed
             if self.flip :
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

player = Character("p_idle__000",30, 550)
player.run_img_right = ["p_run__000", "p_run__001", "p_run__002", "p_run__003", "p_run__004", "p_run__005", "p_run__006", "p_run__007", "p_run__008", "p_run__009"]
player.run_img_left = ["p_run__000_left", "p_run__001_left", "p_run__002_left", "p_run__003_left", "p_run__004_left", "p_run__005_left", "p_run__006_left", "p_run__007_left", "p_run__008_left", "p_run__009_left"]

def update():
    player.update_position()
    player.moving = False

    if keyboard.right:
            player.move_right(WIDTH)

    if keyboard.left:
            player.move_left(WIDTH)

    player.apply_gravity(0.5)
    
    player.check_ground_collision("p_jump__004")

    player.update_animation('p_idle__000', 'p_jump__004', 'p_jump__004_left')  

def on_key_down(key):
     if key == key.SPACE and player.on_ground:
        player.jump()

def draw():
    screen.fill((255,255,255))
    player.draw()

pgzrun.go()

