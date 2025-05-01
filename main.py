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
        self.run_images = []
        self.current_frame = 0
        self.animation_speed = 0.6
        self.moving = False
        self.jumping = False
        

    def limit_moviment(self, WIDTH):
         if self.x < 30 or self.x > WIDTH -30:
            self.x = self.original_x

    def move_right(self, WIDTH):
        self.x += self.velocity_x
        self.moving = True  
        self.limit_moviment(WIDTH)

    def move_left(self, WIDTH):
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

    def update_animation(self, idle_image):
         if self.moving:
             self.current_frame += self.animation_speed
             if self.current_frame > len(self.run_images):
                self.current_frame = 0

             self.image = self.run_images[int(self.current_frame)]
    
         else:
             self.image = idle_image

         if not self.on_ground:
             self.image = 'p_jump__004'

player = Character("p_idle__000",30, 550)
player.run_images = ["p_run__000", "p_run__001", "p_run__002", "p_run__003", "p_run__004", "p_run__005", "p_run__006", "p_run__007", "p_run__008", "p_run__009"]

def update():
    player.update_position()
    player.moving = False

    if keyboard.right:
            player.move_right(WIDTH)

    if keyboard.left:
            player.move_left(WIDTH)

    player.apply_gravity(0.5)
    
    player.check_ground_collision("p_jump__004")

    player.update_animation('p_idle__000')  

def on_key_down(key):
     if key == key.SPACE and player.on_ground:
        player.jump()

def draw():
    screen.fill((255,255,255))
    player.draw()

pgzrun.go()

