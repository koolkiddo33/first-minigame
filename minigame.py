import turtle
import math
import time
import random

SCALE = 10
TIMELIMIT = 30
BOUNDS = 300
JERK = 0.25
RADIUS = 10

pos = [0,0]
velocity = [0,0]
acceleration = [0,0]

turtle.penup()
turtle.hideturtle()
turtle.tracer(0, 0)

def drawCircle(RADIUS):
    turtle.setheading(0)
    turtle.forward(RADIUS)
    turtle.setheading(90)
    turtle.pendown()
    turtle.circle(RADIUS)
    turtle.penup()
    turtle.setheading(0)
    turtle.forward(-RADIUS)
    turtle.setheading(90)

def right():
    acceleration[0] += 1
def left():
    acceleration[0] -= 1
def up():
    acceleration[1] += 1
def down():
    acceleration[1] -= 1

def drawBounds(BOUNDS):
    turtle.goto(-BOUNDS, -BOUNDS)
    turtle.pendown()
    turtle.setheading(90)
    for i in range(4):
        turtle.forward(BOUNDS*2)
        turtle.right(90)
    turtle.penup()

score = 0
goalRadius = random.randint(20, 30)
goalPos = [random.randint(-(0.9*BOUNDS-goalRadius), 0.9*BOUNDS-goalRadius), random.randint(-(0.9*BOUNDS-goalRadius), 0.9*BOUNDS-goalRadius)]
startTime = time.time()
deltaTime = 0
gameTime = 0
while(gameTime < TIMELIMIT):
    loopStart = time.time()
    drawBounds(BOUNDS)

    turtle.onkeypress(right, 'd')
    turtle.onkeypress(left, 'a')
    turtle.onkeypress(up, 'w')
    turtle.onkeypress(down, 's')
    turtle.listen()

    # Calculate the acceleration using JERK
    # x-direction
    if acceleration[0] != 0:
        if acceleration[0] >= -JERK*deltaTime*SCALE and acceleration[0] <= JERK*deltaTime*SCALE:
            acceleration[0] = 0
        elif acceleration[0] > JERK*deltaTime*SCALE:
            acceleration[0] -= JERK*deltaTime*SCALE
        else:
            acceleration[0] += JERK*deltaTime*SCALE
    # y-direction
    if acceleration[1] != 0:
        if acceleration[1] >= -JERK*deltaTime*SCALE and acceleration[1] <= JERK*deltaTime*SCALE:
            acceleration[1] = 0
        elif acceleration[1] > JERK*deltaTime*SCALE:
            acceleration[1] -= JERK*deltaTime*SCALE
        else:
            acceleration[1] += JERK*deltaTime*SCALE

    velocity[0] += acceleration[0]*deltaTime*SCALE
    velocity[1] += acceleration[1]*deltaTime*SCALE
    pos[0] += velocity[0]*deltaTime*SCALE
    pos[1] += velocity[1]*deltaTime*SCALE

    turtle.goto(goalPos[0], goalPos[1])
    drawCircle(goalRadius)

    turtle.goto(pos[0], pos[1])
    drawCircle(RADIUS)

    turtle.goto(-BOUNDS, BOUNDS)
    turtle.write('Score: ' + str(score))

    turtle.goto(BOUNDS, BOUNDS)
    turtle.write('Time left: ' + str(round(TIMELIMIT - gameTime, 1)), False, 'right')

    # Check if circle in goal
    if pos[0] >= goalPos[0] - (goalRadius - RADIUS) and pos[0] <= goalPos[0] + (goalRadius - RADIUS) and pos[1] >= goalPos[1] - (goalRadius - RADIUS) and pos[1] <= goalPos[1] + (goalRadius - RADIUS):
        goalRadius = random.randint(20, 30)
        goalPos = [random.randint(-(0.9*BOUNDS-goalRadius), 0.9*BOUNDS-goalRadius), random.randint(-(0.9*BOUNDS-goalRadius), 0.9*BOUNDS-goalRadius)]
        score += 1

    # Keep in bounds
    if (pos[0] + RADIUS > BOUNDS):
        velocity[0] = -velocity[0]*0.8
        pos[0] = BOUNDS - RADIUS
    if (pos[0] - RADIUS < -BOUNDS):
        velocity[0] = -velocity[0]*0.8
        pos[0] = -BOUNDS + RADIUS
    if (pos[1] + RADIUS > BOUNDS):
        velocity[1] = -velocity[1]*0.8
        pos[1] = BOUNDS - RADIUS
    if (pos[1] - RADIUS < -BOUNDS):
        velocity[1] = -velocity[1]*0.8
        pos[1] = -BOUNDS + RADIUS

    turtle.update()
    turtle.clear()

    # Lag mode B)
    # time.sleep(random.randint(1, 6)/16)
    deltaTime = time.time() - loopStart
    gameTime = time.time() - startTime
    if deltaTime > 0.3:
        print('Lagged for ' + str(round(deltaTime, 3)) + ' seconds at: ' + str(gameTime))
print('Final score: ' + str(score))