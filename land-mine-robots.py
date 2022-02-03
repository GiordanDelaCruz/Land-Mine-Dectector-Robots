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

# TODO: Finish Implementation
# Create file path
def create_path_file(rover_num):

    # initialize rover path file
    init_rover_path(rover_num)

    # 1. read rover data from API
    api_link = base_link + str(rover_num)
    response = requests.get(api_link)

    # 1.1 Query only specific parameters from the JSON String
    # moveSeq = response.json()['data']['moves']
    moveSeq = "MMLMLMRMM"

    # DEBUG
    print("\nRover {num}\n".format(num = rover_num))  

    for action in moveSeq:

        rover_char = rover_orientation(action)
        # update_rover_path(rover_char, path_2d_arr)

# Determine rover orientation
def rover_orientation(action):

    # Initialize values
    direction = Direction.DOWN
    rover_ori = "V"
    prev_rover_ori = "V"

    clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
    idx = clock_wise.index(direction)

    # 3.1 move forward (M)
    if action == "M":
        new_dir = clock_wise[idx] # no change  NOTE: POTENTIALLY DO NOT NEED THIS

    # 3.2 move left (L)
    elif action == "L":
        next_idx = (idx + 1) % 4
        new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        
    # 3.3 move right(R)    
    elif action == "R":
        next_idx = (idx - 1) % 4
        new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d
    
    # 3.4 dig mine (D)
    else: 
        pass
        # next_idx = (idx - 1) % 4
        # new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

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
    dir_path = 'rover-data'
    file_name = "path_" + str(rover_num) + ".txt"
    file_path = os.path.join(dir_path, file_name)

    # save rover's path
    # TODO: change text file to save path rather than move sequence 
    file = open(file_path, "w")

    # read map 
    map_2d_arr = read_map_data("map.txt")
    path_2d_arr = map_2d_arr

    num_of_row = len(path_2d_arr)
    num_of_col = len(path_2d_arr[0])
    counter = 0

    # DEBUG
    print("num of row: {row}, num of col: {col}".format(row = num_of_row, col = num_of_col))

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

# TODO: Implement        
# Update rover path map  
def update_rover_path(rover_char, path_2d_arr):
    pass

    


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
create_path_file(1)

# Part 2: Parallel Program
# for i in range(1, 11):
#     create_path_file(i)
