import time
import pygame
import numpy as np
import random as rd
import math
import scipy
from PIL import Image

screen_width = 800
screen_height = 600
cell_size = 2

COLOR_BG = (10,10,100)
COLOR_GRID = (40,40,40)
COLOR_ALIVE_NEXT = (255,255, 0)

#KERNELS
image = Image.open(r'kernels/round.png').convert('L')
K = np.asarray(image)
K = np.clip(K, 0, 1)


def growth(U):
    return 0 + (U==3) - ((U<2)|(U>3))

def growth_B(U):
    #b1, b2, s1, s2 = 34, 45, 34, 58        #square kernel
    b1, b2, s1, s2 = 26, 33, 26, 44     #round kernel
    return 0 + ((U>=b1)&(U<=b2)) - ((U<s1)|(U>s2))

def update2(screen, cells, size, with_progress=False):
    U = scipy.signal.convolve2d(cells, K, mode='same', boundary='wrap')
    temp_cells = np.clip(cells + growth_B(U), 0, 1)

    for row, col in np.ndindex(cells.shape):
        color = COLOR_BG if temp_cells[row, col] == 0 else COLOR_ALIVE_NEXT
        pygame.draw.rect(screen, color, (col*size, row*size, size, size))

    return temp_cells

def Draw(screen, cells, size, with_progress=False):
    for row, col in np.ndindex(cells.shape):
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT
        pygame.draw.rect(screen, color, (col*size, row*size, size, size))



def main(dimx, dimy, cellsize):
    pygame.init()
    screen = pygame.display.set_mode((dimx, dimy))
    pygame.display.set_caption("John Conway's Game of Life")

    cells = np.zeros((dimy // cellsize, dimx // cellsize))

    screen.fill(COLOR_BG)
    #update2(screen, cells, cellsize)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    pygame.display.update()
                if event.key == pygame.K_r and running == False:
                    for r, c in np.ndindex(cells.shape):
                        cells[r, c] = math.floor(rd.randint(0,3)/3)
                    Draw(screen, cells, cellsize)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // cellsize, pos[0] // cellsize] = 1
                Draw(screen, cells, cellsize)
                pygame.display.update()

        if running:
            cells = update2(screen, cells, cellsize, with_progress=True)
            pygame.display.update()

        time.sleep(0.001)


if __name__ == '__main__':
    main(screen_width, screen_height, cell_size)

