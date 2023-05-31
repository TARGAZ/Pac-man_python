import pygame
import sys

from map import Map
from game import *
from wall import *


class Pacman:
    def __init__(self):
        self.image = pygame.image.load("assets/pacman/pacman0.png")  # On charge l'image de Pac-Man
        self.colliderbox = self.image.get_rect()  # On fait une boite de collision de la taille de la texture
        self.speed = 5  # Vitesse de Pac-Man
        self.life = 2  # Nombre de vies restantes
        self.bonus_lives_given = 0  # Nombre de vis bonus accordées par les palliers de 10000 sur le score
        self.direction = 0
        self.next_direction = 0
        self.current_node = 0  # Noeud actuel du Pac-Man sur la map

    def bonus_life_from_score(self, score):  # attribution d'une vie bonus à chaque pallier de 10000 sur le score
        score -= self.bonus_lives_given * 10000
        if score > 9999:
            self.life += 1
            self.bonus_lives_given += 1

    def display_remaining_lives(self, screen):  # Affichage des vies restantes sur le bord de l'écran
        not_displayed_yet = self.life
        life_texture = pygame.image.load("assets/pacman/pacman1.png")
        life_texture_collider = life_texture.get_rect()
        while not_displayed_yet > 0:
            life_texture_collider.x = 710
            life_texture_collider.y = 750 - not_displayed_yet * 30
            screen.blit(life_texture, life_texture_collider)
            not_displayed_yet -= 1



    def pacman_wrap_around(self):  # Permet à Pac-Man d'emprunter le tunnel
        if self.colliderbox.x > 60:
            self.colliderbox.x -= 680
        if self.colliderbox.x < 0:
            self.colliderbox.x += 680

    def death_animation(self, death_animation_counter):  # Charge la bonne image pour l'animation de la mort de Pac-Man
        pacman_death_animation = ["assets/pacman/pacman0.png",
                                  "assets/pacman/pacman_dead0.png",
                                  "assets/pacman/pacman_dead1.png",
                                  "assets/pacman/pacman_dead2.png",
                                  "assets/pacman/pacman_dead3.png",
                                  "assets/pacman/pacman_dead4.png",
                                  "assets/pacman/pacman_dead5.png",
                                  "assets/pacman/pacman_dead6.png",
                                  "assets/pacman/pacman_dead7.png",
                                  "assets/pacman/pacman_dead8.png",
                                  "assets/pacman/pacman_dead9.png",
                                  "assets/pacman/pacman_dead10.png"]

        self.image = pygame.image.load((pacman_death_animation[death_animation_counter]))

    def moving_animation(self, animation_counter):  # Animation du mouvement (mouvement bouche + orientation)
        pacman_animations = ["assets/pacman/pacman1.png",
                             "assets/pacman/pacman2.png",
                             "assets/pacman/pacman1.png",
                             "assets/pacman/pacman0.png"]
        if self.direction == 1:  # up
            temp = pygame.image.load(pacman_animations[animation_counter])
            self.image = pygame.transform.rotate(temp, 270)

        if self.direction == 2:  # down
            temp = pygame.image.load(pacman_animations[animation_counter])
            self.image = pygame.transform.rotate(temp, 90)

        if self.direction == 3:  # left
            self.image = pygame.image.load(pacman_animations[animation_counter])

        if self.direction == 4:  # right
            temp = pygame.image.load(pacman_animations[animation_counter])
            self.image = pygame.transform.rotate(temp, 180)

    def nextmove(self, wall):  # Stocke la prochaine instruction de mouvement donnée par le joueur
        if self.next_direction == 1:
            self.colliderbox.y -= self.speed
        if self.next_direction == 2:
            self.colliderbox.y += self.speed
        if self.next_direction == 3:
            self.colliderbox.x -= self.speed
        if self.next_direction == 4:
            self.colliderbox.x += self.speed

        for i in range(len(wall)):  # En cas de collision avec un mur, on annule le dernier mouvement
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

        if self.next_direction == 1:  # Utile pour calculer la légitimité du prochain mouvement, si il n'est pas valide on continuera dans la direction actuelle
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

    def move(self, wall):  # Fonction de déplacement du Pac-Man
        next = self.nextmove(wall)
        if next == 1:
            if self.next_direction == 1:
                self.next_direction = 0
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

        if self.direction == 1:  # up
            self.colliderbox.y -= self.speed
        if self.direction == 2:  # down
            self.colliderbox.y += self.speed
        if self.direction == 3:  # left
            self.colliderbox.x -= self.speed
        if self.direction == 4:  # right
            self.colliderbox.x += self.speed

        for i in range(len(wall)):  # Empeche de passer à travers un mur
            if self.colliderbox.colliderect(wall[i].colliderbox):
                if self.direction == 1:
                    self.colliderbox.y += self.speed
                if self.direction == 2:
                    self.colliderbox.y -= self.speed
                if self.direction == 3:
                    self.colliderbox.x += self.speed
                if self.direction == 4:
                    self.colliderbox.x -= self.speed
