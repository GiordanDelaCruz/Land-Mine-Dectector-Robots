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

# 1. read rover data from API
base_link = "https://coe892.reev.dev/lab1/rover/"
for i in range(1, 11):
    api_link = base_link + str(i)
    response = requests.get(api_link)

    # Query only specific parameters from the JSON String
    moveSeq = response.json()['data']['moves']
    print("\nRover {roverNum} Move Data:".format(roverNum = i))
    print(moveSeq)

# 2. create file & save each respective rover data
    #TODO 

# 3. read map data
with open("map.txt") as file:
    firstline = file.readline()
    # 3.1. save number of row & columns
    row = int( firstline.split(' ')[0] )
    col = int ( firstline.split(' ')[1] )

# 3.2 save map data
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


# 4. plot map
    #TODO 
