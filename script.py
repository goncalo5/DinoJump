#!/usr/bin/env python
import random
import pygame
import os
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
MUSIC_GAME = "Rize_Up.mp3"
CRASH_SOUND = "car_door.wav"

# Buttons:
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50

# Dino
DINO_IMG_NAME = "t-rex.png"
DINO_WIDTH = 100
DINO_HEIGHT = 100
DINO_INIT_POSX = 0
DINO_INIT_POSY = None
DINO_INIT_SPEED = 10


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
        textRect.center = ((x+(w/2)), (y+(h/2)))
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
        TextRect.center = ((DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/2))
        game.display.blit(TextSurf, TextRect)

    def handle_common_events(self, game):
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                game.quit_the_game()


class MainMenu(Menu):
    def __init__(self, game, text):
        super(MainMenu, self).__init__(game, text)
        self.background = BACKGROUDS["menu"]
        self.text = text

        while True:
            self.handle_common_events(game)
            self.handle_events(game)
            self.print_background(game)
            self.print_text(game)
            self.create_buttons(game)

            pygame.display.update()
            game.clock.tick(15)

    def handle_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game.game_loop()

    def create_buttons(self, game):
        Button(game, "PLAY", DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT *
               0.8, BUTTON_WIDTH, BUTTON_HEIGHT, GREEN, BRIGHT_GREEN,
               game.game_loop)
        Button(game, "QUIT", DISPLAY_WIDTH * 0.7, DISPLAY_HEIGHT *
               0.8, BUTTON_WIDTH, BUTTON_HEIGHT, RED, BRIGHT_RED,
               game.quit_the_game)


class PauseMenu(Menu):
    def __init__(self, game, text):
        super(PauseMenu, self).__init__(game, text)
        pygame.mixer.music.pause()
        game.is_paused = True

        self.text = text

        while game.is_paused:
            self.handle_common_events(game)
            self.handle_events(game)
            self.print_text(game)
            self.create_buttons(game)

            pygame.display.update()
            game.clock.tick(15)

    def handle_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game.unpause()

    def create_buttons(self, game):
        Button(game, "Continue", DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.8,
               BUTTON_WIDTH, BUTTON_HEIGHT, GREEN, BRIGHT_GREEN,
               game.unpause_the_game)
        Button(game, "QUIT", DISPLAY_WIDTH * 0.7, DISPLAY_HEIGHT * 0.8,
               BUTTON_WIDTH, BUTTON_HEIGHT, RED, BRIGHT_RED,
               game.quit_the_game)


class Game(object):
    def __init__(self):

        self.display = \
            pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("A Dino Game")
        self.clock = pygame.time.Clock()

        self.is_paused = False

        MainMenu(self, "Dino Game")
        self.game_loop()
        self.quit_the_game()

    def quit_the_game(self):
        pygame.quit()
        quit()

    def unpause_the_game(self):
        print "unpause_the_game"
        pygame.mixer.music.unpause()
        self.is_paused = False

    def text_objects(self, text, font):
        textSurface = font.render(text, True, TEXT_COLOR)
        return textSurface, textSurface.get_rect()

    def game_loop(self):
        # pygame.mixer.music.load(MUSIC_GAME)
        # pygame.mixer.music.play(-1)

        self.display.fill(BACKGROUDS["game"])
        self.dino = Dino(self)

        x_change = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_the_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = - self.dino.speed
                    elif event.key == pygame.K_RIGHT:
                        x_change = self.dino.speed
                    elif event.key in [pygame.K_p, pygame.K_ESCAPE]:
                        PauseMenu(self, "PAUSED")

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and x_change < 0:
                        x_change = 0
                    if event.key == pygame.K_RIGHT and x_change > 0:
                        x_change = 0

            self.dino.x += x_change

            pygame.display.update()
            self.clock.tick(FPS)


class Dino(object):
    def __init__(self, game):
        self.w = DINO_WIDTH
        self.h = DINO_HEIGHT

        self.x = DINO_INIT_POSX
        if DINO_INIT_POSY:
            self.y = DINO_INIT_POSY
        else:
            self.y = DISPLAY_HEIGHT * 0.7
        self.speed = DINO_INIT_SPEED / FPS

        self.try_load_dino_image(DINO_IMG_NAME)
        self.draw_dino(game)

    def try_load_dino_image(self, dino_image_name):
        try:
            path_and_file = os.path.join("images", dino_image_name)
            self.img = pygame.image.load(path_and_file)
            pygame.display.set_icon(self.img)
        except pygame.error:
            import traceback
            print(traceback.format_exc())
            self.img = None

    def draw_dino(self, game):
        if self.img is None:
            pygame.draw.rect(game.display, RED, (self.x, self.y,
                                                 self.w, self.h))
        else:
            game.display.blit(self.img, (self.x, self.y))


Game()
