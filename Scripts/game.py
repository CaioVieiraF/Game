#!/usr/bin/env python
import pygame
import time
import random
from subprocess import call

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
dark_blue = (0, 0, 190)
yellow = (255, 255, 0)
dark_red = (190, 0, 0)
dark_green = (0, 190, 0)

display_width = 800
display_height = 600
len_x = 20
len_y = 20
coin = 30
changeVar = 10
direction = "right"
pause = False

with open('packages/save.txt') as f:
    file = f.read().split(",")
    savePT = file[1]


img = pygame.image.load('packages/sprites/Snake_sprite.png')
appleImg = pygame.image.load('packages/sprites/apple_sprite.png')

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake')
pygame.display.set_icon(appleImg)

clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
bigfont = pygame.font.SysFont("comicsansms", 80)


def coinLoc():
    coin_x = round(random.randrange(0, display_width-coin))
    coin_y = round(random.randrange(0, display_height-coin))
    return coin_x, coin_y


def py_quit():
    gameDisplay.fill(black)
    pygame.display.update()
    time.sleep(1)
    pygame.quit()
    quit()


def snake(lengthList, len_x, len_y):

    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    elif direction == "left":
        head = pygame.transform.rotate(img, 90)
    elif direction == "up":
        head = pygame.transform.rotate(img, 0)
    elif direction == "down":
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (lengthList[-1][0], lengthList[-1][1]))

    for XnY in lengthList[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], len_x, len_y])


def font_size(msg, size, color):
    font = pygame.font.SysFont("comicsansms", size)
    surf = font.render(msg, True, color)

    return surf


def text_obj(msg, color, size):
    if size == "small":
        Surf = smallfont.render(msg, True, color)
    elif size == "medium":
        Surf = medfont.render(msg, True, color)
    elif size == "big":
        Surf = bigfont.render(msg, True, color)
    else:
        Surf = font_size(msg, size, color)

    return Surf, Surf.get_rect()


def textScreen(txt, color, size="small", y_loc=0):
    textSurf, textRect = text_obj(txt, color, size)
    textRect.center = (display_width/2), (display_height/2)+y_loc
    gameDisplay.blit(textSurf, textRect)


def pontos(score):
    text = smallfont.render("Pontos: "+str(score), True, white)
    gameDisplay.blit(text, [20, 20])


def button(txt, color, loc, action=None):
    global pause

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if loc[0]+loc[2] > mouse[0] > loc[0] and loc[1]+loc[3] > mouse[1] > loc[1]:
        if click[0] == 1 and action is not None:
            if action == "play":
                gameLoop()
            if action == "quit":
                py_quit()
            if action == "cont":
                pause = False

        pygame.draw.rect(gameDisplay, color[1], loc)
    else:
        pygame.draw.rect(gameDisplay, color[0], loc)

    textSurf, textRect = text_obj(txt, black, 30)
    textRect.center = loc[0]+(loc[2]/2), loc[1]+(loc[3]/2)
    gameDisplay.blit(textSurf, textRect)


def pause_m():
    global pause
    pause = True
    textScreen("Pause", white, "big", -80)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                py_quit()

        button(
            "Continuar",
            [dark_green, green],
            [(display_width/2) - 50,
                (display_height/2)+25, 100, 50],
            action="cont"
        )
        button(
            "Sair",
            [dark_red, red],
            [(display_width/2)-50,
                (display_height/2)+85, 100, 50],
            action="quit"
        )

        pygame.display.update()


def menu(sv):
    gameMenu = True

    while gameMenu:
        gameDisplay.fill(dark_blue)
        textScreen("Snake", green, "big", -50)
        button(
            "Jogar!",
            [dark_green, green],
            [(display_width/2) - 50,
                (display_height/2)+25, 100, 50],
            action="play"
        )
        button(
            "Sair",
            [dark_red, red],
            [(display_width/2)-50,
                (display_height/2)+85, 100, 50],
            action="quit"
        )

        textScreen("Best: "+str(sv), white, y_loc=250)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                call(["clear"])
                print("bye!")
                py_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    gameLoop()
                    gameMenu = False
                elif event.key == pygame.K_ESCAPE:
                    gameMenu = False
                    call(["clear"])
                    print("bye!")
                    py_quit()


def gameLoop():
    global direction
    direction = "right"

    gameExit = False
    gameOver = False
    position_x = display_width/2
    position_y = display_height/2
    position_x_change = 20
    position_y_change = 0
    coin_x = round(random.randrange(0, display_width-len_x))
    coin_y = round(random.randrange(0, display_height-len_y))
    snakeSize = 1
    lengthList = []
    points = 0

    while not gameExit:

        while gameOver:
            gameDisplay.fill(dark_blue)
            textScreen("GAME OVER", red, "big", -20)
            button(
                "Tentar de novo",
                [dark_green, green],
                [(display_width/2)-100,
                 (display_height/2)+25, 200, 50],
                action="play")
            button(
                "Sair",
                [dark_red, red],
                [(display_width/2)-50,
                 (display_height/2)+85, 100, 50],
                action="quit"
            )
            textScreen("pontos: "+str(points), white, y_loc=200)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        direction = "right"
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    position_y_change = -len_y
                    position_x_change = 0
                    direction = "up"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    position_y_change = len_y
                    position_x_change = 0
                    direction = "down"
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    position_x_change = -len_x
                    position_y_change = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    position_x_change = len_x
                    position_y_change = 0
                    direction = "right"
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    gameExit = True
                elif event.key == pygame.K_p:
                    pause_m()

        outOfBound = [
            position_x > display_width-len_x,
            position_x < 0,
            position_y > display_height-len_y,
            position_y < 0
        ]
        if outOfBound[0] or outOfBound[1] or outOfBound[2] or outOfBound[3]:
            gameOver = True

        position_y += position_y_change
        position_x += position_x_change
        gameDisplay.fill(dark_blue)
        gameDisplay.blit(appleImg, [coin_x, coin_y])

        head = []
        head.append(position_x)
        head.append(position_y)
        lengthList.append(head)

        if len(lengthList) > snakeSize:
            del lengthList[0]

        for each in lengthList[:-1]:
            if head == each:
                gameOver = True

        snake(lengthList, len_x, len_y)

        pontos(snakeSize-1)

        pygame.display.update()

        position_x = int(position_x)
        position_y = int(position_y)
        coin_x = int(coin_x)
        coin_y = int(coin_y)

        getCoinX1 = [
            position_x > coin_x,
            position_x < coin_x+coin,
            position_x+len_x > coin_x,
            position_x+len_x < coin_x+coin
        ]
        getCoinY1 = [
            position_y > coin_y,
            position_y < coin_y+coin,
            position_y+len_y > coin_y,
            position_y+len_y < coin_y+coin
        ]
        if getCoinX1[0] and getCoinX1[1] or getCoinX1[2] and getCoinX1[3]:
            if getCoinY1[0] and getCoinY1[1] or getCoinY1[2] and getCoinY1[3]:
                coin_x, coin_y = coinLoc()
                snakeSize += 1

        getCoinX2 = [
            coin_x > position_x,
            coin_x < position_x+len_x,
            coin_x+coin > position_x,
            coin_x+coin < position_x+len_x
        ]
        getCoinY2 = [
            coin_y > position_y,
            coin_y < position_y+len_y,
            coin_y+coin > position_y,
            coin_y+coin < position_y+len_y
        ]
        if getCoinX2[0] and getCoinX2[1] or getCoinX2[2] and getCoinX2[3]:
            if getCoinY2[0] and getCoinY2[1] or getCoinY2[2] and getCoinY2[3]:
                coin_x, coin_y = coinLoc()
                snakeSize += 1

        points = snakeSize-1
        with open('packages/save.txt') as f:
            file = f.read().split(",")
            tmpsv = int(file[1])

            if points > tmpsv:
                with open('packages/save.txt', 'w') as f:
                    f.write("0,"+str(points))
                    f.close()

        clock.tick(15)

    call(['clear'])
    print('Bye!')
    py_quit()


menu(savePT)
