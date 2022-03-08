from enum import Enum
from threading import Thread
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

    # __init__ function
    def __init__(self, number):
        self.rover_number = number #rover number
        self.move_sequence = self.get_rover_moves() #save rover's sequence of moves
        self.location = [0, 0] #current location of rover represented by [x,y]
        self.direction = Direction.SOUTH  #initial direction for rover
        self.map_2d_list = self.generate_map_list() #create 2d list that will save the map layout
        self.path = self.generate_path() #write the rover path in the text file
        self.start_rover()

    # Retrieve rover moves from API
    def get_rover_moves(self):

        # 1. Read rover data from API
        api_link = BASE_LINK + str(self.rover_number)
        response = requests.get(api_link)

        # 2. Save sequence of moves
        self.move_sequence = response.json()['data']['moves']
        # print("\nRover {num}\nmove_seq = {moves}".format(num = self.rover_number, moves = self.move_sequence))  
        # print("Move type: {type}".format( type = type(self.move_sequence[0])) )

        return self.move_sequence

    # Determine the new direction of the rover, based on the move in move_sequence
    def set_direction(self, move):
        
        #Move
        if(move == 'M'):
            self.set_location()
            return
            
        #Dig    
        if(move == 'D'):
            return
        
        # Based off current direction of rover, determine the new direction of the rover if the
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

    # Updates location of rover
    def set_location(self):

        # Get row and col
        row = len(self.map_2d_list)
        col = len(self.map_2d_list[0])

        # Note: location[0] = x-coordinate, location[1] = y-coordinate
        if (self.direction == Direction.NORTH and self.location[1] > 0):
            self.location[1] -= 1

        if (self.direction ==  Direction.EAST and self.location[0] < col -1):
            self.location[0] += 1

        if (self.direction ==  Direction.SOUTH and self.location[1] < row -1):
            self.location[1] += 1

        if (self.direction ==  Direction.WEST and self.location[0] > 0):
            self.location[0] -= 1

        self.map_2d_list[self.location[1]][self.location[0]] = '*'

    # Create map_2d_list from map.txt file
    def generate_map_list(self):
        
        # 1. Declare map_2d_list
        self.map_2d_list  = []

        text_file = "map.txt"
        with open(text_file) as file:
            firstline = file.readline()
            # save number of row & columns
            row = int( firstline.split(' ')[0] )
            col = int ( firstline.split(' ')[1] )

        # 2. Initialize values for map_2d_list
        self.map_2d_list = [[0 for i in range(col)] for j in range(row)]
        colIdx = 0
        rowIdx = 0

        # save map data
        file = open(text_file, "r")
        next(file) # Skip first line in file

        for line in file:
            for char in line:
                # Save data about map
                if char.isalnum():
                    self.map_2d_list[rowIdx][colIdx] = char
                    # DEBUG
                    # print("Row: {rowIdx}, Col: {colIdx}, element: {char}".format(rowIdx= rowIdx, colIdx = colIdx, char = char))
                    colIdx += 1
            rowIdx += 1
            colIdx = 0

        # 3. Creat starting point 
        self.map_2d_list[0][0] = '*'

        return self.map_2d_list
        
    # Write path into rover text files
    def generate_path(self):
        text_file = 'rover-data/path_{}.txt'.format(self.rover_number)
        with open(text_file, 'w') as file:
            for i in self.map_2d_list:
                for j in i:
                    file.write(j)
                file.write('\n')

    # Initialize Rovers
    def start_rover(self):
        for move in self.move_sequence:
            self.set_direction(move)
        self.generate_path()

# Main function
def main():
    start = time.time()
    threads = []
  
    for i in range(1,10):
        thread = "thread{}".format(i)
        temp_arg = '{}'.format(i)
        locals()[thread] = Thread(target=Rover, args=('{}').format(temp_arg))
        threads.append(locals()[thread])
    t10 = Thread(target=Rover, args=('10',)) #thread 10 had to implemented seperately as it needed the "," or would give positional argument errors
    threads.append(t10)
    for i in threads:
        i.start()
    for t in threads:
        t.join()
    end = time.time()
    print("************************************************************")
    print("*                        Threading                         *")
    print("************************************************************\n")
    print("The computation time was: ", (end-start), "seconds\n")

main()
