import pygame


class Wall:
    def __init__(self):
        self.image = pygame.image.load("assets/wall/transparent_wall.png")
        self.colliderbox = self.image.get_rect()
        self.Owall = 0  # Variable pour que les fantomes puissent passer par le trait rose
