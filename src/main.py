import pygame
import math
from random import randint
from boid import Boid

turnfactor = 0.2
visualRange = 20
protectedRange = 2
centeringFactor = 0.0005
avoidfactor = 0.05
matchingfactor = 0.05
maxspeed = 3
minspeed = 2

boid_count = 50
boids = []
bir = [] # <- boids in range

pygame.init()
screen = pygame.display.set_mode((500,500))
running = True
clock = pygame.time.Clock()

w,h = pygame.display.get_surface().get_size()

for i in range(boid_count):
    boids.append(Boid(randint(0,w-10), randint(0,h-10), 0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    
    for boid in boids:
        close_dx = close_dy = 0
        # getting all of the boids in range and such
        for b in boids:
            d = math.sqrt(abs(boid.x - b.x)**2 + abs(boid.y - b.y)**2) 
            if d <= visualRange:
                bir.append(b)
            for B in bir:
                if d <= protectedRange:
                    close_dx += boid.x - B.x
                    close_dy += boid.y - B.y
                else:
                    
                    
        boid.vx+=close_dx
        boid.vy+=close_dy
        boid.x+=boid.vx*avoidfactor
        boid.y+=boid.vy*avoidfactor
        pygame.draw.circle(screen, (255,255,255), (boid.x,boid.y), 10)

        bir = []


    pygame.display.flip()
    clock.tick(60)

pygame.quit
