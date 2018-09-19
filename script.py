#!/usr/bin/env python
import os
import random
import pygame
pygame.init()

# SETTINGS
# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
MAROON = (128,  0,   0)

# Screen
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 600

BACKGROUDS = {
    "menu": BLACK,
    "game": BLACK,
    "pause": None
}

FPS = 60

# Text
TEXT_COLOR = WHITE
TEXT_FONT = "freesansbold.ttf"
TEXT_SIZE = 80

# music:
MUSIC_ON = False
MUSIC_GAME = "Rize_Up.mp3"
CRASH_SOUND = "car_door.wav"

# Buttons:
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50

# Dino
DINO_IMG_NAME = "t-rex3.png"
# DINO_IMG_NAME = "bad.png"
DINO_WIDTH = 180
DINO_HEIGHT = 120
DINO_MARGIN = 0
DINO_INIT_POSX = 100
DINO_INIT_POSY = None
DINO_INIT_SPEED = 300
DINO_JUMP = 80
DINO_WEIGHT = 15


class Button(object):
    def __init__(self, game, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        mouse_is_pressed = pygame.mouse.get_pressed()[0]

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(game.display, ac, (x, y, w, h))
            if mouse_is_pressed:
                action()
        else:
            pygame.draw.rect(game.display, ic, (x, y, w, h))

        smallText = pygame.font.Font(TEXT_FONT, 20)
        textSurf, textRect = game.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2.)), (y + (h / 2.)))
        game.display.blit(textSurf, textRect)


class Menu(object):
    def __init__(self, game, text):
        self.background = None
        self.text = None

    def print_background(self, game):
        game.display.fill(self.background)

    def print_text(self, game):
        largeText = pygame.font.Font(TEXT_FONT, TEXT_SIZE)
        TextSurf, TextRect = game.text_objects(self.text, largeText)
        TextRect.center = ((DISPLAY_WIDTH / 2.), (DISPLAY_HEIGHT / 2.))
        game.display.blit(TextSurf, TextRect)

    def handle_common_events(self, game, event):
        game.handle_common_keys(event)


class MainMenu(Menu):
    def __init__(self, game, text):
        super(MainMenu, self).__init__(game, text)
        self.background = BACKGROUDS["menu"]
        self.text = text

        while True:
            for event in pygame.event.get():
                self.handle_common_events(game, event)
                self.handle_events(game, event)
            self.print_background(game)
            self.print_text(game)
            self.create_buttons(game)

            pygame.display.update()
            game.clock.tick(10)

    def handle_events(self, game, event):
        print "handle_events", event
        if event.type == pygame.KEYDOWN:
            print event.type
            if event.key == pygame.K_RETURN:
                game.loop()

    def create_buttons(self, game):
        Button(game, "PLAY", DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT *
               0.8, BUTTON_WIDTH, BUTTON_HEIGHT, GREEN, BRIGHT_GREEN,
               game.loop)
        Button(game, "QUIT", DISPLAY_WIDTH * 0.7, DISPLAY_HEIGHT *
               0.8, BUTTON_WIDTH, BUTTON_HEIGHT, RED, BRIGHT_RED,
               game.quit)


class PauseMenu(Menu):
    def __init__(self, game, text):
        super(PauseMenu, self).__init__(game, text)
        pygame.mixer.music.pause()
        game.is_paused = True

        self.text = text

        while game.is_paused:
            # print "is_paused", game.is_paused
            for event in pygame.event.get():
                print 11, event
                self.handle_common_events(game, event)
                self.handle_events(game, event)
            self.print_text(game)
            self.create_buttons(game)

            pygame.display.update()
            game.clock.tick(15)

    def handle_events(self, game, event):
        # print "handle_events", event
        if event.type == pygame.KEYDOWN:
            # print event.key, [pygame.K_p, pygame.K_ESCAPE]
            if event.key in [pygame.K_p, pygame.K_ESCAPE]:
                game.to_unpause()

    def create_buttons(self, game):
        Button(game, "Continue", DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.8,
               BUTTON_WIDTH, BUTTON_HEIGHT, GREEN, BRIGHT_GREEN,
               game.to_unpause)
        Button(game, "QUIT", DISPLAY_WIDTH * 0.7, DISPLAY_HEIGHT * 0.8,
               BUTTON_WIDTH, BUTTON_HEIGHT, RED, BRIGHT_RED,
               game.quit)


class GameOverMenu(Menu):
    def __init__(self, game, text):
        super(GameOverMenu, self).__init__(game, text)
        pygame.mixer.music.pause()
        game.is_paused = True

        self.text = text

        while game.is_paused:
            # print "is_paused", game.is_paused
            for event in pygame.event.get():
                print 11, event
                self.handle_common_events(game, event)
                self.handle_events(game, event)
            self.print_text(game)
            self.create_buttons(game)

            pygame.display.update()
            game.clock.tick(15)

    def handle_events(self, game, event):
        # print "handle_events", event
        if event.type == pygame.KEYDOWN:
            # print event.key, [pygame.K_p, pygame.K_ESCAPE]
            if event.key in [pygame.K_RETURN]:
                game.loop()

    def create_buttons(self, game):
        Button(game, "Play Again", DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.8,
               BUTTON_WIDTH, BUTTON_HEIGHT, GREEN, BRIGHT_GREEN,
               game.loop)
        Button(game, "QUIT", DISPLAY_WIDTH * 0.7, DISPLAY_HEIGHT * 0.8,
               BUTTON_WIDTH, BUTTON_HEIGHT, RED, BRIGHT_RED,
               game.quit)


class Dino(object):
    def __init__(self, game):
        print "create Dino"
        self.width = DINO_WIDTH
        self.height = DINO_HEIGHT

        self.x = DINO_INIT_POSX
        if DINO_INIT_POSY:
            self.y = DINO_INIT_POSY
        else:
            self.y = DISPLAY_HEIGHT * 0.5
        # self.speed = float(DINO_INIT_SPEED) / FPS
        self.jump = float(DINO_JUMP) / FPS ** 0.5
        self.weight = float(DINO_WEIGHT) / FPS

        self.dx = 0
        self.dy = self.weight

        self.jump_active = False

        self.try_load_dino_image(DINO_IMG_NAME)
        self.update(game)

    def try_load_dino_image(self, dino_image_name):
        try:
            path_and_file = os.path.join("images", dino_image_name)
            self.img = pygame.image.load(path_and_file)
            print 5, self.img
            pygame.display.set_icon(self.img)
        except pygame.error:
            import traceback
            print(traceback.format_exc())
            self.img = None

    def update(self, game):

        if self.y + (self.height - DINO_MARGIN) > game.ground.y - 20:
            self.dy = 0
        self.x += self.dx
        self.y += self.dy
        self.dy += self.weight
        self.y = min(self.y, game.ground.y - (self.height - DINO_MARGIN))

        if self.img is None:
            self.obj = pygame.draw.rect(game.display, RED,
                                        (self.x + DINO_MARGIN,
                                         self.y,
                                         self.width - 2 * DINO_MARGIN,
                                         self.height-30))
        else:

            self.obj = game.display.blit(self.img, (self.x, self.y))

        for objtree in game.ground.effects.tree.objs:
            if self.obj.colliderect(objtree):
                print "colisao"
                game.over()

    def handle_events(self, game, event):

        if event.type == pygame.KEYDOWN:
            print self.y, game.ground.y
            if event.key in [pygame.K_UP, pygame.K_SPACE] and\
                    self.y + (self.height - DINO_MARGIN) > game.ground.y - 20:
                self.jump_active = True
                self.dy -= self.jump
                self.y -= 50

        # control the jump
        if event.type == pygame.KEYUP:
            if self.jump_active and event.key in [pygame.K_UP, pygame.K_SPACE]:
                self.dy = max(self.dy, 0)
                self.jump_active = False


class GroundOrnaments(object):
    def __init__(self, ground):
        self.n_of_lines = 20
        self.margin = 30
        self.degree = 3
        self.speed = ground.speed
        self.lines = []
        for i in range(self.n_of_lines):
            self.lines.append([])
            self.lines[i].append(random.randrange(DISPLAY_WIDTH))
            self.lines[i].append(ground.y + self.margin *
                                 random.triangular(0, 1, 0.5)**self.degree)

    def update(self, game, ground):
        for line in self.lines:
            line[0] -= self.speed
            if line[0] < 0:
                line[0] = DISPLAY_WIDTH
                line[1] = ground.y + self.margin *\
                    random.triangular(0, 1, 0.5)**self.degree
            pygame.draw.rect(game.display, ground.color,
                             (line[0], line[1], 10, 2))


class Tree(object):
    def __init__(self, game, ground):
        self.x = DISPLAY_WIDTH
        self.y = ground.y
        self.width = 10
        self.height = 80
        self.speed = ground.speed
        self.objs = []
        # # self.img = pygame.draw.rect(game.display, MAROON,
        # #                             (self.x, self.y - self.height,
        # #                              self.width, self.height))
        # self.objs.append(pygame.draw.rect(game.display, MAROON,
        #                                   (self.x, self.y - self.height,
        #                                    self.width, self.height)))

    def update(self, game):
        self.x -= self.speed
        if self.x < 0:
            self.x = DISPLAY_WIDTH
        self.objs = []
        self.objs.append(pygame.draw.rect(game.display, MAROON,
                                          (self.x, self.y - self.height,
                                           self.width, self.height)))
        self.objs.append(pygame.draw.ellipse(game.display, GREEN,
                                             (self.x - self.height / 2.,
                                              self.y - self.height,
                                              self.height, self.width * 3)))


class GroundEffects(object):
    def __init__(self, game, ground):
        self.speed = ground.speed
        self.tree = Tree(game, ground)

    def update(self, game):
        self.tree.update(game)


class Ground(object):
    def __init__(self, game):
        self.y = DISPLAY_HEIGHT * 0.85
        self.speed = float(DINO_INIT_SPEED) / FPS
        self.color = WHITE
        self.ornaments = GroundOrnaments(self)
        self.effects = GroundEffects(game, self)

    def draw(self, game):
        pygame.draw.line(game.display, self.color,
                         (0, self.y), (DISPLAY_WIDTH, self.y), 3)
        self.draw_ornaments(game)
        self.effects.update(game)

    def draw_ornaments(self, game):
        self.ornaments.update(game, self)


class Game(object):
    def __init__(self):

        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("A Dino Game")
        self.clock = pygame.time.Clock()

        self.is_paused = False
        self.cmd_key_down = False

        MainMenu(self, "Dino Game")
        self.loop()
        self.quit()

    def quit(self):
        pygame.quit()
        quit()

    def to_pause(self):
        PauseMenu(self, "PAUSED")

    def to_unpause(self):
        print "to_unpause"
        if MUSIC_ON:
            pygame.mixer.music.unpause()
        self.is_paused = False

    def over(self):
        print "game over"
        if MUSIC_ON:
            pygame.mixer.music.stop()
            crash_sound = pygame.mixer.Sound(os.path.join("musics", CRASH_SOUND))
            pygame.mixer.Sound.play(crash_sound)
        GameOverMenu(self, "Game Over")

    def text_objects(self, text, font):
        textSurface = font.render(text, True, TEXT_COLOR)
        return textSurface, textSurface.get_rect()

    def loop(self):
        if MUSIC_ON:
            pygame.mixer.music.load(os.path.join("musics", MUSIC_GAME))
            pygame.mixer.music.play(-1)

        self.ground = Ground(self)

        self.display.fill(BACKGROUDS["game"])
        self.dino = Dino(self)

        while True:
            for event in pygame.event.get():
                print event
                self.handle_common_keys(event)

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_p, pygame.K_ESCAPE]:
                        PauseMenu(self, "PAUSED")

                self.dino.handle_events(self, event)

            self.display.fill(BACKGROUDS["game"])

            self.dino.update(self)
            self.ground.draw(self)

            pygame.display.update()
            self.clock.tick(FPS)

    def handle_common_keys(self, event):
        if event.type == pygame.QUIT:
            self.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == 310:
                self.cmd_key_down = True
            if self.cmd_key_down and event.key == pygame.K_q:
                self.quit()

        if event.type == pygame.KEYUP:
            if event.key == 310:
                self.cmd_key_down = False


Game()
