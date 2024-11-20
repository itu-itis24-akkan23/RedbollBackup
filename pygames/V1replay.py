import pygame
import algorithm
import numpy as np
pygame.init()

a = pygame.display.Info()
screenx = a.current_w
screeny = a.current_h
screenm = screeny//2
screenmx = screenx//2

window = pygame.display.set_mode((screenx, screeny-60), pygame.RESIZABLE)
active = True
pygame.display.set_caption("a")
blob = pygame.Rect(screenx//2-8, screeny//2+5, 16, 17)
blob_right = pygame.Rect(screenx//2+5, screeny//2-10, 15, 20)
blob_left = pygame.Rect(screenx//2-20, screeny//2-10, 15, 20)
jump = False

cloc = pygame.time.Clock()
font = pygame.font.Font(None, 36)
horbos=0
gravity_state = 0
booster = 0
frame10 = 0  # 0 to 9
vertical = -10
hitbox = False
collision = False
run_speed = 11
max_velocity = 30
jump_str = 36
boost = False
hboost=0
fps = 30
input_w=False
input_a=False
input_d=False
constants = (screenx, screeny, screenmx, screenm)

lands = []  #         0,850;   600,1000;  1200,1150;  1800,1000     <---grasses
#                     180,760; 780,910;   1380,1060;  1980,910      <---stones
enemy = pygame.Rect(screenmx-10, 900, 60, 60)
for k in range(8):
    absk = (abs(2-k % 4))*150
    if k < 4:
        mon = (pygame.Rect(int(600*k), int(1150 - absk), 400, 30))
    else:
        mon = (pygame.Rect(int(k*600-2220), int(1060 - absk), 40, 110))
    lands.append(mon)

use = np.load('data.npy', allow_pickle=True)
algorithm.init(use)

landse = lands+[enemy]
image = pygame.image.load("redbol.png")
imagere = image.get_rect()
enemy_img = pygame.image.load("NBALL.png")
enemy_imgre = enemy_img.get_rect()
imagere.topleft = (screenmx-20, screenm-20)
gras = pygame.image.load("graz.png")
stone = pygame.image.load("stone.png")

plats = []
for platform in range(8):
    if platform < 4:
        plats.append(gras.get_rect())
    else:
        plats.append(stone.get_rect())
time=0
while active:

    if time==900:
        exit()
    time+=1
    leftcol = False
    rightcol = False
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            active = False
        elif i.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_h:
                hitbox = not hitbox

    collision = False
    for land in lands:
        if blob.colliderect(land):
            collision = True
            target_level = screenm+19
            target_relative = target_level - land.y
            for lan in landse:
                lan.y += target_relative
        elif vertical > 0:
            gravity_state  = 1
        elif vertical > -max_velocity:
            gravity_state = 2

        if blob_left.colliderect(land):
            leftcol = True
            target_x = screenmx - (19+land.width)
            target_xr = target_x - land.x
            for lan in landse:
                lan.x += target_xr

        if blob_right.colliderect(land):
            rightcol = True
            target_x = screenmx + 19
            target_xr = target_x - land.x
            for lan in landse:
                lan.x += target_xr

    inputs = algorithm.algorithm(lands[0:4], enemy, constants, time, collision)
    input_w, input_a, input_d = inputs
    press = pygame.key.get_pressed()
    if collision:
        vertical = 0
        if input_w:
            vertical += jump_str
    elif gravity_state == 1:
        vertical -= 3
    elif gravity_state == 2:
        vertical -= 1
    gravity_state = 0

    if input_a and not leftcol:
        for l in landse:
            l.x += run_speed
    if input_d and not rightcol:
        for l in landse:
            l.x -= run_speed

    for l in lands:
        l.y += vertical
        if l.y < -200:
            l.y += 1300
        if l.x < -700:
            l.x += 2400
        elif l.x > screenx+300:
            l.x -= 2400

    fpssh = cloc.get_fps()
    frame10 = (frame10 + 1) % 10
    if frame10 == 0:
        pass

    #             ENEMY

    enemy.y += vertical
    erel = (enemy.x-screenmx+30, screenm-enemy.y-30)
    if erel[0] < 0:
        enemy.x += 1
    else:
        enemy.x -= 1

    if abs(erel[0]) > 50:
        horbos+=1
        if horbos>180:
            hboost=True
    else:
        hboost=False
        horbos=0
    if hboost:
        enemy.x -= erel[0]//20

    if erel[1] > 0:
        enemy.y += 8
    enemy.x -= erel[0]//15
    enemy.y += erel[1]//5
    if erel[1] < 20:
        boost = False
        booster = 0
    if erel[1] > 50:
        boost = True
    if boost:
        booster += 1
        if booster > 32:
            enemy.y += erel[1]//5
            enemy.x -= erel[0]//3
        enemy.y += erel[1]//20
        enemy.x -= erel[0]//20

    if enemy.colliderect(imagere):
        hit = True
    else:
        hit = False
        
    #             DISPLAY

    window.fill((120, 80, 240))
    window.blit(image, imagere)

    enemy_imgre.topleft = enemy.topleft
    window.blit(enemy_img, enemy_imgre)

    for p in plats:
        pix = plats.index(p)
        pixx = lands[pix].x
        pixy = lands[pix].y
        if pix < 4:
            p.topleft = (pixx, pixy-17)
            window.blit(gras, p)
        else:
            p.topleft = (pixx, pixy)
            window.blit(stone, p)

    if hitbox   :
        pygame.draw.rect(window, (200, 200, 200), imagere)
        pygame.draw.rect(window, (0, 255, 0), blob)
        pygame.draw.rect(window, (0, 255, 0), blob_left)
        pygame.draw.rect(window, (0, 255, 0), blob_right)
        for land in lands:
            pygame.draw.rect(window, (0, 0, 255), land)
        pygame.draw.rect(window, (255, 0, 0), enemy)
        enemy_loc = font.render(f"{erel}", True, (200, 200, 200))
        window.blit(enemy_loc, (20, 40))
        if hit:
            window.blit(font.render(("NOOO"), True, (200, 100, 100)), (20, 60))
        else:
            window.blit(font.render(("YEEE"), True, (100, 200, 100)), (20, 60))
        fpsobj = font.render(f"{int(fpssh)}", True, (200, 200, 200))
        window.blit(fpsobj, (20, 20))
        inputz = font.render((f"w-{input_w} a-{input_a} d-{input_d}"),True,(200,200,200))
        window.blit(inputz, (20, 80))
        window.blit(font.render((f"{vertical}"), True, (200, 200, 200)), (20, 100))
    pygame.display.flip()
    cloc.tick(fps)
pygame.quit()