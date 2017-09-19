import pygame
import time
import random

pygame.init()

crash_sound = pygame.mixer.Sound("Crash.wav")
pygame.mixer.music.load('Jazz.wav')

pause = False

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)

red = (200, 0, 0)
bright_red = (255, 0, 0)

yellow = (200, 200, 0)
bright_yellow = (255, 255, 0)

green = (0, 200, 0)
bright_green = (0, 255, 0)

car_width = 128

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

car_img = pygame.image.load('race_car.bmp')
icon = pygame.image.load('race_car_icon.bmp')
pygame.display.set_icon(car_img)


def quit_game():
    pygame.quit()
    quit()


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def things_dodged(count):
    font = pygame.font.SysFont('comicsansms', 25)
    max_score = open("score_saver.txt", 'r').read()
    text_max_score = font.render("Max Score: " + str(max_score), True, red)
    this_score = font.render("Your score: " + str(count), True, red)
    gameDisplay.blit(text_max_score, (0, 0))
    gameDisplay.blit(this_score, (0, 30))


def car(x, y):
    gameDisplay.blit(car_img, (x, y))


def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def message_display(text):
    large_text = pygame.font.SysFont('comicsansms', 115)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(text_surf, text_rect)

    pygame.display.update()

    time.sleep(2)

    game_loop()


def crashed(new_score):
    output_new_score = False
    old_score = open("score_saver.txt", 'r').read()
    if int(new_score) > int(old_score):
        output_new_score = True
        save_score = open("score_saver.txt", 'w')
        save_score.write(str(new_score))
        save_score.close()

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    large_text = pygame.font.SysFont('comicsansms', 115)
    text_surf, text_rect = text_objects('A bit Racey', large_text)
    text_rect.center = ((display_width / 2), (display_height / 2.3))
    gameDisplay.blit(text_surf, text_rect)

    score = int_check(open("score_saver.txt", 'r').read())
    large_text = pygame.font.SysFont('comicsansms', 20)
    if output_new_score:
        text_surf, text_rect = text_objects('Congratulations!!! New Max Score: ' + score, large_text)
    else:
        text_surf, text_rect = text_objects('Max Score: ' + score, large_text)
    text_rect.center = ((display_width / 2), (display_height / 1.7))
    gameDisplay.blit(text_surf, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()

        button("GO!", 150, 400, 100, 50, green, bright_green, game_loop)
        button("Reset max score", 300, 400, 200, 50, yellow, bright_yellow, reset_score)
        button("EXIT!", 550, 400, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    small_text = pygame.font.SysFont('comicsansms', 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = (x + (w / 2), y + (h / 2))
    gameDisplay.blit(text_surf, text_rect)


def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def paused():
    global pause
    pygame.mixer.music.pause()
    large_text = pygame.font.SysFont('comicsansms', 115)
    text_surf, text_rect = text_objects('Paused', large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(text_surf, text_rect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or pygame.K_ESCAPE:
                    pygame.mixer.music.unpause()
                    pause = False

        button("Continue", 200, 400, 100, 50, green, bright_green, unpause)
        button("EXIT!", 500, 400, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def int_check(s):
    try:
        int(s)
        return s
    except ValueError:
        save_file_temp = open("score_saver.txt", 'w')
        save_file_temp.write("0")
        save_file_temp.close()
        return str(0)


def delete_score():
    save_file = open("score_saver.txt", 'w')
    save_file.write('0')
    save_file.close()
    game_loop()


def reset_score():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        large_text = pygame.font.SysFont('comicsansms', 40)
        text_surf, text_rect = text_objects('You really want to delete your score?', large_text)
        text_rect.center = ((display_width / 2), (display_height / 2.3))
        gameDisplay.blit(text_surf, text_rect)

        score = int_check(open("score_saver.txt", 'r').read())
        large_text = pygame.font.SysFont('comicsansms', 20)
        text_surf, text_rect = text_objects('Max Score: ' + score, large_text)
        text_rect.center = ((display_width / 2), (display_height / 1.7))
        gameDisplay.blit(text_surf, text_rect)

        button("NO!", 150, 400, 100, 50, green, bright_green, game_loop)
        button("Yes!", 550, 400, 100, 50, red, bright_red, delete_score)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()

        gameDisplay.fill(white)
        large_text = pygame.font.SysFont('comicsansms', 115)
        text_surf, text_rect = text_objects('A bit Racey', large_text)
        text_rect.center = ((display_width / 2), (display_height / 2.3))
        gameDisplay.blit(text_surf, text_rect)

        score = int_check(open("score_saver.txt", 'r').read())
        large_text = pygame.font.SysFont('comicsansms', 20)
        text_surf, text_rect = text_objects('Max Score: ' + score, large_text)
        text_rect.center = ((display_width / 2), (display_height / 1.7))
        gameDisplay.blit(text_surf, text_rect)

        button("GO!", 150, 400, 100, 50, green, bright_green, game_loop)
        button("Reset max score", 300, 400, 200, 50, yellow, bright_yellow, reset_score)
        button("EXIT!", 550, 400, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    global pause
    pygame.mixer.music.play(-1)
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_starty = -600
    thing_speed = 5
    thing_width = 150
    thing_height = 150
    dodged = 0

    thing_startx = random.randrange(0, (display_width - 500))
    game_exit = False

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    paused()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10
                if event.key == pygame.K_RIGHT:
                    x_change = 10

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed
        car(x, y)
        things_dodged(dodged)

        if x > display_width - car_width:
            x = 0

        if x < 0:
            x = display_width - car_width

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width - thing_width)
            dodged += 1
            thing_speed += 0.5

        if y < thing_starty + thing_height - 50:
            if ((x > thing_startx) and (x < thing_startx + thing_width)) or \
                    ((x + car_width > thing_startx) and (x + car_width < thing_startx + thing_width)):
                crashed(dodged)

        pygame.display.update()
        clock.tick(60)


game_intro()
pygame.quit()
quit()
