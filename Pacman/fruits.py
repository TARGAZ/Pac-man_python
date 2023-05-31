import pygame


class Fruit:  # Classe parent pour tous les objets (appellés fruits par la communauté Pac-Man même si certains n'en sont pas)
    def __init__(self):
        self.value = 0  # Valeur du fruit (pour le bonus de score)
        self.position = (14, 17)  # Position du spawn de fruit


class Cherry(Fruit):
    def __init__(self):
        super().__init__()
        self.value = 100
        self.image = pygame.image.load("assets/fruits/cherry.png")
        self.colliderbox = self.image.get_rect()


class Strawberry(Fruit):
    def __init__(self):
        super().__init__()
        self.value = 300
        self.image = pygame.image.load("assets/fruits/strawberry.png")
        self.colliderbox = self.image.get_rect()


class Orange(Fruit):
    def __init__(self):
        super().__init__()
        self.value = 500
        self.image = pygame.image.load("assets/fruits/yellow.png")
        self.colliderbox = self.image.get_rect()


class Apple(Fruit):
    def __init__(self):
        super().__init__()
        self.value = 700
        self.image = pygame.image.load("assets/fruits/apple.png")
        self.colliderbox = self.image.get_rect()


class Melon(Fruit):
    def __init__(self):
        super().__init__()
        self.value = 1000
        self.image = pygame.image.load("assets/fruits/melon.png")
        self.colliderbox = self.image.get_rect()


class Galaxian(Fruit):
    def __init__(self):
        super().__init__()
        self.value = 2000
        self.image = pygame.image.load("assets/fruits/galaxian.png")
        self.colliderbox = self.image.get_rect()


class Bell(Fruit):
    def __init__(self):
        super().__init__()
        self.value = 3000
        self.image = pygame.image.load("assets/fruits/bell.png")
        self.colliderbox = self.image.get_rect()


class Key(Fruit):
    def __init__(self):
        super().__init__()
        self.value = 5000
        self.image = pygame.image.load("assets/fruits/key.png")
        self.colliderbox = self.image.get_rect()
