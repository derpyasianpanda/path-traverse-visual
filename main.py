# The goal of this project is to gather many search algorithms and visualize them here
import math
import pygame
import numpy as np
import sys
from tile_queues import *
import os


class Tile:
    def __init__(self, coord1, coord2=0, weight=1, special="normal", state="path"):
        if isinstance(x, int):
            self.x = coord1
            self.y = coord2
        else:
            self.x, self.y = coord1
        self.coord = (self.x, self.y)
        self.weight = weight
        self.special = special
        self.state = state

    def __repr__(self):
        return f"A {self.special} {self.state} @ {self.x},{self.y}"

    def mark_special(self, special):
        self.special = special
        pygame.draw.rect(screen, colors[special],
                         (self.x * tile_width, self.y * tile_height, tile_width, tile_height))
        pygame.display.update()
        return special

    def update_state(self, state):
        self.state = state
        if self.special != "goal" and self.special != "start":
            pygame.draw.rect(screen, colors[state],
                             (self.x * tile_width, self.y * tile_height, tile_width, tile_height))
            pygame.display.update()
        return state


def get_distance(tile1, tile2):  # Euclidean distance between two points
    return math.sqrt(math.pow(tile1.x - tile2.x, 2) + math.pow(tile1.y - tile2.y, 2))


def get_distance_manhattan(tile1, tile2):  # Manhattan distance between two points
    return math.pow(tile1.x - tile2.x, 2) + math.pow(tile1.y - tile2.y, 2)


def get_traveled(tile):  # distance traveled from origin
    return tile.parent.g + get_distance(tile, tile.parent)


def get_dijkstra_score(tile):  # retrieve the tile's cost
    return tile.g * tile.weight


def get_f_score(tile):  # f-score for A* path-finding
    return tile.h + get_dijkstra_score(tile)


def within_board(x, y):  # checks if coords are in board
    return 0 <= x < grid_width \
           and 0 <= y < grid_height


def walkable(x, y):  # checks if its a wall
    return grid[x, y].state != "wall"


def get_valid_neighbor_coords(x, y):  # gets all the neighboring coordinates including diagonals
    # Order is N, E, S, W, NE, SE, SW, NW
    neighbors = [
        [x, y - 1],
        [x + 1, y],
        [x, y + 1],
        [x - 1, y]
    ]

    diagonals = [
        [x + 1, y - 1],
        [x + 1, y + 1],
        [x - 1, y + 1],
        [x - 1, y - 1]
    ]

    index = 0
    while index < len(neighbors):
        xn, yn = neighbors[index]
        if not within_board(xn, yn) \
                or not walkable(xn, yn):
            del neighbors[index]
        else:
            index = index + 1

    index = 0
    while index < len(diagonals):
        xd, yd = diagonals[index]
        if not within_board(xd, yd) \
                or not walkable(xd, yd) \
                or ([xd, y] not in neighbors and [x, yd] not in neighbors):
            del diagonals[index]
        else:
            index = index + 1

    neighbors += diagonals
    return neighbors


def a_star_search():
    for x in range(grid_width):
        for y in range(grid_height):
            grid[x, y].h = get_distance(grid[x, y], goal_tile)

    start_tile.f = get_f_score(start_tile)
    open_queue = AStarQueue()
    open_queue.insert(start_tile)

    while not open_queue.is_empty():
        best_tile = open_queue.remove()

        best_tile.update_state("closed")
        neighbors = get_valid_neighbor_coords(best_tile.x, best_tile.y)
        for x, y in neighbors:
            if grid[x, y].state == "closed":
                continue
            new_g = best_tile.g + get_distance(grid[x, y], best_tile)
            if grid[x, y] not in open_queue:
                if grid[x, y].special == "goal":
                    grid[x, y].g = new_g
                    grid[x, y].parent = best_tile
                    print(grid[x, y], f"Goal reached after {grid[x, y].g} units traveled")
                    return grid[x, y]
                open_queue.insert(grid[x, y])
                grid[x, y].update_state("open")

            try:
                if new_g < grid[x, y].g:
                    grid[x, y].g = new_g
                    grid[x, y].parent = best_tile
                    grid[x, y].f = get_f_score(grid[x, y])
                    continue
            except:
                grid[x, y].g = new_g
                grid[x, y].parent = best_tile

            grid[x, y].f = get_f_score(grid[x, y])

    return None


def dijkstra_search():
    start_tile.d = get_dijkstra_score(start_tile)
    open_queue = DijkstraQueue()
    open_queue.insert(start_tile)

    while not open_queue.is_empty():
        best_tile = open_queue.remove()

        best_tile.update_state("closed")
        neighbors = get_valid_neighbor_coords(best_tile.x, best_tile.y)
        for x, y in neighbors:
            if grid[x, y].state == "closed":
                continue
            new_g = best_tile.g + get_distance(grid[x, y], best_tile)
            if grid[x, y] not in open_queue:
                if grid[x, y].special == "goal":
                    grid[x, y].g = new_g
                    grid[x, y].parent = best_tile
                    print(grid[x, y], f"Goal reached after {grid[x, y].g} units traveled")
                    return grid[x, y]
                open_queue.insert(grid[x, y])
                grid[x, y].update_state("open")

            try:
                if new_g < grid[x, y].g:
                    grid[x, y].g = new_g
                    grid[x, y].parent = best_tile
                    grid[x, y].d = get_dijkstra_score(grid[x, y])
                    continue
            except:
                grid[x, y].g = new_g
                grid[x, y].parent = best_tile

            grid[x, y].d = get_dijkstra_score(grid[x, y])

    return None


def greedy_first_search():
    for x in range(grid_width):
        for y in range(grid_height):
            grid[x, y].h = get_distance(grid[x, y], goal_tile)

    open_queue = GreedyQueue()
    open_queue.insert(start_tile)

    while not open_queue.is_empty():
        best_tile = open_queue.remove()

        best_tile.update_state("closed")
        neighbors = get_valid_neighbor_coords(best_tile.x, best_tile.y)
        for x, y in neighbors:
            if grid[x, y].state == "closed":
                continue
            if grid[x, y] not in open_queue:
                if grid[x, y].special == "goal":
                    print(grid[x, y], "Goal reached")
                    grid[x, y].parent = best_tile
                    return grid[x, y]
                open_queue.insert(grid[x, y])
                grid[x, y].update_state("open")
                grid[x, y].parent = best_tile

    return None


def breadth_first_search():
    open_queue = [start_tile]

    while len(open_queue) != 0:
        current_tile = open_queue.pop(0)

        if current_tile.state != "closed":
            current_tile.update_state("closed")

        neighbors = get_valid_neighbor_coords(current_tile.x, current_tile.y)
        for x, y in neighbors:
            if grid[x, y] not in open_queue and grid[x, y].state != "closed":
                if grid[x, y].special == "goal":
                    grid[x, y].parent = current_tile
                    print(grid[x, y], "Goal reached")
                    return grid[x, y]
                open_queue.append(grid[x, y])
                grid[x, y].update_state("open")
                grid[x, y].parent = current_tile


def depth_first_search():
    open_queue = [start_tile]

    while len(open_queue) != 0:
        current_tile = open_queue.pop(-1)

        if current_tile.state != "closed":
            current_tile.update_state("closed")

        neighbors = reversed(get_valid_neighbor_coords(current_tile.x, current_tile.y))
        for x, y in neighbors:
            if grid[x, y] not in open_queue and grid[x, y].state != "closed":
                if grid[x, y].special == "goal":
                    grid[x, y].parent = current_tile
                    print(grid[x, y], "Goal reached")
                    return grid[x, y]
                open_queue.append(grid[x, y])
                grid[x, y].update_state("open")
                grid[x, y].parent = current_tile


def on_mouse_press():
    global start_tile
    global goal_tile
    mx, my = pygame.mouse.get_pos()
    x = mx // (display_width // grid_width)
    y = my // (display_height // grid_height)
    rb, mb, lb = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    print(mx, my)
    print(rb, mb, lb)
    if rb:
        if keys[pygame.K_LCTRL]:
            if not grid[x, y] == goal_tile:
                start_tile.mark_special("normal")
                grid[start_tile.coord] = Tile(start_tile.coord)
                grid[x, y] = Tile(x, y)
                start_tile = grid[x, y]
                start_tile.mark_special("start")
                start_tile.g = 0
        elif keys[pygame.K_LALT]:
            if not grid[x, y] == start_tile:
                goal_tile.mark_special("normal")
                grid[goal_tile.coord] = Tile(goal_tile.coord)
                grid[x, y] = Tile(x, y)
                goal_tile = grid[x, y]
                goal_tile.mark_special("goal")
        else:
            if grid[x, y] != goal_tile and grid[x, y] != start_tile:
                grid[x, y].mark_special("normal")
                grid[x, y].update_state("wall")
    elif lb:
        if grid[x, y].state == "wall":
            grid[x, y].update_state("path")


def get_solution(search_type):
    solution: Tile = searches[search_type]()
    if solution:
        while True:
            try:
                solution.parent.mark_special("solution")
                solution = solution.parent
            except:
                solution.mark_special("start")
                break


def reset_board(hard):
    global grid
    global start_tile
    global goal_tile

    screen.fill(colors["path"])

    for x in range(grid_width):
        for y in range(grid_height):
            if hard:
                grid[x, y] = Tile(x, y)
            else:
                if grid[x, y].state == "wall":
                    grid[x, y] = Tile(x, y)
                    grid[x, y].update_state("wall")
                else:
                    grid[x, y] = Tile(x, y)

    start_tile = grid[start_tile.coord]
    start_tile.mark_special("start")
    start_tile.g = 0

    goal_tile = grid[goal_tile.coord]
    goal_tile.mark_special("goal")


def change_algorithm(algorithm):
    global current_search
    current_search = algorithm
    pygame.display.set_caption(f"{current_search} algorithm")


# Initial setup
colors = {
    "wall": (0, 0, 0),
    "closed": (0, 0, 255),
    "open": (102, 153, 255),
    "path": (255, 255, 255),
    "normal": (255, 255, 255),
    "goal": (255, 153, 0),
    "start": (255, 0, 0),
    "solution": (0, 255, 0)
}
searches = {
    "dijkstra's": dijkstra_search,
    "a*": a_star_search,
    "dfs": depth_first_search,
    "bfs": breadth_first_search,
    "greedy": greedy_first_search
}
display_width = 800
display_height = 800
sys.setrecursionlimit(1000000)
os.environ['SDL_VIDEO_CENTERED'] = "0"
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
screen.fill(colors["path"])
current_search = "a*"
pygame.display.set_caption(f"{current_search} algorithm")
grid_height = 100
grid_width = 100
tile_width = display_width // grid_width
tile_height = display_height // grid_height
grid = np.empty((grid_width, grid_height), object)
for x in range(grid_width):
    for y in range(grid_height):
        grid[x, y] = Tile(x, y)
# Initial setup


goal_tile = grid[99, 99]
goal_tile.mark_special("goal")

start_tile = grid[0, 0]
start_tile.g = 0
start_tile.mark_special("start")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Quitting")
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                print("Getting Solution")
                reset_board(False)
                get_solution(current_search)
            if event.key == pygame.K_F5:
                print("Refreshing")
                reset_board(True)
            if event.key == pygame.K_a:
                change_algorithm("a*")
            if event.key == pygame.K_d:
                change_algorithm("dijkstra's")
            if event.key == pygame.K_b:
                change_algorithm("bfs")
            if event.key == pygame.K_EQUALS:
                change_algorithm("dfs")
            if event.key == pygame.K_g:
                change_algorithm("greedy")
        if True in pygame.mouse.get_pressed():
            on_mouse_press()

    pygame.display.flip()
