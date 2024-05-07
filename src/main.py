import pygame
import math
from random import randint
from boid import Boid

margin = 500
turnfactor = 0.2
visualRange = 30
protectedRange = 2
centeringFactor = 0.0005
avoidfactor = 0.05
matchingfactor = 0.05
maxspeed = 7
minspeed = 2

Pfactor = 0.0005
PAfactor = 5000
Prange = 150
Pmaxspeed = 15
Pminspeed = 1
Pmargin=10
#Pturnfactor = 0.002

boid_count = 100
boids = []
bir = [] # <- boids in range

pygame.init()
screen = pygame.display.set_mode((1000,920))
running = True
clock = pygame.time.Clock()

w,h = pygame.display.get_surface().get_size()

P = Boid(randint(0,w-10), randint(0,h-10), 0, 0)

for i in range(boid_count):
    boids.append(Boid(randint(0,w-100), randint(0,h-100), 0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    XAVG=YAVG=0
    
    for boid in boids:
        close_dx = close_dy = 0
        xvel_avg = yvel_avg = 0
        tot = 0
        x_avg = y_avg = 0
        # getting all of the boids in range and such
        for b in boids:
            d = math.sqrt(abs(boid.x - b.x)**2 + abs(boid.y - b.y)**2) 
            if d <= visualRange:
                bir.append(b)
            totVx = totVy = 0

            totx = toty = 0
            for B in bir:
                if d <= protectedRange:
                    close_dx += boid.x - B.x
                    close_dy += boid.y - B.y
                else:
                    totVx+=B.vx 
                    totVy+=B.vy
                    totx+=B.x 
                    toty+=B.y
                    tot+=1
                    
            if tot !=0:
                xvel_avg=totVx/tot
                yvel_avg=totVy/tot
                x_avg=totx/tot
                y_avg=toty/tot
                    
                    
        boid.vx+=close_dx*avoidfactor
        boid.vy+=close_dy*avoidfactor
        boid.vx+=(xvel_avg-boid.vx)*matchingfactor
        boid.vy+=(yvel_avg-boid.vy)*matchingfactor
        boid.vx+=(x_avg-boid.x)*centeringFactor
        boid.vy+=(y_avg-boid.y)*centeringFactor

        if math.sqrt((boid.x-P.x)**2+(boid.y-P.y)**2) <= Prange:
            boid.vx+=(boid.x-P.x)*PAfactor
            boid.vy+=(boid.y-P.y)*PAfactor

        if boid.x < margin:
            boid.vx=boid.vx + turnfactor
        if boid.x > w-margin:
            boid.vx=boid.vx - turnfactor
        if boid.y < margin:
            boid.vy=boid.vy + turnfactor
        if boid.y > h-margin:
            boid.vy=boid.vy - turnfactor

        speed = math.sqrt(boid.vx**2 + boid.vy**2)
        if speed>maxspeed and speed!=0:
            boid.vx = (boid.vx/speed)*maxspeed
            boid.vy = (boid.vy/speed)*minspeed 
        if speed<minspeed and speed!=0:
            boid.vx = (boid.vx/speed)*minspeed 
            boid.vy = (boid.vy/speed)*minspeed

        boid.x+=boid.vx
        boid.y+=boid.vy
        pygame.draw.circle(screen, (255,255,255), (boid.x,boid.y), 10)
        XAVG+=boid.x 
        YAVG+=boid.y

        bir = []

    XAVG=(XAVG/boid_count)
    YAVG=(YAVG/boid_count)
    pygame.draw.circle(screen, (0,255,0), (XAVG,YAVG),5)
    #print(str(XAVG)+", "+str(YAVG))
    P.vx+=(XAVG-P.x)*Pfactor
    P.vy+=(YAVG-P.y)*Pfactor
    P.x+=P.vx 
    P.y+=P.vy
    # if P.x < Pmargin:
    #     P.vx=P.vx + Pturnfactor
    # if P.x > w-Pmargin:
    #     P.vx=P.vx - Pturnfactor
    # if P.y < Pmargin:
    #     P.vy=P.vy + Pturnfactor
    # if P.y > h-Pmargin:
    #     P.vy=P.vy - Pturnfactor

    speed = math.sqrt(P.vx**2 + P.vy**2)
    if speed>Pmaxspeed and speed!=0:
        P.vx = (P.vx/speed)*Pmaxspeed
        P.vy = (P.vy/speed)*Pminspeed 
    if speed<Pminspeed and speed!=0:
        P.vx = (P.vx/speed)*Pminspeed 
        P.vy = (P.vy/speed)*Pminspeed
    pygame.draw.circle(screen, (255,0,0), (P.x,P.y), 30)

    pygame.display.flip()
    clock.tick(60)

pygame.quit
