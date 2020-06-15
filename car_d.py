import pygame
import random
import time
import nnGame
import numpy as np

pygame.init()

# colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (53, 115, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)


playerImg = pygame.image.load('car1.png')
enemyImg = pygame.image.load('car.png')

car_width = 70
car_height = 141

game_width = 600
game_height = 800

gameDisplay = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption('Tejas GAME')
clock = pygame.time.Clock()


def obstacle(x, y):
    gameDisplay.blit(enemyImg, (x, y))


def car(x, y):
    gameDisplay.blit(playerImg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def text_on_left(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def small_text(str_val, color, x, y):
    smalltext = pygame.font.Font('freesansbold.ttf', 15)
    textSurf, textRect = text_on_left(str_val, smalltext, color)
    textRect.center = (x, y)

    gameDisplay.blit(textSurf, textRect)


def message_display(str_val):
    largeText = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_objects(str_val, largeText)
    textRect.center = ((game_width/2), (game_height/2))

    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()


def crash():
    message_display('You Crashed')


def car_collision(e_x, e_y, x, y):
    for i in range(len(e_x)):
        if e_x[i] == x and y-car_height < e_y[i] < y:
            return True
    return False


def input_learn_line():
    pygame.draw.rect(gameDisplay, green, [0, 400, game_width, 2])  # M1


def show_highway():
    pygame.draw.rect(gameDisplay, black, [255, 0, 10, game_height])     # M1
    pygame.draw.rect(gameDisplay, black, [335, 0, 10, game_height])     # M2
    pygame.draw.rect(gameDisplay, black, [175, 0, 10, game_height])     # L
    pygame.draw.rect(gameDisplay, black, [415, 0, 10, game_height])     # R


def get_enemies():
    e_pos = [185, 265, 345]
    z = [random.randrange(0, 3) for i in range(2)]
    e_x = []
    if z[0] != z[1]:
        e_x = [e_pos[z[i]] for i in range(2)]
    else:
        e_x.append(e_pos[z[0]])

    e_y = [-(random.randrange(300, 400)) for i in range(2)]
    e_speed = [random.randrange(5, 10) for i in range(2)]

    return e_pos, e_x, e_y, e_speed


def get_player_pos(val, e_pos):
    for i in range(len(e_pos)):
        if val == e_pos[i]:
            return i/2.0
    return 0


def get_e_pos(data_list, e_list, e_pos):
    indexes = []
    for each in e_pos:
        if each in e_list:
            val = e_pos.index(each) + 1         # lane number
            indexes.append(val)
    for each in range(len(e_pos)):
        data_list.append(0)
    for each in indexes:
        data_list[each] = 1
    return data_list


def autonomous_move(val):
    pixel_move = 0
    if val == 0.1:      # no move
        return pixel_move
    elif val == 0.2:    # move right
        return 80
    elif val == 0.3:  # move left
        return -80
    elif val == 0.4:  # move right right
        return 160
    elif val == 0.5:  # move left left
        return -160

    return pixel_move


def check_input_line(y_list):
    for each in y_list:
        if each > 400:
            return True
    return False


def game_loop(nn_weights):

    # enemy spawn 1
    e_pos, e_x, e_y, e_speed = get_enemies()

    x = (game_width * 0.5) - (car_width * 0.5)
    y = game_height * 0.8

    gameExit = False
    go_left = False
    go_right = False
    autonomous = False
    green_line_touched = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    go_left = True
                elif event.key == pygame.K_RIGHT:
                    go_right = True
                if event.key == pygame.K_SPACE:
                    if autonomous:
                        autonomous = False
                    else:
                        autonomous = True

        gameDisplay.fill(white)
        car(x, y)

        green_line_touched = check_input_line(e_y)
        if not autonomous:
            if go_left:
                go_left = False
                x -= 80
            elif go_right:
                go_right = False
                x += 80
            small_text('autonomous mode:OFF', red, 90, 50)
        else:
            if green_line_touched:
                p_pos = get_player_pos(x, e_pos)
                input_data = [1]
                input_data = get_e_pos(input_data, e_x, e_pos)
                input_data.append(1)
                input_data.append(1)    # bias val
                input_data.append(p_pos)
                input_data = np.array([input_data])
                move_car = nnGame.predict(nn_weights, input_data)
                x += autonomous_move(move_car)
            small_text('autonomous mode:ON', red, 90, 50)

        # enemy control
        e_y[0] += e_speed[0]
        e_y[1] += e_speed[1]
        obstacle(e_x[0], e_y[0])
        if len(e_x) > 1:
            obstacle(e_x[1], e_y[1])
        if e_y[0] > game_height + car_height and e_y[1] > game_height + car_height:
            e_pos, e_x, e_y, e_speed = get_enemies()
            green_line_touched = False

        # enemy collision
        if car_collision(e_x, e_y, x, y):
            crash()

        # other render
        show_highway()
        input_learn_line()
        small_text('Input Line', green, 90, 410)

        if x > e_pos[2] + 10 or x < e_pos[0] - 10:
            crash()
        pygame.display.update()

        clock.tick(60)     # fps


if __name__ == '__main__':
    weights = nnGame.training()
    game_loop(nn_weights=weights)
    pygame.quit()
