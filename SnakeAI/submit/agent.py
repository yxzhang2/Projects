import numpy as np
import utils
import random
import copy


class Agent:
    
    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma

        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()

        self.s=None
        self.a=None
        self.points=0

    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path, self.Q)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def act(self, state, points, dead):
        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        '''
        rPlus=1

        #Getting each variable from states for easy access
        snake_head_x=state[0]
        snake_head_y=state[1]
        snake_body=state[2]
        food_x=state[3]
        food_y=state[4]

        #Create markov decision process by comverting from enviornment space to state space
        #Initialize variables
        adjoining_wall_x=0
        adjoining_wall_y=0
        food_dir_x=0
        food_dir_y=0
        adjoining_body_top=0
        adjoining_body_bottom=0
        adjoining_body_left=0
        adjoining_body_right=0

        #adjoining_wall_x
        if (snake_head_x==40):
            adjoining_wall_x=1
        elif (snake_head_x==480):
            adjoining_wall_x=2
        else:
            adjoining_wall_x=0

        #adjoining_wall_y
        if (snake_head_y==40):
            adjoining_wall_y=1
        elif (snake_head_y==480):
            adjoining_wall_y=2
        else:
            adjoining_wall_y=0
        
        #food_dir_x
        if (snake_head_x==food_x):
            food_dir_x=0        
        elif(food_x<snake_head_x):
            food_dir_x=1
        elif(food_x>snake_head_x):
            food_dir_x=2

        #food_dir_y
        if (snake_head_y==food_y):
            food_dir_y=0        
        elif(food_y<snake_head_y):
            food_dir_y=1
        elif(food_y>snake_head_y):
            food_dir_y=2
        
        #adjoining_body_top
        if ((snake_head_x,snake_head_y-40) in snake_body):
            adjoining_body_top=1
        else:
            adjoining_body_top=0

        #adjoining_body_bottom
        if ((snake_head_x,snake_head_y+40) in snake_body):
            adjoining_body_bottom=1
        else:
            adjoining_body_bottom=0

        #adjoining_body_left
        if ((snake_head_x-40,snake_head_y) in snake_body):
            adjoining_body_left=1
        else:
            adjoining_body_left=0

        #adjoining_body_right
        if ((snake_head_x+40,snake_head_y) in snake_body):
            adjoining_body_right=1
        else:
            adjoining_body_right=0        

        #converted (discretized)state
        cState=(adjoining_wall_x, adjoining_wall_y, food_dir_x, food_dir_y, adjoining_body_top, adjoining_body_bottom, adjoining_body_left, adjoining_body_right)

        if (self.train):
            if (self.s!=None and self.a!=None): #Check for first step
                #Update Q-table
                #Calculate reward for last action
                reward=-0.1 #Nothing happens
                if (points>self.points): #Gets food
                    reward=1
                elif (dead): 
                    reward=-1
                else:
                    reward=-0.1
                alpha=self.C/(self.C+self.N[self.s][self.a])  
                maxQ=max(self.Q[cState][0],self.Q[cState][1],self.Q[cState][2],self.Q[cState][3])  
                self.Q[self.s][self.a]+=alpha*(reward+self.gamma*maxQ-self.Q[self.s][self.a])
                self.points=points

                if (dead):
                    self.reset()                
                    return None
            # #Update N-table

            #temporary copy of Q to calculate f 
            f=copy.deepcopy(self.Q[cState])
            

            for i in range(len(f)):
                if (self.N[cState][i]<self.Ne):
                    f[i]=rPlus
            
            # action = np.argwhere(f == np.amax(f)).flatten().tolist()[-1]
            action=0

            maxF=-np.inf
            if (f[3]>maxF):
                action=3
                maxF=f[3]
            
            if(f[2]>maxF):
                action=2
                maxF=f[2]
            
            if(f[1]>maxF):
                action=1
                maxF=f[1]
            
            if(f[0]>maxF):
                action=0
                maxF=f[0]           




            #action= np.argmax(f)
            if (not dead):
                self.N[cState][action]+=1
            
            self.a=action
            self.s=cState
            return self.actions[action]  


        else:
            action=np.argmax(self.Q[cState])       
            return self.actions[action]
