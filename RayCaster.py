import pygame

from math import cos, sin, pi

BLACK = (0,0,0)
WHITE = (255,255,255)
BACKGROUND = (64,64,64)

colors = {
    '1' : (255,255,0),
    '2' : (0, 255, 255),
    }

class Raycaster(object):
    def __init__(self,screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.blocksize = 50
        self.wallHeight = 50

        self.stepSize = 5

        self.setColor(WHITE)

        self.player = {
            "x" : 75,
            "y" : 175,
            "angle" : 0,
            "fov" : 60
            }

    def setColor(self, color):
        self.blockColor = color

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def drawRect(self, x, y, color = WHITE):
        rect = (x, y, self.blocksize, self.blocksize)
        self.screen.fill(color, rect)

    def drawPlayerIcon(self,color):
        rect = (self.player['x'] - 2, self.player['y'] - 2, 5, 5)
        self.screen.fill(color, rect)

    def castRay(self, a):
        rads = a * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if self.map[j][i] != ' ':
                return dist, self.map[j][i]

            self.screen.set_at((x,y), WHITE)

            dist += 5

    def render(self):

        halfWidth = int(self.width / 2)
        halfHeight = int(self.height / 2)

        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):
                
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)

                if self.map[j][i] != ' ':
                    self.drawRect(x, y, colors[self.map[j][i]])

        self.drawPlayerIcon(BLACK)

        for i in range(halfWidth):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / halfWidth
            dist, c = self.castRay(angle)

            x = halfWidth + i 

            # perceivedHeight = screenHeight / (distance * cos( rayAngle - viewAngle) * wallHeight
            h = self.height / (dist * cos( (angle - self.player['angle']) * pi / 180 )) * self.wallHeight

            start = int( halfHeight - h/2)
            end = int( halfHeight + h/2)

            for y in range(start, end):
                self.screen.set_at((x, y), colors[c])



        for i in range(self.height):
            self.screen.set_at( (halfWidth, i), BLACK)
            self.screen.set_at( (halfWidth+1, i), BLACK)
            self.screen.set_at( (halfWidth-1, i), BLACK)


pygame.init()
screen = pygame.display.set_mode((1000,500)) #, pygame.FULLSCREEN)

r = Raycaster(screen)

r.setColor( (128,0,0) )
r.load_map('map.txt')

isRunning = True

while isRunning:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            elif ev.key == pygame.K_w:
                r.player['x'] += cos(r.player['angle'] * pi / 180) * r.stepSize
                r.player['y'] += sin(r.player['angle'] * pi / 180) * r.stepSize
            elif ev.key == pygame.K_s:
                r.player['x'] -= cos(r.player['angle'] * pi / 180) * r.stepSize
                r.player['y'] -= sin(r.player['angle'] * pi / 180) * r.stepSize
            elif ev.key == pygame.K_a:
                r.player['x'] -= cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                r.player['y'] -= sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
            elif ev.key == pygame.K_d:
                r.player['x'] += cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                r.player['y'] += sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
            elif ev.key == pygame.K_q:
                r.player['angle'] -= 5
            elif ev.key == pygame.K_e:
                r.player['angle'] += 5

    screen.fill(BACKGROUND)
    r.render()

    
    pygame.display.flip()

pygame.quit()
