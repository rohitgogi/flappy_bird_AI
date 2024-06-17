"""
The game of flappy bird. That was made with python;
pygame. Features pixel perfect collision using masks,
and a simple genetic algorithm to train the bird to
play and eventually beat the game.

Date Modified:  Jun 17, 2024
Author: Rohit Gogi
"""

import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 500  # Window width
WIN_HEIGHT = 800  # Window height

# Load images
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x  # x position
        self.y = y  # y position
        self.tilt = 0  # tilt of the bird
        self.tick_count = 0  # time/frame rate counter
        self.vel = 0  # velocity
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2  # displacement formula for free fall
        if d >= 16:  # terminal velocity (max displacement) so we don't fall too fast
            d = 16
        if d < 0:  # if we are moving up, move up a bit more
            d -= 2  # jump this amount higher
        self.y = self.y + d  # move the bird up or down based on the displacement calculation
        if d < 0 or self.y < self.height + 50:  # if we are moving up, tilt up or tilt down if we are moving down
            if self.tilt < self.MAX_ROTATION:  # if we are going up and we are not tilted all the way up, tilt up
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:  # if we are falling down really fast, tilt down all the way
                self.tilt -= self.ROT_VEL

    def draw(self, win):  # draw the bird
        self.img_count += 1  # keep track of how many times we have shown an image
        self.img = self.IMGS[self.img_count // self.ANIMATION_TIME % len(self.IMGS)]  # get the image to show based on the image count using modulo
        if self.tilt <= -80:  # if we are nose diving, show the bird with wings straight
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)  # rotate the bird around the center of the image
        win.blit(rotated_image, new_rect.topleft)  # draw the bird rotated at the center of the image

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200  # gap between pipes
    VEL = 5  # velocity of the pipes because pipes are moving and not the bird

    def __init__(self, x): 
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        if t_point or b_point:
            return True
        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_window(win, birds, pipes, base, score, generation):
    win.blit(BG_IMG, (0, 0))  # Draw the background

    for pipe in pipes:
        pipe.draw(win)
    for bird in birds:
        bird.draw(win)  # Draw the birds
    
    base.draw(win)  # Draw the base

    # Draw the score
    font = pygame.font.SysFont("comicsans", 50)
    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    # Draw the generation count
    text = font.render("Gen: " + str(generation), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    pygame.display.update()  # Update the display


def main(genomes, config, generation):
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    pygame.init()  # Initialize Pygame
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    bird = Bird(200, 200)
    base = Base(730)
    pipes = [Pipe(600)]
    score = 0

    run = True
    while run:
        clock.tick(30)  # 30 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
        
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):  # enumerate allows us to loop over something and have an automatic counter
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)  # remove the bird
                    nets.pop(x)  # remove the neural net associated with the bird
                    ge.pop(x)  # remove the genome associated with the bird

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
        
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            
            pipe.move()
        
        if add_pipe:
            score += 1

            for g in ge:  # give a fitness score of 5 for passing a pipe, favoring birds that can pass pipes
                g.fitness += 5

            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        base.move()
        draw_window(win, birds, pipes, base, score, generation)



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    generation = 0  # Initialize the generation counter

    while True:
        generation += 1
        p.run(lambda genomes, config: main(genomes, config, generation), 1)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)  # Gets the current directory's path
    config_path = os.path.join(local_dir, "config.txt")  # Gets the path to the config file
    run(config_path)  # Runs the main function with the config file path
