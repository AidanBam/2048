import random
import pygame
import lists_2048

color_list = lists_2048.color_list
cord_list = lists_2048.cord_list


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
        try:
            for i in range(4):
                if not cord_list[self.location[0] + x_change, self.location[1] + y_change]:
                    place_holder = cord_list[self.location]
                    cord_list[self.location] = False
                    self.location = (self.location[0] + x_change, self.location[1] + y_change)
                    cord_list[self.location] = place_holder
                elif cord_list[self.location[0] + x_change, self.location[1] + y_change].number == self.number:
                    self.number += self.number
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
            global running
            pygame.time.wait(3000)
            running = False
            finding_location = False


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


def draw_board():
    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(440, 160, 356, 356))
    for x in range(440, 790, 89):
        for y in range(160, 510, 89):
            pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(x, y, 90, 90), 2)

'''VARIABLES'''
direction = None
running = True
screen = pygame.display.set_mode((1280, 720))


def run_game():
    global running, direction, screen
    pygame.init()
    pygame.display.set_caption("2048 - NO NN")
    clock = pygame.time.Clock()
    screen.fill("grey")
    draw_board()
    spawn_block()
    while running:
        clock.tick(60)
        pygame.display.flip()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            direction = 'up'
        elif keys[pygame.K_s]:
            direction = 'down'
        elif keys[pygame.K_d]:
            direction = 'right'
            move('right')
        elif keys[pygame.K_a]:
            direction = 'left'
        if direction is not None:
            move(direction)
            pygame.time.wait(300)
            draw_board()
            for item in cord_list:
                if cord_list[item] != False:
                    cord_list[item].create_block()
            spawn_block()
            direction = None

run_game()
