import pygame
import sys
import random
from pacman import *
import dijkstar
from game import *


class Ghost:
    def __init__(self):
        self.imgweak = pygame.image.load("assets/ghosts/ghost_dead.png")  # Texture fantome vulnérable
        self.colliderbox = self.imgweak.get_rect()  # Boite de collision de la meme taille
        self.eye = pygame.image.load("assets/ghosts/eye_left.png")  # Texture du fantome tué
        self.colliderbox = self.eye.get_rect()

        self.speed = 5  # vitesse
        self.weak = 0  # état de vulnérabilité
        self.is_loaded = 0  # état du chargement sur la map
        self.is_out = 0  # est il sorti de la grotte ?

    def ghost_wrap_around(self):  # Permet aux fantomes d'utiliser les tunnels
        if self.colliderbox.x > 680:
            self.colliderbox.x -= 680
        if self.colliderbox.x < 0:
            self.colliderbox.x += 680

    def random_next_move(self, wall):  # test la validité d'un changement de direction
        self.next_direction = random.randint(1, 4)  # Prends une valeur aléatoire mais demi tours interdits
        if self.next_direction == 1 and self.direction == 2:
            self.next_direction = 2
        if self.next_direction == 2 and self.direction == 1:
            self.next_direction = 1
        if self.next_direction == 3 and self.direction == 4:
            self.next_direction = 4
        if self.next_direction == 4 and self.direction == 3:
            self.next_direction = 3

        if self.next_direction == 1:  # Applique le mouvement pour un test
            self.colliderbox.y -= self.speed
        if self.next_direction == 2:
            self.colliderbox.y += self.speed
        if self.next_direction == 3:
            self.colliderbox.x -= self.speed
        if self.next_direction == 4:
            self.colliderbox.x += self.speed

        for i in range(len(wall)):  # Si collision avec un mur, on invalide le mouvement
            if self.colliderbox.colliderect(wall[i].colliderbox):
                if self.next_direction == 1:
                    self.colliderbox.y += self.speed
                    return 0
                if self.next_direction == 2:
                    self.colliderbox.y -= self.speed
                    return 0
                if self.next_direction == 3:
                    self.colliderbox.x += self.speed
                    return 0
                if self.next_direction == 4:
                    self.colliderbox.x -= self.speed
                    return 0

        if self.next_direction == 1:  # Valide le mouvement (sans l'éxécuter)
            self.colliderbox.y += self.speed
            return 1
        if self.next_direction == 2:
            self.colliderbox.y -= self.speed
            return 1
        if self.next_direction == 3:
            self.colliderbox.x += self.speed
            return 1
        if self.next_direction == 4:
            self.colliderbox.x -= self.speed
            return 1

    def random_move(self, wall, next):  # Applique le mouvement random selon les memes conditions que le fonction du dessus
        if next == 1:
            if self.next_direction == 1:
                self.next_direction = 0  # On clear la prochaine direction
                self.direction = 1
            if self.next_direction == 2:
                self.next_direction = 0
                self.direction = 2
            if self.next_direction == 3:
                self.next_direction = 0
                self.direction = 3
            if self.next_direction == 4:
                self.next_direction = 0
                self.direction = 4

        if self.direction == 1:  # On applique le mouvement dans le direction validée
            self.colliderbox.y -= self.speed
        if self.direction == 2:
            self.colliderbox.y += self.speed
        if self.direction == 3:
            self.colliderbox.x -= self.speed
        if self.direction == 4:
            self.colliderbox.x += self.speed

        for i in range(len(wall)):  # En cas de collision avec un mur on annule le mouvement
            if self.colliderbox.colliderect(wall[i].colliderbox):
                if self.direction == 1:
                    self.colliderbox.y += self.speed
                if self.direction == 2:
                    self.colliderbox.y -= self.speed
                if self.direction == 3:
                    self.colliderbox.x += self.speed
                if self.direction == 4:
                    self.colliderbox.x -= self.speed

    def followpac(self, wall, pacnode, game):  # Suivi de Pac-Man
        if self.current_node[0] == 14 and self.current_node[1] == 27:  # Permet d'emprunter le tunnel
            next = self.random_next_move(wall)
            self.random_move(wall, next);
            return
        if self.current_node[0] == 14 and self.current_node[1] == 0:  # Permet d'emprunter le tunnel
            next = self.random_next_move(wall)
            self.random_move(wall, next);
            return
        next = 0  # validité du prochain mouvement
        p = game.dijkstra(self.current_node, pacnode)  # Renvoie le chemin le plus court du noeud actuel à Pac-Man
        if len(p) == 1:  # Nous sommes déjà sur Pac-Man
            return 1
        if p[0][0] > p[1][0]:  # Déplacement en haut
            self.colliderbox.y -= self.speed
            self.next_direction = 1
        elif p[0][0] < p[1][0]:  # Déplacement en bas
            self.colliderbox.y += self.speed
            self.next_direction = 2
        elif p[0][1] > p[1][1]:  # Déplacement à gauche
            self.colliderbox.x -= self.speed
            self.next_direction = 3
        elif p[0][1] < p[1][1]:  # Déplacement à droite
            self.colliderbox.x += self.speed
            self.next_direction = 4

        for i in range(len(wall)):  # En cas de collision avec un mur, on annule le mouvement
            if self.colliderbox.colliderect(wall[i].colliderbox):
                if self.next_direction == 1:
                    self.colliderbox.y += self.speed
                    next = 1
                if self.next_direction == 2:
                    self.colliderbox.y -= self.speed
                    next = 1
                if self.next_direction == 3:
                    self.colliderbox.x += self.speed
                    next = 1
                if self.next_direction == 4:
                    self.colliderbox.x -= self.speed
                    next = 1
        if next == 0:
            self.direction = self.next_direction  # On valide le prochain mouvement

        if next == 1:  # On continue dans la direction actuelle
            if self.direction == 1:
                self.colliderbox.y -= self.speed
            if self.direction == 2:
                self.colliderbox.y += self.speed
            if self.direction == 3:
                self.colliderbox.x -= self.speed
            if self.direction == 4:
                self.colliderbox.x += self.speed

    def fuite(self, wall, pacman):  # On cherche à s'éloigner de Pac-Man
        while True:
            next = self.random_next_move(wall)
            if self.next_direction == 1 and pacman.direction == 2:
                break
            if self.next_direction == 2 and pacman.direction == 1:
                break
            if self.next_direction == 3 and pacman.direction == 4:
                break
            if self.next_direction == 4 and pacman.direction == 3:
                break
            self.random_move(wall, next)
            return

    def rentrer(self, wall, game):  # Une foi le fantome mort, retour à la grotte avant de réapparaitre
        next = 0
        p = game.dijkstra(self.current_node, self.start_node)  # chemin le plus court vers la grotte
        if len(p) == 1:
            return 1
        if p[0][0] > p[1][0]:
            self.colliderbox.y -= self.speed
            self.next_direction = 1
        elif p[0][0] < p[1][0]:
            self.colliderbox.y += self.speed
            self.next_direction = 2
        elif p[0][1] > p[1][1]:
            self.colliderbox.x -= self.speed
            self.next_direction = 3
        elif p[0][1] < p[1][1]:
            self.colliderbox.x += self.speed
            self.next_direction = 4

        for i in range(len(wall)):
            if self.colliderbox.colliderect(wall[i].colliderbox):
                if wall[i].Owall == 1:
                    if self.next_direction == 1:
                        self.colliderbox.y -= self.speed
                        next = 0
                    if self.next_direction == 2:
                        self.colliderbox.y += self.speed
                        next = 0
                    if self.next_direction == 3:
                        self.colliderbox.x -= self.speed
                        next = 0
                    if self.next_direction == 4:
                        self.colliderbox.x += self.speed
                        next = 0
                else:
                    if self.next_direction == 1:
                        self.colliderbox.y += self.speed
                        next = 1
                    if self.next_direction == 2:
                        self.colliderbox.y -= self.speed
                        next = 1
                    if self.next_direction == 3:
                        self.colliderbox.x += self.speed
                        next = 1
                    if self.next_direction == 4:
                        self.colliderbox.x -= self.speed
                        next = 1

        if next == 0:
            self.direction = self.next_direction
        if next == 1:
            if self.direction == 1:
                self.colliderbox.y -= self.speed
            if self.direction == 2:
                self.colliderbox.y += self.speed
            if self.direction == 3:
                self.colliderbox.x -= self.speed
            if self.direction == 4:
                self.colliderbox.x += self.speed

class red(Ghost):
    def __init__(self):
        super().__init__()  # Permet d'hériter des membres et méthodes de sa classe parent
        self.image = pygame.image.load("assets/ghosts/red_left.png")
        self.colliderbox = self.image.get_rect()
        self.direction = 0
        self.next_direction = 0
        self.start_node = 0
        self.current_node = 0

    def move_red(self, wall, pacman, game):
        if self.weak == 1:
            self.speed = -5  # fait les mouvements dans la direction opposée lorsque vulnérable
            next = self.random_next_move(wall)
            self.random_move(wall, next)
            return
        if self.weak == 0:
            self.speed = 5
        if self.weak == 2:
            self.speed = 5
            self.current_node = (int(self.colliderbox.y / 25), int(self.colliderbox.x / 25))  # On renseigne la position actuelle. Division par 25 car c'est la taille de nos textures
            self.rentrer(wall, game)
            self.is_out = 0
            return
        if self.is_out == 0:  # Sort de la grotte
            if self.colliderbox.x < 335:
                self.colliderbox.x += self.speed
            if self.colliderbox.x > 335:
                self.colliderbox.x -= self.speed
            if self.colliderbox.y < 275:
                self.colliderbox.y += self.speed
            if self.colliderbox.y > 275:
                self.colliderbox.y -= self.speed

            if self.colliderbox.x == 335 and self.colliderbox.y == 275:
                self.is_out = 1
        else:
            if abs(self.colliderbox.x - pacman.colliderbox.x) > 80 and abs(self.colliderbox.y - pacman.colliderbox.y) > 80:  # Si jamais loin du Pac-Man
                next = self.random_next_move(wall)
                self.random_move(wall, next)
            else:  # Si jamais on est près du Pac-Man
                self.current_node = (int(self.colliderbox.y / 25), int(self.colliderbox.x / 25))
                self.followpac(wall, pacman.current_node, game)

        if self.direction == 1:  # textures orientées selon la direction actuelle
            self.image = pygame.image.load("assets/ghosts/red_up.png")
        if self.direction == 2:
            self.image = pygame.image.load("assets/ghosts/red_down.png")
        if self.direction == 3:
            self.image = pygame.image.load("assets/ghosts/red_left.png")
        if self.direction == 4:
            self.image = pygame.image.load("assets/ghosts/red_right.png")


class blue(Ghost):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/ghosts/blue_up.png")
        self.colliderbox = self.image.get_rect()
        self.start_node = 0
        self.current_node = 0
        self.direction = 0
        self.next_direction = 0
        self.change = 0

    def move_blue(self, wall, pacman, game):
        if self.weak == 1:
            self.speed = -5
            next = self.random_next_move(wall)
            self.random_move(wall, next)
            return
        if self.weak == 0:
            self.speed = 5
        if self.weak == 2:
            self.speed = 5
            self.current_node = (int(self.colliderbox.y / 25), int(self.colliderbox.x / 25))
            self.rentrer(wall, game)
            self.is_out = 0
            return
        if self.is_out == 0:
            if self.colliderbox.x < 335:
                self.colliderbox.x += self.speed
            if self.colliderbox.x > 335:
                self.colliderbox.x -= self.speed
            if self.colliderbox.y < 275:
                self.colliderbox.y += self.speed
            if self.colliderbox.y > 275:
                self.colliderbox.y -= self.speed

            if self.colliderbox.x == 335 and self.colliderbox.y == 275:
                self.is_out = 1
        else:
            if abs(self.colliderbox.x - pacman.colliderbox.x) > 110 and abs(
                    self.colliderbox.y - pacman.colliderbox.y) > 110:
                next = self.random_next_move(wall)
                self.random_move(wall, next)
            else:
                self.change = self.change % 15
                go_oposite = random.randint(0, 6)
                if go_oposite == 0 or self.change != 0:
                    self.change += 1
                    self.current_node = (int(self.colliderbox.y / 25), int(self.colliderbox.x / 25))
                    self.fuite(wall, pacman)
                else:
                    self.current_node = (int(self.colliderbox.y / 25), int(self.colliderbox.x / 25))
                    self.followpac(wall, pacman.current_node, game)

            if self.direction == 1:
                self.image = pygame.image.load("assets/ghosts/blue_up.png")
            if self.direction == 2:
                self.image = pygame.image.load("assets/ghosts/blue_down.png")
            if self.direction == 3:
                self.image = pygame.image.load("assets/ghosts/blue_left.png")
            if self.direction == 4:
                self.image = pygame.image.load("assets/ghosts/blue_right.png")


class pink(Ghost):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/ghosts/pink_right.png")
        self.colliderbox = self.image.get_rect()
        self.start_node = 0
        self.current_node = 0
        self.direction = 0

    def move_pink(self, wall, pacman, game):
        if self.weak == 1:
            self.speed = -5
            next = self.random_next_move(wall)
            self.random_move(wall, next)
            return
        if self.weak == 0:
            self.speed = 5
        if self.weak == 2:
            self.speed = 5
            self.current_node = (int(self.colliderbox.y / 25), int(self.colliderbox.x / 25))
            self.rentrer(wall, game)
            self.is_out = 0
            return
        if self.is_out == 0:
            if self.colliderbox.x < 335:
                self.colliderbox.x += self.speed
            if self.colliderbox.x > 335:
                self.colliderbox.x -= self.speed
            if self.colliderbox.y < 275:
                self.colliderbox.y += self.speed
            if self.colliderbox.y > 275:
                self.colliderbox.y -= self.speed

            if self.colliderbox.x == 335 and self.colliderbox.y == 275:
                self.is_out = 1
        else:
            if abs(self.colliderbox.x - pacman.colliderbox.x) > 80 and abs(
                    self.colliderbox.y - pacman.colliderbox.y) > 80:
                next = self.random_next_move(wall)
                self.random_move(wall, next);
            else:
                pacnextposition = (0, 0)
                self.current_node = (int(self.colliderbox.y / 25), int(self.colliderbox.x / 25))
                if (abs(self.current_node[0] - pacman.current_node[0])) + abs((self.current_node[1] - pacman.current_node[1])) <= 4:
                    self.next_direction = self.direction
                    self.next_direction = self.direction
                    self.next_direction = self.direction
                    self.next_direction = self.direction
                    self.random_move(wall, 1)
                else:  # regarde 4 cases plus loin que Pac-Man pour tenter d'anticiper ses mouvements et faire une embuscade
                    if pacman.direction == 1:
                        if pacman.current_node[0] - 4 <= 0:
                            pacnextposition = (pacman.current_node[0], pacman.current_node[1])
                        else:
                            pacnextposition = (pacman.current_node[0] - 4, pacman.current_node[1])

                    if pacman.direction == 2:
                        if pacman.current_node[0] + 4 >= 31:
                            pacnextposition = (pacman.current_node[0], pacman.current_node[1])
                        else:
                            pacnextposition = (pacman.current_node[0] + 4, pacman.current_node[1])

                    if pacman.direction == 3:
                        if pacman.current_node[1] - 4 <= 0:
                            pacnextposition = (pacman.current_node[0], pacman.current_node[1])
                        else:
                            pacnextposition = (pacman.current_node[0], pacman.current_node[1] - 4)

                    if pacman.direction == 4:
                        if pacman.current_node[1] + 4 >= 28:
                            pacnextposition = (pacman.current_node[0], pacman.current_node[1])
                        else:
                            pacnextposition = (pacman.current_node[0], pacman.current_node[1] + 4)

                    self.followpac(wall, pacnextposition, game)

            if self.direction == 1:
                self.image = pygame.image.load("assets/ghosts/pink_up.png")
            if self.direction == 2:
                self.image = pygame.image.load("assets/ghosts/pink_down.png")
            if self.direction == 3:
                self.image = pygame.image.load("assets/ghosts/pink_left.png")
            if self.direction == 4:
                self.image = pygame.image.load("assets/ghosts/pink_right.png")


class yellow(Ghost):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/ghosts/yellow_down.png")
        self.colliderbox = self.image.get_rect()
        self.next_direction = 0
        self.direction = 0
        self.start_node = 0
        self.current_node = 0

    def move_yellow(self, wall, game):
        if self.weak == 1:
            self.speed = -5
            next = self.random_next_move(wall)
            self.random_move(wall, next)
            return
        if self.weak == 0:
            self.speed = 5
        if self.weak == 2:
            self.speed = 5
            self.current_node = (int(self.colliderbox.y / 25), int(self.colliderbox.x / 25))
            self.rentrer(wall, game)
            self.is_out = 0
            return
        if self.is_out == 0:
            if self.colliderbox.x < 335:
                self.colliderbox.x += self.speed
            if self.colliderbox.x > 335:
                self.colliderbox.x -= self.speed
            if self.colliderbox.y < 275:
                self.colliderbox.y += self.speed
            if self.colliderbox.y > 275:
                self.colliderbox.y -= self.speed
            if self.colliderbox.x == 335 and self.colliderbox.y == 275:
                self.is_out = 1
        else:
            next = self.random_next_move(wall)
            self.random_move(wall, next);

        if self.direction == 1:
            self.image = pygame.image.load("assets/ghosts/yellow_up.png")
        if self.direction == 2:
            self.image = pygame.image.load("assets/ghosts/yellow_down.png")
        if self.direction == 3:
            self.image = pygame.image.load("assets/ghosts/yellow_left.png")
        if self.direction == 4:
            self.image = pygame.image.load("assets/ghosts/yellow_right.png")