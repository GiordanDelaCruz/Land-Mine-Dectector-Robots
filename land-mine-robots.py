# ----------------------------------------------------------------------------------------
# COE 892 — Distributed & Cloud Computing 
# Lab #1 
#
# @author Giordan Andrew
# @date Jan 29, 2022 
# ----------------------------------------------------------------------------------------

# Import Libraries 
import requests
import json
import os
import threading
import time
from enum import Enum
from array import *

# Global variables
base_link = "https://coe892.reev.dev/lab1/rover/"
init_flag = False

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class myThread (threading.Thread):

   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name

   def run(self):
      print("Starting " + self.name)

      # Get lock to synchronize threads
      threadLock.acquire()

      # Create Rover Path


      # Free lock to release next thread
      threadLock.release()


# Declare Functions

# TODO: Finish Implementation NEED TO FIX IMPLEMENTATION
# Create file path
def create_path_file(rover_num):

    # initialize rover path file
    path_list = init_rover_path(rover_num)

    # 1. read rover data from API
    api_link = base_link + str(rover_num)
    response = requests.get(api_link)

    # 1.1 Query only specific parameters from the JSON String
    # moveSeq = response.json()['data']['moves']
    # moveSeq = "MMLMLMRMM"
    moveSeq = "MLLLMRRRM"

    # DEBUG
    print("\nRover {num}\n".format(num = rover_num))  

    for action in moveSeq:

        rover_char_list = rover_orientation(action)
        update_rover_path(rover_num, rover_char_list, path_list)

init_flag = False

# Determine rover orientation
def rover_orientation(action):

    global init_flag

    # Initialize values
    if ( init_flag == False):
        direction = Direction.DOWN
        rover_ori = "V"
        prev_rover_ori = "V"
        move_flag = False
        init_flag = True
        print("(Inside if) init_flag ={init_flag}".format(init_flag = init_flag))
    
    direction = Direction.DOWN
    clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
    idx = clock_wise.index(direction)

    print("init_flag ={init_flag}".format(init_flag = init_flag))

    # Save previous orientation
    prev_rover_ori = rover_ori

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

    # DEBUG
    print("\nMove: {move}. Direction: {name}, Move Flag: {move_flag}. Rover Orientation: {rover_ori}, Previous Rover Orientation: {prev_rover_ori}".format( move = action, name = direction.name, move_flag = move_flag, rover_ori = rover_ori, prev_rover_ori = prev_rover_ori) )

    return rover_ori, prev_rover_ori, move_flag

# Read map data
def read_map_data(text_file):
    with open(text_file) as file:
        firstline = file.readline()
        # 4.1. save number of row & columns
        row = int( firstline.split(' ')[0] )
        col = int ( firstline.split(' ')[1] )

    # 4.2 save map data
    file = open(text_file, "r")
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

    return map_2d_arr
  
# Initialize rover path file
def init_rover_path(rover_num):

     # create file & save each respective rover data
    dir_path = "rover-data"
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
threadLock = threading.Lock()
threads = []

# Create new threads
thread1 = myThread(1, "Thread-1")
thread2 = myThread(2, "Thread-2")

# Start new Threads
thread1.start()
thread2.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()
print("Exiting Main Thread")




# Part 1: Sequential Program
for i in range(1, 2):
    create_path_file(i)

# Part 2: Parallel Program
# for i in range(1, 11):
#     create_path_file(i)
