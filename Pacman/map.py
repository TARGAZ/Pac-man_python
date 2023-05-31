import pygame


class Map:
    def __init__(self):
        self.colliderbox = pygame.Rect(0, 0, 800, 800)
        self.ascii_maze = [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "X............XX............X",
            "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
            "XoXXXX.XXXXX.XX.XXXXX.XXXXoX",
            "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
            "X..........................X",
            "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
            "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
            "X......XX....XX....XX......X",
            "XXXXXX.XXXXX.XX.XXXXX.XXXXXX",
            "XXXXXX.XXXXX.XX.XXXXX.XXXXXX",
            "XXXXXX.XX          XX.XXXXXX",
            "XXXXXX.XX XXXOOXXX XX.XXXXXX",
            "XXXXXX.XX X      X XX.XXXXXX",
            "      .   X G  G X   .      ",
            "XXXXXX.XX XG    GX XX.XXXXXX",
            "XXXXXX.XX XXXXXXXX XX.XXXXXX",
            "XXXXXX.XX          XX.XXXXXX",
            "XXXXXX.XX XXXXXXXX XX.XXXXXX",
            "XXXXXX.XX XXXXXXXX XX.XXXXXX",
            "X............XX............X",
            "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
            "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
            "Xo..XX........P.......XX..oX",
            "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
            "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
            "X......XX....XX....XX......X",
            "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
            "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
            "X..........................X",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        ]

class Map_texture:
    def __init__(self):
        self.texture = pygame.image.load("assets/map/map.png")
        self.collidebox = self.texture.get_rect()
