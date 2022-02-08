# ----------------------------------------------------------------------------------------
# COE 892 — Distributed & Cloud Computing 
# Lab #1 
#
# @author Giordan Andrew
# @date Jan 29, 2022 
# ----------------------------------------------------------------------------------------

# Import Libraries 
from msilib.schema import Class
import requests
import json
import os
import threading
import time
from enum import Enum
from array import *
import threading
from threading import Thread
from time import sleep, perf_counter


# Global variables
base_link = "https://coe892.reev.dev/lab1/rover/"

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


# Rover Class
class Rover:
    # Class variables
    move_sequence = move_sequence
    direction = direction
    character = character
    prev_character = prev_character
    move_flag = move_flag

    # [F] Initialization 
    def _init_(self, number):
        self.number = number
        map_2d_arr = self.read_map_data(self.number)
        path_2d_arr = self.read_map_data(self.number)

    # [F] Get move sequence from API
    def get_move_sequence(self):

        # 1. Read rover data from API
        api_link = base_link + str(self.number)
        response = requests.get(api_link)

        # 1.1 Query only specific parameters from the JSON String
        # moveSeq = response.json()['data']['moves']
        self.move_sequence  = "MMLMLMRMM"

        # DEBUG
        print("\nRover {num}\n".format(num = self.number))  

    # [F] Read map data
    def read_map_data(self, text_file):

        with open(text_file) as file:
            firstline = file.readline()
            # 4.1. save number of row & columns
            row = int( firstline.split(' ')[0] )
            col = int ( firstline.split(' ')[1] )

        # 4.2 save map data
        file = open(text_file, "r")

        # Initialize map_2d_arr with 0's
        map_2d_arr = [[0 for i in range(col)] for j in range(row)]
        colIdx = 0
        rowIdx = 0

        # Skip first line in file
        next(file)
        for line in file:
            for char in line:
                
                # Save data about map
                if char.isalnum():
                    map_2d_arr[rowIdx][colIdx] = char

                    # DEBUG
                    # print("Row: {rowIdx}, Col: {colIdx}, element: {char}".format(rowIdx= rowIdx, colIdx = colIdx, char = char))
                    colIdx += 1

            rowIdx += 1
            colIdx = 0

        # DEBUG
        # print("map in 2D:\n", map_2d_arr)


    # [F] Get map & initialize the values inside the path_2d_arr
    def init_path_2d_arr(self, text_file):

        # create file & save each respective rover data
        dir_path = 'rover-data'
        file_name = "path_" + str(self.number) + ".txt"
        file_path = os.path.join(dir_path, file_name)

        # save rover's path
        file = open(file_path, "w")

        # read map 
        path_2d_arr = self.read_map_data("map.txt")
      
        num_of_row = len(path_2d_arr)
        num_of_col = len(path_2d_arr[0])
        counter = 0

        # DEBUG
        print("num of row: {row}, num of col: {col}".format(row = num_of_row, col = num_of_col))

        # start position of rover
        path_2d_arr[0][0] = "V"

        # load map data into rover path file 
        for row in path_2d_arr:
            for char in row:

                if counter < 5:
                    file.write(char)
                    counter = counter + 1
                else:  
                    string = "\n" + char
                    file.write(string)
                    counter = 1

        prev_row_idx = 0
        prev_col_idx = 0

        return path_2d_arr, prev_row_idx, prev_col_idx

    # [F] Update path_2d_arr
    def update_path_2d_arr(self):

        # Need to fix
        # Initialize values
        self.direction = Direction.DOWN
        self.character = "V"
        self.prev_character = "V"
        self.move_flag = False

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(direction)

        for action in self.move_sequence:
            # 3.1 move forward (M)
            if action == "M":
                new_dir = clock_wise[idx] # no change  NOTE: POTENTIALLY DO NOT NEED THIS
                move_flag = True

            # 3.2 move left (L)
            elif action == "L":
                next_idx = (idx + 1) % 4
                new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
                move_flag = False
                
            # 3.3 move right(R)    
            elif action == "R":
                next_idx = (idx - 1) % 4
                new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d
                move_flag = False
            
            # 3.4 dig mine (D)
            else: 
                pass

            direction = new_dir

            # Determine rover orientation
            # Case #1: Rover faces SOUTH
            if prev_rover_ori == "V": 
                if direction.name == "LEFT":
                    self.character = ">"
                elif direction.name == "RIGHT":
                    self.character = "<"

            # Case 2: Rover faces EAST
            elif prev_rover_ori == ">":
                if direction.name == "LEFT":
                    self.character = "^"
                elif direction.name == "RIGHT":
                    self.character = "V"

            # Case 3: Rover faces NORTH
            elif prev_rover_ori == "^":
                if direction.name == "LEFT":
                    self.character = "<"
                elif direction.name == "RIGHT":
                    self.character = ">"
                    
            # Case 4: Rover faces WEST
            elif prev_rover_ori == "<":
                if direction.name == "LEFT":
                    self.character = "V"
                elif direction.name == "RIGHT":
                    self.character = "^"

            # Save previous orientation
            prev_rover_ori = self.character

            # DEBUG
            print("Move: {move}. Direction: {name}, Value: {value}. Rover Orientation: {rover_ori}".format( move = action, name = direction.name, value = direction.value, rover_ori = rover_ori) )

        return rover_ori, prev_rover_ori, move_flag

    
    # Update path_rover text file with path_2d_arr
    def update_rover_path(self):

        # Get rover characters
        move_flag = rover_char_list[2]
        prev_rover_char = rover_char_list[1]
        rover_char = rover_char_list[0]
        
        # Get path map & previous row & col index
        path_2d_arr = path_list[0]
        prev_row_idx = path_list[1]
        prev_col_idx = path_list[2]

        # First case of updating rover
        # Note: May not need

        # TODO: FIX LOGIC
        # Determine new row & col index from;
        #  1) prev_rover_char
        #  2) rover_char
        # if prev_rover_char == "V" and prev_row_idx == 0 and prev_col_idx == 0:

        if rover_char == "V" and move_flag == True:
            prev_row_idx = prev_row_idx + 1
        elif rover_char == ">" and move_flag == True:
            prev_col_idx = prev_col_idx + 1
        elif rover_char == "<" and move_flag == True:
            prev_col_idx = prev_col_idx - 1
        elif rover_char == "^" and move_flag == True:
            prev_row_idx = prev_row_idx - 1

        path_2d_arr[prev_row_idx][prev_col_idx] = rover_char

        # DEBUG
        print(path_2d_arr)

        # create file & save each respective rover data
        dir_path = 'rover-data'
        file_name = "path_" + str(rover_num) + ".txt"
        file_path = os.path.join(dir_path, file_name)

        # save rover's path
        file = open(file_path, "w")

        # load map data into rover path file 
        counter = 0
        for row in path_2d_arr:
            for char in row:

                if counter < 5:
                    file.write(char)
                    counter = counter + 1
                else:  
                    string = "\n" + char
                    file.write(string)
                    counter = 1






# Declare Functions

# TODO: Finish Implementation
# Create file path
def create_path_file(rover_num):

    # initialize rover path file
    path_list = init_rover_path(rover_num)

    # 1. read rover data from API
    api_link = base_link + str(rover_num)
    response = requests.get(api_link)

    # 1.1 Query only specific parameters from the JSON String
    # moveSeq = response.json()['data']['moves']
    moveSeq = "MMLMLMRMM"

    # DEBUG
    print("\nRover {num}\n".format(num = rover_num))  

    for action in moveSeq:

        rover_char_list = rover_orientation(action)
        update_rover_path(rover_num, rover_char_list, path_list)

# Determine rover orientation
def rover_orientation(action):

    # Initialize values
    direction = Direction.DOWN
    rover_ori = "V"
    prev_rover_ori = "V"
    move_flag = False

    clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
    idx = clock_wise.index(direction)

    # 3.1 move forward (M)
    if action == "M":
        new_dir = clock_wise[idx] # no change  NOTE: POTENTIALLY DO NOT NEED THIS
        move_flag = True

    # 3.2 move left (L)
    elif action == "L":
        next_idx = (idx + 1) % 4
        new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        move_flag = False
        
    # 3.3 move right(R)    
    elif action == "R":
        next_idx = (idx - 1) % 4
        new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d
        move_flag = False
    
    # 3.4 dig mine (D)
    else: 
        pass

    direction = new_dir

    # Determine rover orientation
    # Case #1: Rover faces SOUTH
    if prev_rover_ori == "V": 
        if direction.name == "LEFT":
            rover_ori = ">"
        elif direction.name == "RIGHT":
            rover_ori = "<"

    # Case 2: Rover faces EAST
    elif prev_rover_ori == ">":
        if direction.name == "LEFT":
            rover_ori = "^"
        elif direction.name == "RIGHT":
            rover_ori = "V"

    # Case 3: Rover faces NORTH
    elif prev_rover_ori == "^":
        if direction.name == "LEFT":
            rover_ori = "<"
        elif direction.name == "RIGHT":
            rover_ori = ">"
            
    # Case 4: Rover faces WEST
    elif prev_rover_ori == "<":
        if direction.name == "LEFT":
            rover_ori = "V"
        elif direction.name == "RIGHT":
            rover_ori = "^"

    # Save previous orientation
    prev_rover_ori = rover_ori

    # DEBUG
    print("Move: {move}. Direction: {name}, Value: {value}. Rover Orientation: {rover_ori}".format( move = action, name = direction.name, value = direction.value, rover_ori = rover_ori) )

    return rover_ori, prev_rover_ori, move_flag


  
# Initialize rover path file
def init_rover_path(rover_num):

    # create file & save each respective rover data
    dir_path = 'rover-data'
    file_name = "path_" + str(rover_num) + ".txt"
    file_path = os.path.join(dir_path, file_name)

    # save rover's path
    file = open(file_path, "w")

    # read map 
    map_2d_arr = read_map_data("map.txt")
    path_2d_arr = map_2d_arr

    num_of_row = len(path_2d_arr)
    num_of_col = len(path_2d_arr[0])
    counter = 0

    # DEBUG
    print("num of row: {row}, num of col: {col}".format(row = num_of_row, col = num_of_col))

    # start position of rover
    path_2d_arr[0][0] = "V"

    # load map data into rover path file 
    for row in path_2d_arr:
        for char in row:

            if counter < 5:
                file.write(char)
                counter = counter + 1
            else:  
                string = "\n" + char
                file.write(string)
                counter = 1

    prev_row_idx = 0
    prev_col_idx = 0

    return path_2d_arr, prev_row_idx, prev_col_idx

# TODO: Implement        
# Update rover path map  
def update_rover_path(rover_num, rover_char_list, path_list):
    
    # Get rover characters
    move_flag = rover_char_list[2]
    prev_rover_char = rover_char_list[1]
    rover_char = rover_char_list[0]
    
    # Get path map & previous row & col index
    path_2d_arr = path_list[0]
    prev_row_idx = path_list[1]
    prev_col_idx = path_list[2]

    # First case of updating rover
    # Note: May not need

    # TODO: FIX LOGIC
    # Determine new row & col index from;
    #  1) prev_rover_char
    #  2) rover_char
    # if prev_rover_char == "V" and prev_row_idx == 0 and prev_col_idx == 0:

    if rover_char == "V" and move_flag == True:
        prev_row_idx = prev_row_idx + 1
    elif rover_char == ">" and move_flag == True:
        prev_col_idx = prev_col_idx + 1
    elif rover_char == "<" and move_flag == True:
        prev_col_idx = prev_col_idx - 1
    elif rover_char == "^" and move_flag == True:
        prev_row_idx = prev_row_idx - 1

    path_2d_arr[prev_row_idx][prev_col_idx] = rover_char

    # DEBUG
    print(path_2d_arr)

    # create file & save each respective rover data
    dir_path = 'rover-data'
    file_name = "path_" + str(rover_num) + ".txt"
    file_path = os.path.join(dir_path, file_name)

    # save rover's path
    file = open(file_path, "w")

    # load map data into rover path file 
    counter = 0
    for row in path_2d_arr:
        for char in row:

            if counter < 5:
                file.write(char)
                counter = counter + 1
            else:  
                string = "\n" + char
                file.write(string)
                counter = 1

# ----------------------------------------------------------------------------------------
#                                       Main body
# ----------------------------------------------------------------------------------------
# Part 1: Sequential Program

# Create Thread
for i in range(1, 11):
    thread = Rover(rover_num = i)

create_path_file(1)

# Part 2: Parallel Program
# for i in range(1, 11):
#     create_path_file(i)


start_time = perf_counter()

for i in range(1, 11):
    thread = Rover(rover_num = i)

    thread

stask()
stask()

end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')

#
#
#


start_time = perf_counter()

# create two new threads
t1 = Thread(target=ptask)
t2 = Thread(target=ptask)

# start the threads

t1.start()
# print('starting thread ', t1.getName())

t2.start()
# print('starting thread ', t2.name)

# wait for the threads to complete
t1.join()
t2.join()

end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
