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
from threading import Thread
from time import perf_counter

# Global variables
base_link = "https://coe892.reev.dev/lab1/rover/"

# Declare Functions
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
    file.write( str(rover_num) )
    # file.write(moveSeq)
    file.close()

    print('done\n')

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

        # 3.1.0 move forward (M) & down
        # prev_char = "M"
        # for char in moveSeq:
            
        #     if char == "M" & prev_char == "M":
        #         file.write("\n*")

        #     # 3.1.1 move forward (M) & right
        #     if char == "M" & prev_char == "R":
        #         file.write("*")

        #     # 3.1.2 move forward (M) & left
        #     if char == "M" & prev_char == "L":
        #         file.write("*")

        #     # 3.2 move left (L)
        #     elif char == "L":
        #             file.write("*")
        #     # 3.3 move right(R)
        #     elif char == "R":
        #             file.write("*")
        #     # 3.4 dig mine (D)
        #     elif char == "D":
        #             file.write("*")

        #     prev_char = char


        # TEMPORARY FUNCTIONALITY   
        file.write(moveSeq)
        file.close()

# 4. read map data
def read_map_data():

    with open("map.txt") as file:
        firstline = file.readline()
        # 4.1. save number of row & columns
        row = int( firstline.split(' ')[0] )
        col = int ( firstline.split(' ')[1] )

    # 4.2 save map data
    file = open("map.txt", "r")
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


# run single thread & time it
start_time = perf_counter()
stask()
end_time = perf_counter()
print(f'\nIt took {end_time- start_time: 0.2f} second(s) to complete.\n\n')


# run multithread & time it
start_time = perf_counter()

# create new threads
t1 = Thread( target=ptask(1) )
t2 = Thread( target=ptask(2) )
t3 = Thread( target=ptask(3) )
t4 = Thread( target=ptask(4) )
t5 = Thread( target=ptask(5) )
t6 = Thread( target=ptask(6) )
t7 = Thread( target=ptask(7) )
t8 = Thread( target=ptask(8) )
t9 = Thread( target=ptask(9) )
t10 = Thread( target=ptask(10) )

# start the threads
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
t9.start()
t10.start()

# wait for the threads to complete
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()
t9.join()
t10.join()

end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
