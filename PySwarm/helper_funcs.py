import pygame
import time
import numpy as np
import itertools


def draw_grid(screen, background):

    for x in np.linspace(0,screen.get_size()[0],30):
        pygame.draw.line(background, (200,200,200), [x,0], [x,screen.get_size()[1] ], 1)

    for y in np.linspace(0,screen.get_size()[1],20):
        pygame.draw.line(background, (200,200,200), [0,y], [screen.get_size()[0],y ], 1)


def action_state():

    #Iterables
    l = [0, 1]
    #Create Permutations
    asm = list(itertools.product(l, repeat = 8))

    return np.vstack(asm)



def bin_dec(state):

    return(int(''.join(map(lambda state: str(int(state)),state)),2))


def dec_bin(state):

    bin = '{0:08b}'.format(state)

    return [int(n) for n in bin]
