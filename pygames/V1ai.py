import pygame as pg
import algorithm
import master
import numpy as np



# region INIT
pg.init()
a = pg.display.Info()
screenx = a.current_w
screeny = a.current_h
screenm = screeny//2
screenmx = screenx//2

hitbox = False
if hitbox:
    window = pg.display.set_mode((screenx, screeny-60), pg.RESIZABLE)
    cloc = pg.time.Clock()
    fps = 0

active = True
pg.display.set_caption("Among Us")
blob = pg.Rect(screenmx-8, screeny//2+5, 16, 17)
blob_right = pg.Rect(screenmx+5, screeny//2-10, 15, 20)
blob_left = pg.Rect(screenmx-20, screeny//2-10, 15, 20)
imagere = pg.Rect(screenmx-20, screenm-20, 40, 40)
enemy = pg.Rect(screenmx-10, 900, 60, 60)


font = pg.font.Font(None, 36)
horbos=0
frame10 = 0  # 0 to 9
vertical = -10

collision = False
run_speed = 11
max_velocity = 30
jump_str = 36
boost = False
hboost = False

creatureNumber = 0
hitCounter = 0
allFitness = []
genDone = 0
jumpCount = 0

input_w = False
input_a = False
input_d = False
constants = (screenx, screeny, screenmx, screenm)

lands = []  # 0,850;   600,1000;  1200,1150;  1800,1000     <---grasses
#                     180,760; 780,910;   1380,1060;  1980,910      <---stones

for k in range(8):
    absk = (abs(2-k % 4))*150
    if k < 4:
        mon = (pg.Rect(int(600*k), int(1150 - absk), 400, 30))
    else:
        mon = (pg.Rect(int(k*600-2220), int(1060 - absk), 40, 110))
    lands.append(mon)

landse = lands+[enemy]
timer = 0
# endregion


batchSize = 100  # Cant be changed by itself

learningRate = 0.1
afterLearn = 0.04  # Real learning rate, activates after gen20
lr=0.02
continu = False

# region afterINIT
parameters = []
if not continu:
    for i in range(batchSize):
        randomParam = master.init()
        parameters.append(randomParam)
        currentParameter = parameters[0]
else:
    parameters = 50*[np.load('data.npy', allow_pickle=True)]
    currentParameter = parameters[0]
    algorithm.init(currentParameter)
# endregion
relX=0
# region MAIN
while active:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            active = False
    if input_a == input_d:
        jumpCount += 0.02
    if input_a:
        relX+=1
    if input_d:
        relX-=1
    if timer == 900:
        jumpCount-=abs(relX)*0.0001
        relX=0
        fitness = (900-hitCounter)/9-jumpCount/70
        allFitness.append(fitness)
        hitCounter = 0
        jumpCount = 0
        creatureNumber += 1
        if creatureNumber == batchSize:
            print("gen", genDone, max(allFitness))
            if genDone >= 50:
                learningRate = lr
            elif genDone>=20:
                learningRate=afterLearn
            array = np.array(
                (parameters[allFitness.index(max(allFitness))]), dtype=object)
            np.save("data.npy", array, allow_pickle=True)
            genDone += 1
            creatureNumber = 0
            survivingParams = master.elimination(parameters, allFitness)
            parameters = master.mutate(survivingParams, learningRate)
            allFitness = []
        currentParameter = parameters[creatureNumber]
        timer = 0
        input_w = False
        input_a = False
        input_d = False
        frame10 = 0
        vertical = -10
        collision = Falseboost = False
        hboost = False
        enemy = pg.Rect(screenmx-10, 900, 60, 60)
        lands = []  # 0,850;   600,1000;  1200,1150;  1800,1000     <---grasses
#                     180,760; 780,910;   1380,1060;  1980,910      <---stones
        for k in range(8):
            absk = (abs(2-k % 4))*150
            if k < 4:
                mon = (pg.Rect(int(600*k), int(1150 - absk), 400, 30))
            else:
                mon = (pg.Rect(int(k*600-2220), int(1060 - absk), 40, 110))
            lands.append(mon)
        landse = lands+[enemy]

    timer += 1
    leftcol = False
    rightcol = False
    collision = False
    for land in lands:
        if blob.colliderect(land):  # Collisions
            collision = True
            target_level = screenm+19
            target_relative = target_level - land.y
            for lan in landse:
                lan.y += target_relative
        elif vertical > 0:
            gravity_state = 1
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

    #       ALGORITHM

    algorithm.init(currentParameter)
    inputs = algorithm.algorithm(lands[0:4], enemy, constants, timer, collision)
    input_w, input_a, input_d = inputs

    # INPUT

    # press = pg.key.get_pressed()
    if collision:
        vertical = 0
        jumpCount -= 0.05
        if input_w:
            vertical += jump_str
            jumpCount -= 0.15

    elif gravity_state == 1:
        vertical -= 3
    elif gravity_state == 2:
        vertical -= 1
    gravity_state = 0

    if (input_a) and not leftcol:
        for l in landse:
            l.x += run_speed
    if (input_d) and not rightcol:
        for l in landse:
            l.x -= run_speed

    for l in lands:  # platform teleport
        l.y += vertical
        if l.y < -200:
            l.y += 1300
            jumpCount+=40
        if l.x < -700:
            l.x += 2400
            jumpCount -= 35
        elif l.x > screenx+300:
            l.x -= 2400
            jumpCount -= 35


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
        horbos += 1
        if horbos > 180:
            hboost = True
    else:
        hboost = False
        horbos = 0
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
    if hit:
        hitCounter += 1

    #             DISPLAY


    
    if hitbox:
        window.fill((120, 80, 240))
        fpssh = cloc.get_fps()
        pg.draw.rect(window, (200, 200, 200), imagere)
        pg.draw.rect(window, (0, 255, 0), blob)
        pg.draw.rect(window, (0, 255, 0), blob_left)
        pg.draw.rect(window, (0, 255, 0), blob_right)
        for land in lands:
            pg.draw.rect(window, (0, 0, 255), land)
        pg.draw.rect(window, (255, 0, 0), enemy)
        enemy_loc = font.render(f"{erel}", True, (200, 200, 200))
        window.blit(enemy_loc, (20, 40))
        if hit:
            window.blit(font.render(("NOOO"), True, (200, 100, 100)), (20, 60))

        fpsobj = font.render(f"{int(fpssh)}", True, (200, 200, 200))
        window.blit(fpsobj, (20, 20))

        pg.display.flip()
        cloc.tick(fps)
# endregion
pg.quit()
exit()
