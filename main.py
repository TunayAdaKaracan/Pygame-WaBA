import datetime
import pygame
import random
import math
import pickle

# inits
pygame.init()
pygame.font.init()

# Pygame Vars
screen = pygame.display.set_mode((800, 800), vsync=1)
clock = pygame.time.Clock()

# Setups
pygame.display.set_caption("Billy And Willys Adventures")

# Fonts
main_menu_font_70 = pygame.font.Font("fonts/upheavtt.ttf", 70)
early_game_boy_50 = pygame.font.Font("fonts/Early GameBoy.ttf", 40)

# Game Vars
true_scroll = [0, 0]
level_name = "hey"

# Sounds
jump_sound = pygame.mixer.Sound("sounds/jump.wav")
fly_bat_sound = pygame.mixer.Sound("sounds/bat_fly.mp3")
pygame.mixer.music.load("sounds/bg_music.wav")

# Setup Button Images
def setup_buttons():
    global start_button, start_button_highlite, start_button_pressed
    global exit_button, exit_button_pressed, exit_button_highlite
    start_button = pygame.image.load("buttons/start.png").convert_alpha()
    for y in range(start_button.get_height()):
        for x in range(start_button.get_width()):
            pixel = start_button.get_at((x, y))
            if pixel == (0, 0, 0, 255):
                start_button.set_at((x, y), (0, 0, 0, 0))
    start_button_highlite = start_button.copy()
    start_button_pressed = start_button.copy()
    for y in range(start_button.get_height()):
        for x in range(start_button.get_width()):
            pixel = start_button.get_at((x, y))
            if pixel == (255, 255, 255, 255):
                start_button_highlite.set_at((x, y), (179, 182, 186, 255))
    for y in range(start_button.get_height()):
        for x in range(start_button.get_width()):
            pixel = start_button.get_at((x, y))
            if pixel == (255, 255, 255, 255):
                start_button_pressed.set_at((x, y), (105, 107, 110, 255))
    exit_button = pygame.image.load("buttons/exit.png").convert_alpha()
    for y in range(exit_button.get_height()):
        for x in range(exit_button.get_width()):
            pixel = exit_button.get_at((x, y))
            if pixel == (0, 0, 0, 255):
                exit_button.set_at((x, y), (0, 0, 0, 0))
    exit_button_pressed = exit_button.copy()
    exit_button_highlite = exit_button.copy()
    for y in range(exit_button.get_height()):
        for x in range(exit_button.get_width()):
            pixel = exit_button.get_at((x, y))
            if pixel == (255, 255, 255, 255):
                exit_button_highlite.set_at((x, y), (179, 182, 186, 255))
    for y in range(exit_button.get_height()):
        for x in range(exit_button.get_width()):
            pixel = exit_button.get_at((x, y))
            if pixel == (255, 255, 255, 255):
                exit_button_pressed.set_at((x, y), (105, 107, 110, 255))


# Button Class
class Button:
    def __init__(self, x, y, w, h, color, click_color, highlite_color=None, outline_color = None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.click_color = click_color
        if highlite_color is not None:
            self.highlite_color = highlite_color
        else:
            self.highlite_color = None
        if outline_color is not None:
            self.outline_color = outline_color
        else:
            self.outline_color = None
        self.clicked = False
        self.highlited = False
        self.ticks = 50

    def draw(self):
        if self.clicked:
            pygame.draw.rect(screen, self.click_color, self.rect)
        elif self.highlited and self.highlite_color is not None:
            pygame.draw.rect(screen, self.highlite_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        if self.outline_color is not None:
            pygame.draw.rect(screen, self.outline_color, self.rect, 2)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed(3)
        if self.ticks != 0:
            self.ticks -= 1
        else:
            self.clicked = False
        if buttons[0] and self.rect.collidepoint(mouse_pos):
            self.clicked = True
            self.ticks = 50
        elif self.rect.collidepoint(mouse_pos):
            self.highlited = True
        else:
            self.highlited = False
        return self.clicked


class ImageButton:
    def __init__(self, x, y, image, pressed, highlite=None):
        self.image = image.copy()
        self.pressed = pressed.copy()
        if highlite is not None:
            self.highlite = highlite.copy()
        else:
            self.highlite = None
        self.rect = self.image.get_rect(x = x, y = y)
        self.highlited = False
        self.clicked = False
        self.tick = 50

    def draw(self):
        if self.clicked:
            screen.blit(self.pressed, self.rect)
        elif self.highlited:
            screen.blit(self.highlite, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed(3)
        if self.tick != 50:
            self.tick -= 1
        else:
            self.clicked = False
        if self.rect.collidepoint(mouse_pos) and buttons[0]:
            self.clicked = True
            self.tick = 50
        elif self.rect.collidepoint(mouse_pos):
            self.highlited = True
        else:
            self.highlited = False
        return self.clicked

    def resize(self, w, h):
        self.image = pygame.transform.scale(self.image, (w, h))
        self.pressed = pygame.transform.scale(self.pressed, (w, h))
        self.highlite = pygame.transform.scale(self.highlite, (w, h))
        self.rect.w = w
        self.rect.h = h


class MainMenu:
    def __init__(self):
        self.background = pygame.transform.scale(
            pygame.image.load("assets/Background_2.png").convert_alpha(),
            (700, 700)
        )
        self.start_button = ImageButton(270, 250, start_button, start_button_pressed, start_button_highlite)
        self.exit_button = ImageButton(270, 500, exit_button, exit_button_pressed, exit_button_highlite)
        self.start_button.resize(256, 128)
        self.exit_button.resize(256, 128)
        self.particles = [pygame.Rect(0, random.randint(0, 690), 10, 10)]
        self.text = main_menu_font_70.render("Main Menu", False, (255, 255, 255))
        self.visible = True

    def draw(self):
        self.particles.append(pygame.Rect(0, random.randint(0, 790), 10, 10))
        for particle in self.particles:
            pygame.draw.rect(screen, (255, 255, 255), particle)
            particle.x += 5
            if particle.x > 800:
                self.particles.pop(self.particles.index(particle))
        screen.blit(self.text, (screen.get_width() // 2 - self.text.get_width() // 2, 100))
        self.start_button.draw()
        self.exit_button.draw()

    def check_buttons(self):
        first = self.start_button.update()
        second = self.exit_button.update()
        return first, second

    def clear_particles(self):
        self.particles = []


class Player:
    def __init__(self, x_pos, y_pos, type = "willy"):
        self.idle_animation = []
        for i in range(5):
            animation_image = pygame.image.load(f"characters/{type}_idle/{type}_idle{i}.png").convert_alpha()
            for y in range(animation_image.get_height()):
                for x in range(animation_image.get_width()):
                    pixel = animation_image.get_at((x, y))
                    if pixel == (255, 255, 255, 255):
                        animation_image.set_at((x, y), (0, 0, 0, 0))
            self.idle_animation.insert(0, animation_image)
        self.animation_index = 0
        self.velx = 5
        self.vely = 0
        self.air_timer = 0
        self.rect = self.idle_animation[0].get_rect(x=x_pos, y=y_pos)
        self.animation_timer = datetime.datetime.now()
        self.jumped = False
        self.moving = False
        self.angle = 5
        self.visible = True
        self.rotating_negative = False
        self.moving_right = True
        self.move_particles = []

    def draw(self):
        if not self.visible:
            return
        for particle in self.move_particles:
            pygame.draw.circle(screen, (255, 255, 255), particle[0], particle[3])
            particle[0][1] += particle[1][1]
            particle[1][1] += 0.2
            particle[2] -= 0.1
            particle[3] -= 0.1
            if particle[2] <= 0:
                self.move_particles.remove(particle)
        if self.moving and not self.jumped:
            self.animation_index = 0
            rotated = pygame.transform.rotate(self.idle_animation[0].copy(), self.angle)
            self.move_particles.append([[self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h - 5], [0, -2 - random.randint(0, 20) // 10],6, 3])

            screen.blit(rotated, self.rect)
            if self.rotating_negative:
                self.angle += 1
                if self.angle == 5:
                    self.rotating_negative = False
            else:
                self.angle -= 1
                if self.angle == -5:
                    self.rotating_negative = True
            return
        self.rect.x -= int(true_scroll[0])
        screen.blit(self.idle_animation[self.animation_index % 5], self.rect)
        now = datetime.datetime.now()
        if (now - self.animation_timer).total_seconds() > 0.2:
            self.animation_index += 1
            pos_x, pos_y = self.rect.x, self.rect.y
            self.rect = self.idle_animation[self.animation_index % 5].get_rect(x=pos_x, y=pos_y)
            self.animation_timer = now

    def update(self, level):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            _, coll = self.move([self.velx, 0], level)
            self.moving = True
            self.moving_right = True
        elif keys[pygame.K_a]:
            _, coll = self.move([-self.velx, 0], level)
            self.moving = True
            self.moving_right = False
        else:
            _, coll = self.move([0, 0], level)
            self.moving = False
            self.moving_right = False
        move_y = 0
        move_y += self.vely
        _, coll = self.move([0, move_y], level)
        self.vely += 4
        if self.vely > 4:
            self.vely = 4
        if coll["bottom"]:
            self.vely = 0
            self.air_timer = 0
        else:
            self.air_timer += 1
        if self.air_timer < 6 and keys[pygame.K_SPACE]:
            self.vely = -15
            jump_sound.stop()
            jump_sound.play()

    def set_visible(self, value):
        self.visible = value

    def move(self, movement, level):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += movement[0]
        hit_list = self.check_collision(level)
        for tile in hit_list:
            if movement[0] > 0:
                self.rect.right = tile.rect.left
                collision_types['right'] = True
            elif movement[0] < 0:
                self.rect.left = tile.rect.right
                collision_types['left'] = True
        self.rect.y += movement[1]
        hit_list = self.check_collision(level)
        for tile in hit_list:

            if movement[1] > 0:
                self.rect.bottom = tile.rect.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                self.rect.top = tile.rect.bottom
                collision_types['top'] = True
        return self.rect, collision_types

    def check_collision(self, level):
        hit_tiles = []
        for y in range(len(level.tiles)):
            for block in level.tiles[y]:
                if isinstance(block, Block):
                    if self.rect.colliderect(block.rect):
                        hit_tiles.append(block)
        return hit_tiles


class Bat_Enemy:
    def __init__(self, x_pos, y_pos):
        self.animation = []
        for i in range(5):
            img = pygame.image.load(f"characters/bat/bat_fly{i}.png").convert_alpha()
            for y in range(img.get_height()):
                for x in range(img.get_width()):
                    pixel = img.get_at((x, y))
                    if pixel == (255, 255, 255, 255):
                        img.set_at((x, y), (0, 0, 0, 0))
            img = pygame.transform.scale2x(img)
            self.animation.append(img)
        self.animation_index = 0
        self.rect = self.animation[0].get_rect(x=x_pos, y=y_pos)
        self.animation_timer = datetime.datetime.now()
        self.music = False
        self.music_played = datetime.datetime.now() - datetime.timedelta(seconds=12)

    def draw(self, willy):
        self.rect.x -= int(true_scroll[0])
        screen.blit(self.animation[self.animation_index % 5], self.rect)
        now = datetime.datetime.now()
        if (now - self.animation_timer).total_seconds() > 0.14:
            self.animation_index += 1
            x, y = self.rect.x, self.rect.y
            if self.animation_index % 5 == 1:
                self.rect = self.animation[self.animation_index % 5].get_rect(x=x, y=y-10)
            elif self.animation_index % 5 == 4:
                self.rect = self.animation[self.animation_index % 5].get_rect(x=x, y=y+10)
            else:
                self.rect = self.animation[self.animation_index % 5].get_rect(x=x, y=y)
            self.animation_timer = now
        range_to_player = math.sqrt((self.rect.x - willy.rect.x)**2 + (self.rect.y - willy.rect.y)**2)
        if range_to_player < 400:
            fly_bat_sound.set_volume(1)
            if 300 < range_to_player < 400:
                fly_bat_sound.set_volume(0.4)
            if not self.music:
                if self.animation_index % 5 == 4:
                    self.music_played = datetime.datetime.now()
                    self.music = True
                    fly_bat_sound.play()
            elif (datetime.datetime.now() - self.music_played).total_seconds() > 12:
                self.music = False
        else:
            self.music = False
            fly_bat_sound.stop()


class Willy(Player):
    def __init__(self, x, y):
        super().__init__(x, y, "willy")


class Billy(Player):
    def __init__(self, x, y):
        super().__init__(x, y, "billy")


class Block:
    def __init__(self, x, y, type="1_1"):
        self.image = pygame.transform.scale(pygame.image.load(f"assets/{type}.png"), (40, 40))
        self.rect = self.image.get_rect(x=x, y=y)

    def draw(self):
        self.rect.x -= int(true_scroll[0])
        if -self.image.get_width() < self.rect.x < 800:
            screen.blit(self.image, self.rect)

class Level:
    def __init__(self, name, chunk):
        with open(f"levels/{name}.wabs", "rb") as f:
            data = pickle.loads(f.read())
        self.tiles = []
        self.entitys = []
        for y in range(0, chunk*20):
            row = []
            for x in range(0, chunk*20):
                if data[0][y][x][1] is None:
                    row.append(None)
                    continue
                pos = data[0][y][x][0]
                row.append(Block(pos[0]*40, pos[1]*40, data[0][y][x][1]))
            self.tiles.append(row)
        for entity in data[1]:
            pos = entity[0]
            if entity[1] == "bat":
                self.entitys.append(Bat_Enemy(pos[0]+(pos[2]* 800), pos[1]))
        self.bg = pygame.transform.scale(pygame.image.load("assets/Background_2.png"), (800, 800))

    def draw(self, willy):
        screen.blit(self.bg, (0, 0))
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if isinstance(self.tiles[y][x], Block):
                    self.tiles[y][x].draw()
        """for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if isinstance(self.tiles[y][x], Block):
                    self.tiles[y][x].draw()"""
        for entity in self.entitys:
            entity.draw(willy)


def fps_draw():
    fps_surface = early_game_boy_50.render(f"FPS: {int(clock.get_fps())}", False, (255, 255, 255))
    screen.blit(fps_surface, (0, 0))

# Main Loop
def main():
    global level_name
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    setup_buttons()
    main_menu = MainMenu()
    level = Level(level_name, 2)
    willy = Willy(410, 300)
    on_main_menu = True
    running = True
    while running:
        clock.tick()
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
        if on_main_menu:
            main_menu.draw()
            first, second = main_menu.check_buttons()
            if first:
                on_main_menu = False
                main_menu.clear_particles()
            elif second:
                running = False
        if not on_main_menu:
            if willy.rect.x >= 800-willy.rect.w:
                willy.rect.x = 800-willy.rect.w
            if willy.rect.x <= 0:
                willy.rect.x = 0
            true_scroll[0] = (willy.rect.x-true_scroll[0]-400) / 50
            level.draw(willy)
            willy.draw()
            willy.update(level)
        fps_draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
