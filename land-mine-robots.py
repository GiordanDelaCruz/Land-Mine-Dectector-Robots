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
def single_thread(rover_num):
    create_path_file(rover_num)


def stask():
    print('Starting a task in a single thread ... Thread id... ', threading.get_ident(), '...OS Thread ID...', threading.get_native_id())
    create_path_files()

def ptask(rover_num):
    t = threading.current_thread()
    print('Starting a multi-threaded task ... Thread name... ', t.name, '....Thread ID...', threading.get_ident(), '...OS Thread ID...', threading.get_native_id())
   
    api_link = base_link + str(rover_num)
    response = requests.get(api_link)

     # 1.1 Query only specific parameters from the JSON String
    moveSeq = response.json()['data']['moves']
    print("\nRover {roverNum} Move Data:".format(roverNum = rover_num))
    print(moveSeq)

    # 2. create file & save each respective rover data
    dir_path = 'rover-data'
    file_name = "path_" + str(rover_num) + ".txt"
    file_path = os.path.join(dir_path, file_name)

    # 2.1 save rover's path
    # TODO: change text file to save path rather than move sequence 
    file = open(file_path, "w")
    # file.write(moveSeq)
    file.close()

    print('done\n')

# single thread
def create_path_file(rover_num):

    # 1. read rover data from API
    api_link = base_link + str(rover_num)
    response = requests.get(api_link)

    # 1.1 Query only specific parameters from the JSON String
    # moveSeq = response.json()['data']['moves']
    moveSeq = "MMLMLMRMM"

    # 2. create file & save each respective rover data
    dir_path = 'rover-data'
    file_name = "path_" + str(rover_num) + ".txt"
    file_path = os.path.join(dir_path, file_name)

    # 2.1 save rover's path
    # TODO: change text file to save path rather than move sequence 
    file = open(file_path, "w")

    # 3. plot map
    # TODO: Implement path of rover
    # [straight, right, left]
    direction = Direction.DOWN
    rover_ori = "V"
    prev_rover_ori = "V"

    clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
    idx = clock_wise.index(direction)

    # Read map 
    map_2d_arr = read_map_data("map.txt")
    path_2d_arr = map_2d_arr


    # DEBUG
    print("\nRover {num}\n".format(num = rover_num))  

    # TODO: Fix orientation movement (e.g right & left turns)
    for char in moveSeq:
        
        # 3.1 move forward (M)
        if char == "M":
            new_dir = clock_wise[idx] # no change

        # 3.2 move left (L)
        elif char == "L":
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
            
        # 3.3 move right(R)    
        elif char == "R":
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d
        
        # 3.4 dig mine (D)
        else: 
            pass
            # next_idx = (idx - 1) % 4
            # new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        direction = new_dir

        # Determine rover orientation
        # TODO: Determine correct way to determine rover orientation
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
        
        print("Direction: {name}, Value: {value}. Rover Orientation: {rover_ori}".format( name = direction.name, value = direction.value, rover_ori = rover_ori) )


# multithread
def create_path_files():

    # 1. read rover data from API
    for i in range(1, 11):
        api_link = base_link + str(i)
        response = requests.get(api_link)

        # 1.1 Query only specific parameters from the JSON String
        moveSeq = response.json()['data']['moves']
        # print("\nRover {roverNum} Move Data:".format(roverNum = i))
        # print(moveSeq)

        # 2. create file & save each respective rover data
        dir_path = 'rover-data'
        file_name = "path_" + str(i) + ".txt"
        file_path = os.path.join(dir_path, file_name)

        # 2.1 save rover's path
        # TODO: change text file to save path rather than move sequence 
        file = open(file_path, "w")

        # 3. plot map
        # TODO: Implement path of rover

        direction = down
        for char in moveSeq:
            pass

            # 3.1 move forward (M)
            
            # 3.2 move left (L)
         
            # 3.3 move right(R)
           
            # 3.4 dig mine (D)

# 4. read map data
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

    return map_2d_arr
    # DEBUG
    # print("map in 2D:\n", map_2d_arr)


# Read map
map_2d_arr = read_map_data("map.txt")
print("map in 2D:\n", map_2d_arr)


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
single_thread(10)

# Part 2: Parallel Program



# run single thread & time it
# start_time = perf_counter()
# stask()
# end_time = perf_counter()
# print(f'\nIt took {end_time- start_time: 0.2f} second(s) to complete.\n\n')


# # run multithread & time it
# start_time = perf_counter()

# # create new threads
# t1 = Thread( target=ptask(1) )
# t2 = Thread( target=ptask(2) )
# t3 = Thread( target=ptask(3) )
# t4 = Thread( target=ptask(4) )
# t5 = Thread( target=ptask(5) )
# t6 = Thread( target=ptask(6) )
# t7 = Thread( target=ptask(7) )
# t8 = Thread( target=ptask(8) )
# t9 = Thread( target=ptask(9) )
# t10 = Thread( target=ptask(10) )

# # start the threads
# t1.start()
# t2.start()
# t3.start()
# t4.start()
# t5.start()
# t6.start()
# t7.start()
# t8.start()
# t9.start()
# t10.start()

# # wait for the threads to complete
# t1.join()
# t2.join()
# t3.join()
# t4.join()
# t5.join()
# t6.join()
# t7.join()
# t8.join()
# t9.join()
# t10.join()

# end_time = perf_counter()

# print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
