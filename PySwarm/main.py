import pygame
import time
import numpy as np
from helper_funcs import draw_grid
from drone import drone
from controller import controller

(width, height) = (1500, 1000)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PySwarm")


background = pygame.Surface(screen.get_size())
background = background.convert()

#Initrialize Drone class
drone = drone(screen,9,30)

#Initrialize controller class
path= '/home/roman/Documents/PySwarm/state_action_matrices/state_action_matrix_triangle9.txt'
controller = controller(path,9)

#Start simulation loop
running = True

while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    drone.find_state()
    new_states = controller.new_states(drone.states)
    id = controller.who_moves()
    targ_pos = drone.positions[id] + controller.position_change(new_states[id],30)

    moving = True

    while moving:

        screen.blit(background, (0,0))
        background.fill((255,255,255))
        draw_grid(screen, background)
        pygame.display.flip()
        drone.positions[id] = controller.controller_motion(drone.positions[id], targ_pos)
        controller.can_i_move(drone.positions, drone.threshold_distance)
        drone.draw_drone(background)
        #time.sleep(0.1)



        if drone.positions[id][0] == targ_pos[0] and drone.positions[id][1] == targ_pos[1]:
            moving = False


pygame.quit()
