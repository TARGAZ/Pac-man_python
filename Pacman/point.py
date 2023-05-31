import pygame


class Point:
    def __init__(self):
        self.image = pygame.image.load("assets/gommes/point.png")
        self.colliderbox = self.image.get_rect()


class BigPoint:
    def __init__(self):
        self.image = pygame.image.load("assets/gommes/bigpoint.png")
        self.colliderbox = self.image.get_rect()


def powerOn(red, blue, pink, yellow, pacman):  # Rend vulnérable les fantomes
    red.weak = 1
    blue.weak = 1
    pink.weak = 1
    yellow.weak = 1


def powerOff(red, blue, pink, yellow, pacman):  # Rend invulnérable les fantomes
    red.weak = 0
    blue.weak = 0
    pink.weak = 0
    yellow.weak = 0
