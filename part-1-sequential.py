from enum import Enum
import requests
import json
import time

# Global variables
BASE_LINK = "https://coe892.reev.dev/lab1/rover/"

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    
class Rover:

    def __init__(self, number):
        self.rover_number = number #rover number
        self.move_sequence = self.get_rover_moves() #save rover's sequence of moves
        self.location = [0, 0] #current location of rover represented by [x,y]
        self.direction = Direction.SOUTH  #initial direction for rover
        self.map_2d_list = self.generate_map_list() #create 2d list that will save the map layout
        self.path = self.generate_path() #write the rover path in the text file
        self.start_rover()

    def get_rover_moves(self):

        # 1. Read rover data from API
        api_link = BASE_LINK + str(self.rover_number)
        response = requests.get(api_link)

        # 2. Save sequence of moves
        self.move_sequence = response.json()['data']['moves']
        print("\nRover {num}\nmove_seq = {moves}".format(num = self.rover_number, moves = self.move_sequence))  
        # print("Move type: {type}".format( type = type(self.move_sequence[0])) )

        return self.move_sequence
      
    def get_direction(self):
        return self.direction

    #sets the direction of the rover depending on the instructions
    #if instruction is "M" or "D", the relavent function will be called
    def set_direction(self, move):
        
        #Move
        if(move == 'M'):
            self.set_location()
            return
            
        #Dig    
        if(move == 'D'):
            return
        
        #Based off current direction of rover, determine the new direction of the rover if the
        # next move is either 'R' or 'L'

        # North direction case
        if self.direction == Direction.NORTH:
            if move == 'R':
                self.direction = Direction.EAST
                return
            elif move == 'L':
                self.direction =  Direction.WEST
                return

        # East direction case
        elif self.direction == Direction.EAST:
            if move == 'R':
                self.direction = Direction.SOUTH
                return
            elif move == 'L':
                self.direction =  Direction.NORTH
                return

        # South direction case
        elif self.direction == Direction.SOUTH:
            if move == 'R':
                self.direction = Direction.WEST
                return
            elif move == 'L':
                self.direction =  Direction.EAST
                return

        # West direction case
        elif self.direction == Direction.WEST:
            if move == 'R':
                self.direction = Direction.NORTH
                return
            elif move == 'L':
                self.direction =  Direction.SOUTH
                return

    #facilitates the "M" moving of the rover and updates the board_list 
    #if attempting moving through boundary, nothing will happen
    def set_location(self):
        if (self.direction == Direction.NORTH and self.location[1] > 0):
            self.location[1] -= 1
            self.map_2d_list[self.location[1]][self.location[0]] = '*'
        if (self.direction ==  Direction.EAST and self.location[0] < 15):
            self.location[0] += 1
            self.map_2d_list[self.location[1]][self.location[0]] = '*'
        if (self.direction ==  Direction.SOUTH and self.location[1] < 15):
            self.location[1] += 1
            self.map_2d_list[self.location[1]][self.location[0]] = '*'
        if (self.direction ==  Direction.WEST and self.location[0] > 0):
            self.location[0] -= 1
            self.map_2d_list[self.location[1]][self.location[0]] = '*'

    def generate_map_list(self):
        
        # 1. Declare map_2d_list
        self.map_2d_list  = []

        # 2. Initialize values for map_2d_list
        for i in range(15):
           self.map_2d_list.append(['0']*15)

        # 3. Creat starting point 
        self.map_2d_list[0][0] = '*'

        return self.map_2d_list
        

    def generate_path(self):
        # Write path into rover text files
        with open('rover-data/path_{}.txt'.format(self.rover_number), 'w') as f:
            for i in self.map_2d_list:
                for j in i:
                    f.write(j)
                f.write('\n')

    def start_rover(self):

        for move in self.move_sequence:
            self.set_direction(move)
        self.generate_path()


def main():
    start = time.time()
    for i in range(1,11):
        Rover(i)
    end = time.time()
    print("\nThe computation time was: ", (end-start), "seconds\n")

main()
