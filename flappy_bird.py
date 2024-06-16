import pygame
import neat
import time
import os
import random

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
        # blit is a pygame function that draws one image onto another image

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200  # gap between pipes
    VEL = 5  # velocity of the pipes because pipes are moving and not the bird

    def __init__(self, x): 
        self.x = x
        self.height = 0
        self.gap = 100
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


def draw_window(win, bird):
    win.blit(BG_IMG, (0, 0))  # Draw the background
    bird.draw(win)  # Draw the bird
    pygame.display.update()  # Update the display

def main():
    pygame.init()  # Initialize Pygame
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    bird = Bird(200, 200)

    run = True
    while run:
        clock.tick(30)  # 30 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.move()
        draw_window(win, bird)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()