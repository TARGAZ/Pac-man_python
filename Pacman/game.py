import pygame
from wall import *
from point import *
from fruits import *
import dijkstar
import heapq


class game:
    def __init__(self):
        self.score = 0
        self.graph = dijkstar.Graph()
        self.level = 0

    def load(self, screen, pacman, map, wall, point, bigPoint, red, blue, pink, yellow, i, j):  # Chargement des éléments de la map

        if map.ascii_maze[i][j] == 'X':  # Murs
            wall1 = Wall()
            wall1.colliderbox.x = j * 25
            wall1.colliderbox.y = i * 25
            screen.blit(wall1.image, wall1.colliderbox)
            wall.append(wall1)

        if map.ascii_maze[i][j] == 'O':  # Murs d'entrée/sortie de la grotte des fantomes
            wall1 = Wall()
            wall1.colliderbox.x = j * 25
            wall1.colliderbox.y = i * 25
            screen.blit(wall1.image, wall1.colliderbox)
            wall1.Owall = 1
            wall.append(wall1)

        if map.ascii_maze[i][j] == 'o': # Super-gommes
            bigPoint1 = BigPoint()
            bigPoint1.colliderbox.x = j * 25
            bigPoint1.colliderbox.y = i * 25
            screen.blit(bigPoint1.image, bigPoint1.colliderbox)
            bigPoint.append(bigPoint1)

        if map.ascii_maze[i][j] == '.':  # gommes
            point1 = Point()
            point1.colliderbox.x = j * 25
            point1.colliderbox.y = i * 25
            screen.blit(point1.image, point1.colliderbox)
            point.append(point1)

        if map.ascii_maze[i][j] == 'P':  # Pac-Man
            pacman.colliderbox.x = j * 25
            pacman.colliderbox.y = i * 25
            screen.blit(pacman.image, pacman.colliderbox)

        if map.ascii_maze[i][j] == 'G':  # fantomes
            if red.is_loaded == 0:  # On vérifie si il est chargé
                red.colliderbox.x = j * 25  # échelle affichage écran / taille matrice
                red.colliderbox.y = i * 25
                screen.blit(red.image, red.colliderbox)
                red.is_loaded = 1
                red.start_node = (i, j)  # Noeud du point de départ (pour Dijkstra)

            elif blue.is_loaded == 0:
                blue.colliderbox.x = j * 25
                blue.colliderbox.y = i * 25
                screen.blit(blue.image, blue.colliderbox)
                blue.is_loaded = 1
                blue.start_node = (i, j)

            elif pink.is_loaded == 0:
                pink.colliderbox.x = j * 25
                pink.colliderbox.y = i * 25
                screen.blit(pink.image, pink.colliderbox)
                pink.is_loaded = 1
                pink.start_node = (i, j)

            elif yellow.is_loaded == 0:
                yellow.colliderbox.x = j * 25
                yellow.colliderbox.y = i * 25
                screen.blit(yellow.image, yellow.colliderbox)
                yellow.is_loaded = 1
                yellow.start_node = (i, j)

    def update(self, screen, pacman, map, wall, point, bigPoint, red, blue, pink, yellow, map_texture, fruits):  # Mise à jour des éléments à l'écran
        i = 0
        screen.fill((0, 0, 0))  # On remplit l'écran de noir pour le "nettoyer"

        if fruits != None:  # Affichage des fruits
            fruits.colliderbox.x = fruits.position[0] * 25
            fruits.colliderbox.y = fruits.position[1] * 25
            screen.blit(fruits.image, fruits.colliderbox)

        for i in range(len(wall)):  # Affichage des murs
            screen.blit(wall[i].image, wall[i].colliderbox)
        for i in range(len(point)):   # Affichage des gommes
            screen.blit(point[i].image, point[i].colliderbox)
        for i in range(len(bigPoint)):   # Affichage des super-gommes
            screen.blit(bigPoint[i].image, bigPoint[i].colliderbox)

        screen.blit(pacman.image, pacman.colliderbox)
        pacman.current_node = (int(pacman.colliderbox.y / 25), int(pacman.colliderbox.x / 25))  # Noeud actuel de Pac-Man

        if (red.weak == 1):  # Changement de la texture si le fantome est vulnérable
            screen.blit(red.imgweak, red.colliderbox)
        elif (red.weak == 2):  # Si le fantome est tué, changement de sa texture en oeil (orienté selon direction)
            if red.direction == 1:
                red.eye = pygame.image.load("assets/ghosts/eye_up.png")
            if red.direction == 2:
                red.eye = pygame.image.load("assets/ghosts/eye_down.png")
            if red.direction == 3:
                red.eye = pygame.image.load("assets/ghosts/eye_left.png")
            if red.direction == 4:
                red.eye = pygame.image.load("assets/ghosts/eye_right.png")
            screen.blit(red.eye, red.colliderbox)
        else:
            screen.blit(red.image, red.colliderbox)

        if (blue.weak == 1):
            screen.blit(blue.imgweak, blue.colliderbox)
        elif (blue.weak == 2):
            if blue.direction == 1:
                blue.eye = pygame.image.load("assets/ghosts/eye_up.png")
            if blue.direction == 2:
                blue.eye = pygame.image.load("assets/ghosts/eye_down.png")
            if blue.direction == 3:
                blue.eye = pygame.image.load("assets/ghosts/eye_left.png")
            if blue.direction == 4:
                blue.eye = pygame.image.load("assets/ghosts/eye_right.png")
            screen.blit(blue.eye, blue.colliderbox)
        else:
            screen.blit(blue.image, blue.colliderbox)

        if (pink.weak == 1):
            screen.blit(pink.imgweak, pink.colliderbox)
        elif (pink.weak == 2):
            if pink.direction == 1:
                pink.eye = pygame.image.load("assets/ghosts/eye_up.png")
            if pink.direction == 2:
                pink.eye = pygame.image.load("assets/ghosts/eye_down.png")
            if pink.direction == 3:
                pink.eye = pygame.image.load("assets/ghosts/eye_left.png")
            if pink.direction == 4:
                pink.eye = pygame.image.load("assets/ghosts/eye_right.png")
            screen.blit(pink.eye, pink.colliderbox)
        else:
            screen.blit(pink.image, pink.colliderbox)

        if (yellow.weak == 1):
            screen.blit(yellow.imgweak, yellow.colliderbox)
        elif (yellow.weak == 2):
            if yellow.direction == 1:
                yellow.eye = pygame.image.load("assets/ghosts/eye_up.png")
            if yellow.direction == 2:
                yellow.eye = pygame.image.load("assets/ghosts/eye_down.png")
            if yellow.direction == 3:
                yellow.eye = pygame.image.load("assets/ghosts/eye_left.png")
            if yellow.direction == 4:
                yellow.eye = pygame.image.load("assets/ghosts/eye_right.png")
            screen.blit(yellow.eye, yellow.colliderbox)
        else:
            screen.blit(yellow.image, yellow.colliderbox)

        # On charge la police des logos puis on applique font.render() sur 3 textes
        font = pygame.font.Font("assets/fonts/PAC-FONT.ttf", 36)
        text_pacman = font.render("pacman", True, (255, 255, 0))
        text_by = font.render("BY", True, (255, 255, 0))
        text_esiea = font.render("esiea", True, (54, 169, 225))
        # On affiche à l'écran les 3 textes générés juste au dessus
        screen.blit(text_pacman, (750, 10))
        screen.blit(text_by, (810, 60))
        screen.blit(text_esiea, (775, 110))

        # On affiche le score et le niveau actuel
        font = pygame.font.Font("assets/fonts/Emulogic.ttf", 26)
        text_score = font.render('Score:', True, (255, 255, 255))
        text_var_gamescore = font.render(str(self.score), True, (255, 255, 255))
        text_level = font.render("Level ", True, (255, 255, 255))
        text_var_level = font.render(str(self.level + 1), True, (255, 255, 255))

        screen.blit(text_score, (770, 260))
        screen.blit(text_var_gamescore, (770, 300))
        screen.blit(text_level, (770, 200))
        screen.blit(text_var_level, (910, 200))

        screen.blit(map_texture.texture, map_texture.collidebox)  # affichage de la map
        pacman.display_remaining_lives(screen)  # Affichage des vies restantes sur le bord de l'écran

    def restart(self, screen, pacman, map, wall, point, bigPoint, red, blue, pink, yellow):  # On reprend la partie après la mort de Pac-Man
        if pacman.life == 0:  # On quitte le jeu si jamais on a épuisé toutes nos vies
            pygame.quit()
            exit()
        else:
            i = 0
            pacman.life -= 1
            red.is_out = 0
            blue.is_out = 0
            pink.is_out = 0
            yellow.is_out = 0
            red.is_loaded = 0
            blue.is_loaded = 0
            pink.is_loaded = 0
            yellow.is_loaded = 0

            for i in range(len(map.ascii_maze[i])):
                for j in range(len(map.ascii_maze)):
                    if map.ascii_maze[j][i] == 'P':
                        pacman.colliderbox.x = i * 25
                        pacman.colliderbox.y = j * 25
                    if map.ascii_maze[j][i] == 'G':
                        if red.is_loaded == 0:
                            red.colliderbox.x = i * 25
                            red.colliderbox.y = j * 25
                            red.is_loaded = 1
                        elif blue.is_loaded == 0:
                            blue.colliderbox.x = i * 25
                            blue.colliderbox.y = j * 25
                            blue.is_loaded = 1
                        elif pink.is_loaded == 0:
                            pink.colliderbox.x = i * 25
                            pink.colliderbox.y = j * 25
                            pink.is_loaded = 1
                        elif yellow.is_loaded == 0:
                            yellow.colliderbox.x = i * 25
                            yellow.colliderbox.y = j * 25
                            yellow.is_loaded = 1

    def typevoisin(self, map, i, j):  # Poids des éléments pour Dijkstra
        if map.ascii_maze[i][j] == 'X':
            return 100
        elif map.ascii_maze[i][j] == 'o':
            return 1
        elif map.ascii_maze[i][j] == '.':
            return 1
        elif map.ascii_maze[i][j] == 'P':
            return 1
        elif map.ascii_maze[i][j] == 'G':
            return 1
        elif map.ascii_maze[i][j] == ' ':
            return 1
        elif map.ascii_maze[i][j] == 'O':
            return 1
        else:
            return 1000

    def creeGraph(self, map, red, blue, pink, yellow, pacman):  # Crée le graph pour les calculs de Dijktra
        for i in range(0, len(map.ascii_maze)):
            for j in range(0, len(map.ascii_maze[i])):

                if i > 0:  # Les 4 if servent à éviter les bords
                    if map.ascii_maze[i][j] == 'P':
                        pacman.current_node = (i, j)
                    self.graph.add_edge((i, j), (i - 1, j), self.typevoisin(map, i, j))  # On ajoute un noeud avec les coordonnées (i, j), les coordonnées du voisin et le poids de notre case

                if i < len(map.ascii_maze) - 1:
                    if map.ascii_maze[i][j] == 'P':
                        pacman.current_node = (i, j)
                    self.graph.add_edge((i, j), (i + 1, j), self.typevoisin(map, i, j))

                if j > 0:
                    if map.ascii_maze[i][j] == 'P':
                        pacman.current_node = (i, j)
                    self.graph.add_edge((i, j), (i, j - 1), self.typevoisin(map, i, j))

                if j < len(map.ascii_maze[i]) - 1:
                    if map.ascii_maze[i][j] == 'P':
                        pacman.current_node = (i, j)
                    self.graph.add_edge((i, j), (i, j + 1), self.typevoisin(map, i, j))

        # On relie manuellement les 2 tunnels (wrap-around) pour Dijkstra
        self.graph.add_edge((14, 0), (14, 27), 1)
        self.graph.add_edge((14, 27), (14, 0), 1)

    def dijkstra(self, start, end):  # Cherche le plus court chemin entre les nœuds start et end
        distances = {vertex: float('infinity') for vertex in self.graph}  # initialise le dictionnaire distances en mettant chaque valeur à l'infini
        previous_vertices = {vertex: None for vertex in self.graph}  # initialise le dictionnaire previous_vertices qui stocke les noeuds précédents de chaque noeud et les mettant à None
        distances[start] = 0  # Distance du noeud de départ à 0
        queue = [(0, start)]  # File d'attente du test de chemin le plus cours. la première valeur est définie à (0, start)
        while queue:  # tant qu'il y a des éléments dans la file d'attente
            current_distance, current_vertex = heapq.heappop(queue)  # On prend le prochain noeud de la file (le plus court actuel)

            if current_distance > distances[current_vertex]:  # On vérifie si la distance actuelle est plus grande que la distance enregistrée pour ce noeud
                continue
            for neighbor, weight in self.graph[current_vertex].items():  # Pour chaque voisin du noeud actuel, on regarde si il existe une distance plus courte
                distance = current_distance + weight
                if distance < distances[neighbor]:  # Si cette distance est plus courte que celle enregistrée on remplace le noeud
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = current_vertex
                    heapq.heappush(queue, (distance, neighbor))  # ajoute le voisin à la file puor le prochain test
            if current_vertex == end:  # Si le nœud actuel est celui d'arrivée, fin de la boucle
                break
        path = []  # Tableau pour stocker le chemin final
        vertex = end # Le nœud actuel est celui d'arrivée
        while vertex is not None:  # Tant qu'il y a des éléments dans vertex
            path.append(vertex)  # on ajoute le nœud au chemin
            vertex = previous_vertices[vertex]  # on passe au nœud suivant
        path.reverse()  # inverse l'ordre des cases du tableau
        return path  # renvoie le chamin
