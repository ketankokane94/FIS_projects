import argparse
import sys
import random
#import pdb
import gym
from gym import wrappers, logger

class Agent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space
        self.actions_num = 0
        # Keeps track of which wall to move along
        self.wallToCheck = 'left'

    def formState(self, observation):
        #print(observation)
        sum_ = 0

        for value in observation:
            sum_ += value

        #print(sum_)

        if sum_ == 0:
            return 11#'B'
            # blank
        elif sum_ == 390:
            return 22#'W'
            # wall
        elif sum_ == 538:
            return 33#'S'
            # score
        elif sum_ == 513:
            print('player inserted')
            return 44#'P'
            # player
        else:
            # robot
            return 55#'R'

    def analyzeEnvironment(self, observe):
        for row in range(len(observe)):
            for col in range(len(observe[row])):
                observe[row][col] = int(self.formState(observe[row][col]))
        return observe

    def getplayerpos(self, state):
        for row in range(len(state)):
            for col in range(len(state[row])):
                if state[row][col][0] == 44:
                    #44 is player
                    return row, col

    def checkForRobot(self, state, player_x, player_y):
        for row in range(len(state)):
            for col in range(len(state[row])):
                if state[row][col][0] == 55:
                    #55 is robot
                    if row == player_x:
                        return 'y', row, col
                    if col == player_y:
                        return 'x', row, col
        return 'not found', 0, 0

    def checkForDownWall(self, state, player_x, player_y):
        down_wall = 0

        x = player_x
        y = player_y

        # For bottom wall
        while state[x][y][0] == 44:
            x += 1
        # At this point we are at the bottom extreme of the player
        if state[x][y][0] == 22:
            down_wall = 1

        return down_wall

    def checkForUpWall(self, state, player_x, player_y):
        up_wall = 0

        x = player_x
        y = player_y

        # For top wall
        while state[x][y][0] == 44:
            x -= 1
        # At this point we are at the top extreme of the player
        if state[x][y][0] == 22:
            up_wall = 1

        return up_wall

    def checkForRightWall(self, state, player_x, player_y):
        right_wall = 0

        x = player_x
        y = player_y

        # For right wall
        while state[x][y][0] == 44:
            y += 1
        # At this point we are at the right extreme of the player
        if state[x][y][0] == 22:
            right_wall = 1

        return right_wall

    def checkForLeftWall(self, state, player_x, player_y):
        left_wall = 0

        x = player_x
        y = player_y

        # For left wall
        while state[x][y][0] == 44:
            y -= 1
        # At this point we are at the left extreme of the player
        if state[x][y][0] == 22:
            left_wall = 1

        return left_wall

    def determineMotion(self, state, player_x, player_y):
        # We move clockwise

        if self.wallToCheck == 'left':
            # Try to move along left wall by getting to it first and then up

            left = self.checkForLeftWall(state, player_x, player_y)

            if left == 0:
                # Move left
                action = 4
            else:
                up = self.checkForUpWall(state, player_x, player_y)
                if up == 0:
                    # Move up
                    action = 2
                else:
                    # Move right
                    action = 3
                    # Set wall to move along as up
                    self.wallToCheck = 'up'
        elif self.wallToCheck == 'right':
            # Try to move along right wall by getting to it first and then down

            right = self.checkForRightWall(state, player_x, player_y)

            if right == 0:
                # Move right
                action = 3
            else:
                down = self.checkForDownWall(state, player_x, player_y)
                if down == 0:
                    # Move down
                    action = 5
                else:
                    # Move left
                    action = 4
                    # Set wall to move along as down
                    self.wallToCheck = 'down'
        elif self.wallToCheck == 'up':
            # Try to move along top wall by getting to it first and then right

            up = self.checkForUpWall(state, player_x, player_y)

            if up == 0:
                # Move up
                action = 2
            else:
                right = self.checkForRightWall(state, player_x, player_y)
                if right == 0:
                    # Move right
                    action = 3
                else:
                    # Move down
                    action = 5
                    # Set wall to move along as right
                    self.wallToCheck = 'right'
        elif self.wallToCheck == 'down':
            # Try to move along bottom wall by getting to it first and then left

            down = self.checkForDownWall(state, player_x, player_y)

            if down == 0:
                # Move down
                action = 5
            else:
                left = self.checkForLeftWall(state, player_x, player_y)
                if left == 0:
                    # Move left
                    action = 4
                else:
                    # Move up
                    action = 2
                    # Set wall to move along as left
                    self.wallToCheck = 'left'
        return action

    # You should modify this function
    def act(self, observation, reward, done):
        self.actions_num += 1
        action = 1

        if self.actions_num == 24:
            state = self.analyzeEnvironment(observation)

            f = open('sumsssss.txt', 'a')
            for row in range(len(state)):
                for col in range(len(state[row])):
                    f.write(str(state[row][col][0]))
                f.write('\n')
            f.close()

        if self.actions_num > 24:
            state = self.analyzeEnvironment(observation)

            # Determine action
            action = 0

            player_x, player_y = self.getplayerpos(state)

            if player_x != 0 and player_y != 0:
                # Find a robot in line with bot.

                found, robot_x, robot_y = self.checkForRobot(state, player_x, player_y)
                if found == 'x':
                    # Found vertically adjacent to player

                    if robot_x > player_x:
                        action = 13 #downfire
                    else:
                        action = 10 #upfire

                elif found == 'y':
                    # Found horizontally adjacent to player

                    if robot_y > player_y:
                        action = 11  # rightfire
                    else:
                        action = 12  # leftfire
                else :
                    # No bot found in line with player
                    action = 0#self.determineMotion(state, player_x, player_y)

        return action
        #return self.action_space.sample()

## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='Berzerk-v0', help='Select the environment to run')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = gym.make(args.env_id)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = 'random-agent-results'


    env.seed(0)
    agent = Agent(env.action_space)

    episode_count = 100
    reward = 0
    done = False
    score = 0
    special_data = {}
    special_data['ale.lives'] = 3
    ob = env.reset()
    while not done:
        
        action = agent.act(ob, reward, done)
        ob, reward, done, x = env.step(action)
        score += reward
        env.render()
     
    # Close the env and write monitor result info to disk
    print ("Your score: %d" % score)
    env.close()
