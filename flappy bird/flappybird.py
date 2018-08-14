'''|**********************************************************************;
* Project           : Flappy Bird game
*
* Author            : Sourabh Gond
*
* Date created      : 30/7/2018
*
* Purpose           : Just for fun
*
|**********************************************************************'''
import pygame
import os
from random import *
black = (0,0,0)
white = (255,255,255)
WIDTH = 284*3
HEIGHT = 512
SCORE = 0
pygame.init()
pygame.font.init()
display = pygame.display.set_mode((WIDTH,HEIGHT))

def showScore():
    font = pygame.font.SysFont("Comic Sans MS",20)
    txt = 'Score  '+str(SCORE)
    width = font.size(txt)[0]
    textsurface = font.render(txt,False,white)
    display.blit(textsurface,[WIDTH-width,0])

def get_image(image):
    return os.path.join('.','images',image)

class Background:

    def __init__(self):
        self.x = 0
        self.image = pygame.image.load(get_image("background.png")).convert_alpha()

    def showBackground(self):
        for i in range(0,WIDTH+1,WIDTH//3):
            display.blit(self.image,[i+self.x,0])

class Bird:
    upspeed = 6
    downspeed = 2

    def __init__(self):
        self.x = 40
        self.y = HEIGHT/2
        self.up = pygame.image.load(get_image("bird_up.png")).convert_alpha()
        self.down = pygame.image.load(get_image("bird_down.png")).convert_alpha()

    def move(self):
        key = pygame.key.get_pressed()
        if (key[pygame.K_SPACE] or key[pygame.K_UP]) and self.y-Bird.upspeed>0:
            self.y -= Bird.upspeed
            display.blit(self.up,[self.x,self.y])
        else:
            down=1
            if key[pygame.K_DOWN]:
                down = 2
            if self.y + Bird.downspeed*down< HEIGHT-32:
                self.y += (Bird.downspeed*down)
            display.blit(self.down,[self.x,self.y])


class Pipe:
    pipe_dist = 150
    pipe_speed = 5

    def __init__(self):
        y1 = randrange(32,HEIGHT//2,32)
        x = WIDTH-32
        self.pipes = [[x,y1,y1+Pipe.pipe_dist]]
        self.pipe_body = pygame.image.load(get_image("pipe_body.png")).convert_alpha()
        self.pip_end = pygame.image.load(get_image("pipe_end.png")).convert_alpha()

    def move_pipe(self):
        global SCORE
        for pipe in self.pipes:
            pipe[0]-=Pipe.pipe_speed
            if pipe[0]<-50:
                self.pipes.remove(pipe)
                SCORE += 1
        if self.pipes[-1][0]<WIDTH/2:
            y1 = randrange(32, HEIGHT//2, 32)
            x = WIDTH - 32
            self.pipes.append([x,y1,y1+Pipe.pipe_dist])

    def show_pipe(self):
        for pipe in self.pipes:
            i=0
            while i<(pipe[1]//32):
                display.blit(self.pipe_body, [pipe[0], i*32])
                i+=1
            display.blit(self.pip_end,[pipe[0],i*32])
            display.blit(self.pip_end,[pipe[0],pipe[2]])
            i=pipe[2]+32
            while i<HEIGHT:
                display.blit(self.pipe_body,[pipe[0],i])
                i+=32

    def isCollide(self,bird):
        for pipe in self.pipes:
            if pipe[0]<=bird.x and pipe[1]+32>=bird.y:
                return True
            if pipe[0]<=bird.x and pipe[2]-32<=bird.y:
                return True
        return False

def main():
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    running = True
    gameBackground = Background()
    bird = Bird()
    pipe = Pipe()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
        gameBackground.showBackground()
        bird.move()
        pipe.move_pipe()
        pipe.show_pipe()
        if pipe.isCollide(bird):
            running=False
        showScore()
        pygame.display.flip()
        clock.tick(40)
    print('Your Score '+ str(SCORE))
    print('Thank you for playing')
    pygame.quit()
    quit()

if __name__=='__main__':
    main()
