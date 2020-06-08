import pygame
import time
import numpy as np
from helper_funcs import bin_dec


class drone:


    def __init__(self, screen, n, d):


        #Number of drones

        self.n = n

        #Set distance at which drones are able to detect other drones

        self.threshold_distance = d


        #List to store positions in 2d of all drones

        self.positions = [[int(x/2) for x in screen.get_size()]]

        #Spawn the drones in random connected topology

        for d in range(n-1):

            #Start off at the centre
            position = [int(x/2) for x in screen.get_size()]

            switch = True

            while switch:

                position[0] += self.threshold_distance * np.random.randint(-1,2)
                position[1] += self.threshold_distance * np.random.randint(-1,2)

                if (position in self.positions):
                    pass
                else:
                    self.positions.append(position)
                    switch = False

        self.positions = np.array(self.positions)





    def find_state(self):

        #List storing states for all drones
        self.states = []

        #This loop finds local state for each drone
        for n in range(self.n):

            #Find which drones are close enough
            distance_vect = np.delete(self.positions, n, 0) - self.positions[n]
            distance_mag = np.linalg.norm(distance_vect, axis = 1)
            in_neighbourhood_bool = distance_mag <= self.threshold_distance*np.sqrt(2)+2
            #Add 2 above to avoid possible confusion

            in_neighbourhood = distance_vect[in_neighbourhood_bool]

            #Calculate the angles the drone makes with its surrouding drones
            angles = np.arctan2(in_neighbourhood[:,1], in_neighbourhood[:,0])*(180/np.pi)
            bearings = np.zeros(angles.shape)

            for n in range(len(angles)):

                if angles[n] >= 90:
                    bearings[n] = 450 - angles[n]
                else:
                    bearings[n] = 90 - angles[n]

            state = np.zeros(8)

            #From the angles extract the states
            for angle in bearings:

                if angle >= 337.5 or angle <= 22.5:
                    state[0] = 1
                else:
                    state[int(np.round(angle/45))] = 1


            state = bin_dec(state)

            self.states.append(state)

        self.states = np.array(self.states)





    def new_pos(self):

        self.positions += 5*np.random.randint(-1,2,(self.positions.shape))




    def draw_drone(self,background):
        #Draw all the drones onto the background
        for position in self.positions:

            pygame.draw.circle(background, (2, 0 ,220 ,0.1), position, 10)
