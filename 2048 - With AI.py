import random
import time

import pygame
import lists_2048
reset = False

color_list = lists_2048.color_list
cord_list = lists_2048.cord_list()


class Block:
    def __init__(self, number, location):
        self.size = 86
        self.number = number
        self.location = location
        self.color = color_list.get(number)

    def create_block(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(
            442 + ((self.location[0] - 1) * 89), 162 + ((self.location[1] - 1) * 89), self.size, self.size
        ))

    def move(self, x_change, y_change):
        global score
        try:
            for i in range(4):
                if not cord_list[self.location[0] + x_change, self.location[1] + y_change]:
                    place_holder = cord_list[self.location]
                    cord_list[self.location] = False
                    self.location = (self.location[0] + x_change, self.location[1] + y_change)
                    cord_list[self.location] = place_holder
                elif cord_list[self.location[0] + x_change, self.location[1] + y_change].number == self.number:
                    self.number += self.number
                    score += self.number
                    place_holder = cord_list[self.location]
                    self.color = color_list.get(self.number)
                    cord_list[self.location[0], self.location[1]] = place_holder
                    cord_list[self.location[0] + x_change, self.location[1] + y_change] = False
        except:
            pass


def spawn_block():
    finding_location = True
    while finding_location:
        if False in cord_list.values():
            x = random.randint(1, 4)
            y = random.randint(1, 4)
            if not cord_list[x, y]:
                num = 4 if random.randint(1, 10) == 10 else 2
                create_blk = Block(num, (x,y))
                create_blk.create_block()
                cord_list[x, y] = create_blk
                finding_location = False
            else:
                pass
        else:
            global running, reset
            finding_location = False
            reset = True


def move(direction):
    if direction == 'up':
        for item in cord_list:
            if cord_list[item] != False:
                cord_list[item].move(0,-1)
    elif direction == 'left':
        for item in cord_list:
            if cord_list[item] != False:
                cord_list[item].move(-1,0)
    elif direction == 'down':
        for item in cord_list.__reversed__():
            if cord_list[item] != False:
                cord_list[item].move(0, 1)
    elif direction == 'right':
        for item in cord_list.__reversed__():
            if cord_list[item] != False:
                cord_list[item].move(1, 0)
    spawn_block()


def draw_board():
    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(440, 160, 356, 356))
    for x in range(440, 790, 89):
        for y in range(160, 510, 89):
            pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(x, y, 90, 90), 2)

'''VARIABLES'''
direction = None
running = True
score = 0
screen = pygame.display.set_mode((1280, 720))


def run_game():
    global running, direction, screen, score, cord_list, reset
    direction = None
    running = True
    score = 0
    pygame.init()
    pygame.display.set_caption("2048 - AI")
    clock = pygame.time.Clock()
    screen.fill("grey")
    draw_board()
    spawn_block()
    while running:
        if reset:
            pygame.time.wait(1000)
            running = True
            cord_list = lists_2048.cord_list()
            score = 0
            reset = False
            screen.fill("grey")
            draw_board()
            spawn_block()
            pygame.display.update()
        direction = ai()
        pygame.display.update()
        if direction:
            pygame.display.update()
            move(direction)
            draw_board()
            for item in cord_list:
                if cord_list[item] != False:
                    cord_list[item].create_block()
            direction = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def simulate_move(direction):
    board_copy = get_state()
    score_copy = score
    x_change = 0
    y_change = 0
    if direction == 'right':
        x_change = 1
    elif direction == 'left':
        x_change = -1
    elif direction == 'up':
        y_change = -1
    elif direction == 'down':
        y_change = 1
    if direction == 'down' or direction == 'right':
        for t in range(4):
            for y in range(0, 4):
                for x in range(0, 4):
                    try:
                        if board_copy[y][x] != 0:
                            if board_copy[y + y_change][x + x_change] == 0:
                                board_copy[y + y_change][x + x_change] = board_copy[y][x]
                                board_copy[y][x] = 0
                            elif board_copy[y + y_change][x + x_change] == board_copy[y][x]:
                                board_copy[y + y_change][x + x_change] = board_copy[y][x] * 2
                                board_copy[y][x] = 0
                                score_copy += board_copy[y + y_change][x + x_change]
                    except:
                        pass
    else:
        for t in range(4):
            for y in range(4, 0, -1):
                for x in range(4, 0, -1):
                    try:
                        if board_copy[y][x] != 0:
                            if board_copy[y + y_change][x + x_change] == 0:

                                board_copy[y + y_change][x + x_change] = board_copy[y][x]
                                board_copy[y][x] = 0
                            elif board_copy[y + y_change][x + x_change] == board_copy[y][x]:
                                board_copy[y + y_change][x + x_change] = board_copy[y][x] * 2
                                board_copy[y][x] = 0
                                score_copy += board_copy[y + y_change][x + x_change]
                    except:
                        pass

    return score_copy, board_copy


def get_state():
    state = [[0 for _ in range(4)]for _ in range(4) ]
    for (x, y), block in cord_list.items():
        if block is not False:
            state[y - 1][x - 1] = block.number
    return state


def ai():
    best_move = None
    best_reward = -9999999999999999
    for sim_move in ['down', 'up', 'left', 'right']:
        get_reward(sim_move)
        if get_reward(sim_move) > best_reward:
            best_reward = get_reward(sim_move)
            best_move = sim_move
    return best_move


def get_reward(sim_move):
    game_over = False
    tiles_next_to_others = 0
    simulated_score, simulated_board = simulate_move(sim_move)
    tiles_left = 0
    if 0 not in simulated_board:
        game_over = True
    for x_layer in simulated_board:
        for num in range(0,4):
            try:
                if x_layer[num - 1] == x_layer[num]:
                    tiles_next_to_others += 1
            except:
                pass
            try:
                if x_layer[num + 1] == x_layer[num]:
                    tiles_next_to_others += 1
            except:
                pass
            for y_range in range(0,4):
                try:
                    if simulated_board[y_range + 1][num] == simulated_board[y_range][num]:
                        tiles_next_to_others += 1
                except:
                    pass
                try:
                    if simulated_board[y_range - 1][num] == simulated_board[y_range][num]:
                        tiles_next_to_others += 1
                except:
                    pass

        for y_num in x_layer:
            if y_num != 0:
                tiles_left += 1
        

    reward = ((simulated_score) * (tiles_next_to_others - tiles_left))
    if game_over:
        reward = -9999999999999998
    return reward

run_game()
