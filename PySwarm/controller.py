import time
from PIDController import pidcontroller
import pandas as pd
import numpy as np
from helper_funcs import neighbourhoods

class controller:

    def __init__(self,path,n):

        self.n = n

        #Read action states
        df = pd.read_csv(path, header = None)
        df = df[0].str.split(' ', expand = True)
        df.set_index(0, inplace = True)

        self.action_states = df


        self.moving = np.zeros(self.n)




    def new_states(self,old_states):

        new_states = []

        for state in old_states:

            try:
                movements = self.action_states.loc[str(state)].to_numpy()
                movements = movements[movements != np.array(None)]
                selection = np.random.choice(movements,1)
                new_states.append(int(selection))

            except:
                new_states.append('still')

        return new_states


    def position_change(self,state, d):


        if state == 0:
            change = [0,d]

        elif state == 1:
            change = [d,d]

        elif state == 2:
            change = [d,0]

        elif state == 3:
            change = [d,-d]

        elif state == 4:
            change = [0,-d]

        elif state == 5:
            change = [-d,-d]

        elif state == 6:
            change = [-d,0]

        elif state == 7:
            change = [-d,d]

        else:
            change = [0,0]


        return change


    def can_i_move(self, positions, threshold):

        hoods = neighbourhoods(positions, threshold)

        can_move = []

        for n in range(len(hoods)):

            others_moving = np.delete(self.moving, n, 0)

            #Multiply moving array with in neighbourhood array. Both draw_drone
            #boolean arrays, thus when we multiply them together, if the sum of them
            #resulting array is greater than 0, the drone cannot move.
            mult_arrays = np.multiply(hoods[n], others_moving)

            if np.sum(mult_arrays) > 0:
                can_move.append(False)
            else:
                can_move.append(True)
        print(can_move)
        return can_move






    def who_moves(self):

        drone_id = np.random.randint(self.n-1)
        print(drone_id)
        moving_array = np.zeros(self.n)
        moving_array[drone_id] = 1

        self.moving = moving_array

        return drone_id


    def controller_motion(self, pos, targ_pos):

        #Only adjusting using proportional term
        pid = pidcontroller.PID(1, 0, 0)

        #Find errors for both components
        error_x = targ_pos[0] - pos[0]
        error_y = targ_pos[1] - pos[1]

        max_velocity = 5

        #FUnction to limit velocity
        def set_velocity(vel):

            if vel > max_velocity:
                return max_velocity
            else:
                return vel

        #COntroller Outputs
        output_x = set_velocity(pid.Update(error_x))
        output_y = set_velocity(pid.Update(error_y))

        #Changes in position

        pos[0] += output_x
        pos[1] += output_y

        return pos
