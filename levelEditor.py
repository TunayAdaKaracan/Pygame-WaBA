import pygame
import datetime
import pickle
import os

pygame.init()
pygame.font.init()

main_font_30 = pygame.font.Font("fonts/Early GameBoy.ttf", 30)

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Level Editor For BaWA")

level = None

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
        self.rect = self.animation[0].get_rect(center=(x_pos, y_pos))
        self.animation_timer = datetime.datetime.now()
        self.type = "bat"

    def draw(self):
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

class Block:
    def __init__(self, x, y, type):
        self.image = pygame.transform.scale(pygame.image.load(f"assets/{type}.png"), (40, 40))
        self.rect = self.image.get_rect(x=x, y=y)
        self.type = type

    def draw(self):
        screen.blit(self.image, self.rect)

class Level:
    def __init__(self, name, w, h):
        self.level_name = name
        self.tiles = []
        for y in range(h):
            row = []
            for x in range(w):
                row.append(None)
            self.tiles.append(row)
        self.bg = pygame.transform.scale(pygame.image.load("assets/Background_2.png"), (800, 800))
        self.chunk = 0
        self.entitys = []

    def draw(self):
        screen.blit(self.bg, (0, 0))
        for y in range(len(self.tiles)):
            for x in range(self.chunk * 20, (self.chunk+1) * 20):
                if isinstance(self.tiles[y][x], Block):
                    self.tiles[y][x].draw()
        """for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if isinstance(self.tiles[y][x], Block):
                    self.tiles[y][x].draw()"""
        for entity in self.entitys:
            if entity[1] == self.chunk:
                entity[0].draw()

    def set_block(self, x, y, type):
        self.tiles[y][x+(self.chunk * 20)] = Block(x*40, y*40, type)

    def erase_block(self, x, y):
        self.tiles[y][x+(self.chunk * 20)] = None

    def add_enemy(self, x, y, type):
        if type == "bat":
            self.entitys.append((Bat_Enemy(x, y), self.chunk))

    def remove_enemy(self, x, y):
        for entity in self.entitys:
            if entity[0].rect.collidepoint((x, y)):
                self.entitys.remove(entity)

    def save(self):
        saving = []
        for y in range(len(self.tiles)):
            row = []
            for x in range(len(self.tiles[y])):
                row.append(((x, y), None if self.tiles[y][x] is None else self.tiles[y][x].type))
            saving.append(row)
        saving_entitys = []
        for entity in self.entitys:
            print(entity[0].rect.x, entity[0].rect.y)
            saving_entitys.append(((entity[0].rect.x, entity[0].rect.y, entity[1]), entity[0].type))
        with open(f"levels/{self.level_name}.wabs", "wb") as f:
            f.write(pickle.dumps([saving, saving_entitys]))

    def load(self):
        with open(f"levels/{self.level_name}.wabs", "rb") as f:
            data = pickle.loads(f.read())
        world = []
        entitys = []
        for y in range(len(data[0])):
            row = []
            for x in range(len(data[0][y])):
                if data[0][y][x][1] is None:
                    row.append(None)
                    continue
                pos = data[0][y][x][0]
                row.append(Block((pos[0]*40) % 800, pos[1]*40 % 800, data[0][y][x][1]))
            world.append(row)
        for entity in data[1]:
            print(entity)
            pos = entity[0]
            if entity[1] == "bat":
                entitys.append((Bat_Enemy(pos[0] + 48, pos[1] + 48), pos[2]))
        self.entitys = entitys
        self.tiles = world




class MainMenu:
    def __init__(self):
        self.back = pygame.Rect(0, 0, 800, 800)
        self.BACK_COLOR = (30, 30, 30)
        self.menu_bar = pygame.Rect(50, 100, 350, 600)
        self.MENU_BAR_COLOR = (32,28,28)
        self.items = []
        self.create = pygame.Rect(50, 10, 350, 80)
        self.CREATE_COLOR = (10, 10, 10)
        self.selected = None
        self.pressed = False
        self.typing_bar_visible = False
        self.typing = False
        self.typed = ""
        self.typing_bar = pygame.Rect(420, 10, 350, 80)
        self.key_pressed = False
        self.join_bar = pygame.Rect(420, 620, 350, 80)
        self.plus_1 = pygame.Rect(220, 25, 5, 45)
        self.plus_2 = pygame.Rect(200, 45, 45, 5)

    def draw(self):
        pygame.draw.rect(screen, self.BACK_COLOR, self.back)
        pygame.draw.rect(screen, self.MENU_BAR_COLOR, self.menu_bar)
        pygame.draw.rect(screen, self.CREATE_COLOR, self.create)
        pygame.draw.rect(screen, (255 ,255 ,255), self.plus_1)
        pygame.draw.rect(screen, (255, 255, 255), self.plus_2)
        index = 1
        for world in self.items:
            color = (255, 255, 255)
            if self.selected == world:
                color = (220, 220, 220)
            pygame.draw.rect(screen, color, world[1])
            world_name_surface = main_font_30.render(world[0], False, (0, 0, 0)).convert_alpha()
            screen.blit(world_name_surface, (70, index * 200 - 90 * index))
            index += 1
        if self.typing_bar_visible:
            pygame.draw.rect(screen, (255, 255, 255), self.typing_bar)
            text_surface = main_font_30.render(self.typed, False, (0, 0, 0)).convert_alpha()
            screen.blit(text_surface, (430, 20))
        pygame.draw.rect(screen, (0, 255, 0), self.join_bar)
        pygame.draw.line(screen, (255, 255, 255), (580, 630), (600, 660), 4)
        pygame.draw.line(screen, (255, 255, 255), (600, 660), (580, 690), 4)

    def update(self):
        global level, on_menu
        self.refresh_items()
        mouse_pos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        if not buttons[0]:
            self.pressed = False
        if self.create.collidepoint(mouse_pos) and buttons[0] and not self.pressed:
            self.pressed = True
            if self.typing:
                self.typing = False
                self.typing_bar_visible = False
            else:
                self.typing = True
                self.typing_bar_visible = True
        for world in self.items:
            if world[1].collidepoint(mouse_pos) and buttons[0] and not self.pressed:
                self.selected = world
                self.pressed = True
        if self.join_bar.collidepoint(mouse_pos) and buttons[0] and not self.pressed and not self.selected is None:
            self.pressed = False
            on_menu = False
            level = Level(self.selected[0], 0, 0)
            level.load()
        if self.typing:
            keys = pygame.key.get_pressed()
            if not self.key_pressed:
                if keys[pygame.K_q]: self.typed += "q"
                if keys[pygame.K_w]: self.typed += "w"
                if keys[pygame.K_e]: self.typed += "e"
                if keys[pygame.K_r]: self.typed += "r"
                if keys[pygame.K_t]: self.typed += "t"
                if keys[pygame.K_y]: self.typed += "y"
                if keys[pygame.K_u]: self.typed += "u"
                if keys[pygame.K_o]: self.typed += "o"
                if keys[pygame.K_p]: self.typed += "p"
                if keys[pygame.K_a]: self.typed += "a"
                if keys[pygame.K_s]: self.typed += "s"
                if keys[pygame.K_d]: self.typed += "d"
                if keys[pygame.K_f]: self.typed += "f"
                if keys[pygame.K_g]: self.typed += "g"
                if keys[pygame.K_h]: self.typed += "h"
                if keys[pygame.K_j]: self.typed += "j"
                if keys[pygame.K_k]: self.typed += "k"
                if keys[pygame.K_l]: self.typed += "l"
                if keys[pygame.K_i]: self.typed += "i"
                if keys[pygame.K_z]: self.typed += "z"
                if keys[pygame.K_x]: self.typed += "x"
                if keys[pygame.K_c]: self.typed += "c"
                if keys[pygame.K_v]: self.typed += "v"
                if keys[pygame.K_b]: self.typed += "b"
                if keys[pygame.K_n]: self.typed += "n"
                if keys[pygame.K_m]: self.typed += "m"
                if keys[pygame.K_RETURN]:
                    self.typing = False
                    level = Level(self.typed, 500, 100)
                    level.save()
                    self.typing_bar_visible = False
                    self.key_pressed = False
                    return
                if keys[pygame.K_BACKSPACE]:
                    self.typed = self.typed[:-1]
                self.key_pressed = True
            if not any(keys):
                self.key_pressed = False

    def refresh_items(self):
        self.items = []
        files = list(filter(lambda f: f[-5:] == ".wabs", os.listdir("./levels/")))
        index = 1
        for file in files:
            self.items.append([f"{file[:-5]}", pygame.Rect(60, index * 200 - 90 * index, 330, 100)])
            index += 1



def main():
    global on_menu
    running = True
    on_menu = True
    selected = "dirt"
    entity_placement = False
    menu = MainMenu()
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            if event.type == pygame.MOUSEMOTION and not on_menu:
                buttons = event.buttons
                pos = event.pos
                if buttons[0] and not entity_placement:
                    level.set_block(pos[0] // 40, pos[1] // 40, selected)
                elif buttons[2] and not entity_placement:
                    level.erase_block(pos[0]//40, pos[1] // 40)
            if event.type == pygame.MOUSEBUTTONDOWN and not on_menu and entity_placement:
                button = event.button
                pos = event.pos
                if button == 1:
                    level.add_enemy(pos[0], pos[1], selected)
                elif button == 3:
                    level.remove_enemy(pos[0], pos[1])
            if event.type == pygame.MOUSEBUTTONDOWN and not on_menu and not entity_placement:
                button = event.button
                pos = event.pos
                if button == 1:
                    level.set_block(pos[0] // 40, pos[1] // 40, selected)
                elif button == 3:
                    level.erase_block(pos[0] // 40, pos[1] // 40)
            if event.type == pygame.KEYDOWN and not on_menu:
                if event.key == pygame.K_1:
                    if not entity_placement:
                        selected = "dirt"
                    else:
                        selected = "bat"
                if event.key == pygame.K_2:
                    if not entity_placement:
                       selected = "grass"
                if event.key == pygame.K_KP0:
                    entity_placement = not entity_placement
                    if entity_placement:
                        selected = "bat"
                    else:
                        selected = "dirt"
                if event.key == pygame.K_ESCAPE:
                    level.save()
                    on_menu = True
                if event.key == pygame.K_RIGHT:
                    level.chunk += 1
                if event.key == pygame.K_LEFT:
                    if not level.chunk == 0:
                        level.chunk -= 1
        if on_menu:
            menu.update()
            menu.draw()
        else:
            level.draw()
        pygame.display.update()

if __name__ == "__main__":
    main()