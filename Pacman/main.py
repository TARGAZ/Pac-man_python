# IMPORTATIONS
import pygame
import sys
from pacman import *
from map import *
from game import *
from wall import *
from point import *
from fantome import *
from fruits import *

# INITIALISATIONS
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 800))
pygame.display.update()

map = Map()
map_texture = Map_texture()
pacman = Pacman()
game = game()
red = red()
blue = blue()
pink = pink()
yellow = yellow()
wall = []
point = []
bigPoint = []
animation_counter = 0
ghost_timeout = 0
time = 0
printobject = 0
musique_intro_has_been_played: bool = False
fruits = None

musique_pacman_intro = pygame.mixer.Sound("assets/audio/pacman_intro.wav")
musique_pacman_death = pygame.mixer.Sound("assets/audio/pacman_death.wav")
musique_pacman_siren = pygame.mixer.Sound("assets/audio/pacman_siren.wav")
musique_pacman_eat = pygame.mixer.Sound("assets/audio/pacman_eat.wav")
musique_pacman_eat_fruit = pygame.mixer.Sound("assets/audio/pacman_eat_fruit.wav")
musique_pacman_kill_ghost = pygame.mixer.Sound("assets/audio/pacman_kill_ghost.wav")


# chargement de la map avec tous les éléments (points, fantomes, murs...)
for i in range(len(map.ascii_maze)):
    for j in range(len(map.ascii_maze[i])):
        game.load(screen, pacman, map, wall, point, bigPoint, red, blue, pink, yellow, i, j)

game.creeGraph(map, red, blue, pink, yellow, pacman)  # Création d'un graph utilisé plus tard pour Dijkstra

# Boucle principale du jeu
while True:
    gameclock = clock.tick(20)  # horloge globale du jeu

    keys = pygame.key.get_pressed()   # initialisation et détection des touches pressées
    for event in pygame.event.get():
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        if keys[pygame.K_UP]:
            pacman.next_direction = 1
        if keys[pygame.K_DOWN]:
            pacman.next_direction = 2
        if keys[pygame.K_LEFT]:
            pacman.next_direction = 3
        if keys[pygame.K_RIGHT]:
            pacman.next_direction = 4
        if keys[pygame.K_b]:  # mode niveau 256
            map_texture.texture = pygame.image.load("assets/map/map_256.png")
        if keys[pygame.K_s]:  # ajout de 5000 au score
            game.score += 5000
        if keys[pygame.K_l]:  # on change de level à la volée
            game.level += 1

    if gameclock % 1 == 0:  # à chaque tick, appel des fonctions de déplacement
        pacman.move(wall)
        red.move_red(wall, pacman, game)
        blue.move_blue(wall, pacman, game)
        pink.move_pink(wall, pacman, game)
        yellow.move_yellow(wall, game)
        printobject += 1  # compteur pour savoir quand fait apparaitre un fruit

    if printobject % 320 == 0:  # apparition des fruits selon le niveau
        if game.level == 0:
            fruits = Cherry()
        if game.level == 1:
            fruits = Strawberry()
        if game.level in range(2, 3):
            fruits = Orange()
        if game.level in range(4, 5):
            fruits = Apple()
        if game.level in range(6, 7):
            fruits = Melon()
        if game.level in range(8, 9):
            fruits = Galaxian()
        if game.level in range(10, 11):
            fruits = Bell()
        if game.level > 11:
            fruits = Key()

    if fruits != None:  # Si un fruit est sur la map, on surveille si Pac-Man le mange
        if pacman.colliderbox.colliderect(fruits.colliderbox):
            game.score += fruits.value  # On ajoute le score correpondant au fruit
            musique_pacman_eat_fruit.play()  # Lecture du son associé
            fruits = None  # Disparition du fruit

    pacman.moving_animation(animation_counter)  # animation du Pac-Man (mouvement de bouche et orientation)
    animation_counter += 1
    if animation_counter > 3:  # il n'y a que 4 cases dans le tableau d'animation
        animation_counter = 0

    for i in range(len(point)):  # Vérification de colision avec les gommes
        if pacman.colliderbox.colliderect(point[i].colliderbox):
            game.score += 10
            musique_pacman_eat.play()
            point.pop(i)  # on retire la gomme du tableau
            break

    for i in range(len(bigPoint)):  # Véfication des super-gommes
        if pacman.colliderbox.colliderect(bigPoint[i].colliderbox):
            game.score += 50
            powerOn(red, pink, blue, yellow, pacman)  # Activation de la vulnérabilité des fantomes
            ghost_timeout += 150  # Durée du pouvoir
            red.imgweak = pygame.image.load("assets/ghosts/ghost_dead.png")
            blue.imgweak = pygame.image.load("assets/ghosts/ghost_dead.png")
            yellow.imgweak = pygame.image.load("assets/ghosts/ghost_dead.png")
            pink.imgweak = pygame.image.load("assets/ghosts/ghost_dead.png")
            bigPoint.pop(i)  # On retire la super-gomme du tableau
            break
    # à la fin du timeout, on désactive la vulnérabilité des fantomes
    if ghost_timeout < 0:
        powerOff(red, pink, blue, yellow, pacman)
        ghost_timeout = 0
    else:
        ghost_timeout -= 1

    if ghost_timeout in range(1,30):  # Couleur différente à l'approche de la fin de la vunérabilité
        red.imgweak = pygame.image.load("assets/ghosts/ghost_dead_white.png")
        blue.imgweak = pygame.image.load("assets/ghosts/ghost_dead_white.png")
        yellow.imgweak = pygame.image.load("assets/ghosts/ghost_dead_white.png")
        pink.imgweak = pygame.image.load("assets/ghosts/ghost_dead_white.png")

    # Permet à Pac-Man et aux fantomes d'emprunter le tunnel
    pacman.pacman_wrap_around()
    red.ghost_wrap_around()
    pink.ghost_wrap_around()
    blue.ghost_wrap_around()
    yellow.ghost_wrap_around()

    # Si Pac-Man se fait attraper par un fantome
    if (pacman.colliderbox.colliderect(red.colliderbox) and red.weak == 0) or \
            (pacman.colliderbox.colliderect(blue.colliderbox) and blue.weak == 0) or \
            (pacman.colliderbox.colliderect(pink.colliderbox) and pink.weak == 0) or \
            (pacman.colliderbox.colliderect(yellow.colliderbox) and yellow.weak == 0):
        musique_pacman_siren.stop()  # Arret de la musique principale
        musique_pacman_death.play()  # on joue le jingle de mort
        death_animation_counter = 0  # index du tableau d'animation
        while pygame.mixer.get_busy():  # tant que le jingle dure
            pygame.display.update()  # mise à jour de l'affichage
            if clock.tick(20) % 10 == 1 and death_animation_counter <= 11:  # on met du délai entre les éxécutions
                pacman.death_animation(death_animation_counter)  # fonction qui charge la bonne texture dans pacman.image
                game.update(screen, pacman, map, wall, point, bigPoint, red, blue, pink, yellow, map_texture, fruits)  # mise à jour des éléments à l'écran
                death_animation_counter += 1  # on augmente l'index de 1 (donc on passe à l'image suivante)
        pacman.image = pygame.image.load("assets/pacman/pacman0.png")  # Pour le respawn, on remet la bonne texture sur Pac-Man
        game.restart(screen, pacman, map, wall, point, bigPoint, red, blue, pink, yellow)  # on reprend la partie
        direction = 0  # Pas de mouvement initial
        musique_intro_has_been_played = False  # On rejoue le jingle d'acceuil

    # Collision entre Pac-Man et un fantome vulnérable
    if pacman.colliderbox.colliderect(red.colliderbox):
        if red.weak == 1:  # Etat vulnérable
            red.weak = 2  # Etat mort (oeil qui retourne dans la grotte des fantomes)
            game.score += 200
            musique_pacman_kill_ghost.play()

    if pacman.colliderbox.colliderect(blue.colliderbox):
        if blue.weak == 1:
            blue.weak = 2
            game.score += 200
            musique_pacman_kill_ghost.play()

    if pacman.colliderbox.colliderect(pink.colliderbox):
        if pink.weak == 1:
            pink.weak = 2
            game.score += 200
            musique_pacman_kill_ghost.play()

    if pacman.colliderbox.colliderect(yellow.colliderbox):
        if yellow.weak == 1:
            yellow.weak = 2
            musique_pacman_kill_ghost.play()

    pacman.bonus_life_from_score(game.score)  # Ajout d'une vie supplémentaire pour chaque pallier de 10000 points de score

    if len(point) == 0 and len(bigPoint) == 0:  # Détection de fin de niveau (Pac-Man a mangé toutes les gommes et super-gommes)
        game.level += 1  # On passe au niveau suivant
        # Réinitialisation des éléments
        fruits = None
        blink = 0
        red.weak = 0
        blue.weak = 0
        pink.weak = 0
        yellow.weal = 0
        red.is_out = 0
        blue.is_out = 0
        pink.is_out = 0
        yellow.is_out = 0
        red.is_loaded = 0
        blue.is_loaded = 0
        pink.is_loaded = 0
        yellow.is_loaded = 0

        while blink < 5:  # On fait clignoter la map en bleu et blanc
            map_texture.texture = pygame.image.load("assets/map/map_white.png")
            screen.blit(map_texture.texture, map_texture.collidebox)  # affichage de la map
            pygame.display.update()  # mise à jour de l'affichage
            pygame.time.wait(300)
            map_texture.texture = pygame.image.load("assets/map/map.png")
            screen.blit(map_texture.texture, map_texture.collidebox)  # affichage de la map
            pygame.display.update()  # mise à jour de l'affichage
            pygame.time.wait(300)
            blink += 1

        # Chargement de tous les éléments de la map
        for i in range(len(map.ascii_maze)):
            for j in range(len(map.ascii_maze[i])):
                game.load(screen, pacman, map, wall, point, bigPoint, red, blue, pink, yellow, i, j)

        musique_pacman_siren.stop()
        musique_intro_has_been_played = False

    game.update(screen, pacman, map, wall, point, bigPoint, red, blue, pink, yellow, map_texture, fruits)  # Mise à jour des éléments à l'écran

    if game.level == 256:  # EasterEgg du bug du niveau 256
        map_texture.texture = pygame.image.load("assets/map/map_256.png")

    pygame.display.update()  # mise à jour de l'affichage

    if musique_intro_has_been_played == False:  # Si la musique d'intro n'a pas été jouée
        musique_pacman_intro.play()  # Jouer la musique d'intro
        musique_intro_has_been_played = True
        while pygame.mixer.get_busy():  # Tant que le jingle d'intro est en cours
            # On affiche le texte "READY!" à l'écran avant que la partie ne commence
            font = pygame.font.Font("assets/fonts/Emulogic.ttf", 20)
            text_ready = font.render("READY!", True, (255, 255, 0))
            screen.blit(text_ready, (300, 422))
            pygame.display.update()  # mise à jour de l'affichage
        musique_pacman_siren.play(loops=-1)  # lecture en boucle