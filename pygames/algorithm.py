import numpy as np


def sigma(x):
    return 2/(1+np.e**(x/150))-1

def init(parameter):
    global weigh1, weigh2, weigh3, weigh4, bias1, bias2, bias3, bias4
    weigh1, weigh2, weigh3, weigh4, bias1, bias2, bias3, bias4 = parameter


# lands only 4 platforms----enemy----cons screen x y mx my
def algorithm(lands, enemy, constants, time, collision):

    input_a = False
    input_d = False
    input_w = False
    lands_relative = []

    for land in lands:
        lrx = land.x-constants[2]+200
        lry = land.y-constants[3]
        lands_relative.append((lrx, lry, abs(lrx)+abs(lry)))

    if collision:
        collision=1
    else:
        collision=0
    pick = lands_relative[0]

    for lan in lands_relative:
        if lan[2] < pick[2]:
            pick = lan

    inputs = [
        (pick[0]),
        (pick[1]),
        (enemy.x-constants[2]),
        (enemy.y-constants[3])
    ]

    if time:
        time=1
    else:
        time=0
    inpNormal = np.array([
        sigma(inputs[0]),
        sigma(inputs[1]),
        sigma(inputs[2]),
        sigma(inputs[3]),
        np.sin(time/50),
        collision
    ])

    #print(inpNormal)

    # weigh1 = np.array([
    #     [1, 2, 3, 4, 5, 6, 7, 8],
    #     [1, 2, 3, 4, 5, 6, 7, 8],
    #     [1, 2, 3, 4, 5, 6, 7, 8],
    #     [1, 2, 3, 4, 5, 6, 7, 8],
    #     [1, 2, 3, 4, 5, 6, 7, 8]
    # ])

    # bias1 = np.array([1, 2, 3, 4, 5, 6, 7, 8])

    # weigh2 = np.array([
    #     [1, 2, 3, 4, 5, 6],
    #     [1, 2, 3, 4, 5, 6],
    #     [1, 2, 3, 4, 5, 6],
    #     [1, 2, 3, 4, 5, 6],
    #     [1, 2, 3, 4, 5, 6],
    #     [1, 2, 3, 4, 5, 6],
    #     [1, 2, 3, 4, 5, 6],
    #     [1, 2, 3, 4, 5, 6]
    # ])

    # bias2 = np.array([1, 2, 3, 4, 5, 6])

    # weigh3 = np.array([
    #     [1, 2, 3],
    #     [1, 2, 3],
    #     [1, 2, 3],
    #     [1, 2, 3],
    #     [1, 2, 3],
    #     [1, 2, 3]
    # ])

    # bias3 = np.array([1, 2, 3])

    layer1 = np.dot(inpNormal, weigh1)+bias1

    layer2 = np.dot(layer1, weigh2)+bias2

    layer3 = np.dot(layer2, weigh3)+bias3

    layer4 = np.dot(layer3, weigh4)+bias4

    if layer4[0]>0:
        input_w=True
    if layer4[1]>0:
        input_a=True
    if layer4[2]>0:
        input_d=True

    #print(layer3)

    return input_w, input_a, input_d


# if __name__ == "__main__":
#     algorithm()
