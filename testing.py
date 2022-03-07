# Python 3 code to demonstrate
# SHA hash algorithms.
  
from ast import Str
import hashlib
  
# Create a list of strings
str_list = []

# Read file to get pins
with open("mines.txt") as fp:
    Lines = fp.readlines() 

    for line in Lines:
       str_list.append(line)
      
print(str_list)


# Initializing string
for temp_key in str_list:

   while True:

      # Encoding str using encode(), then sending to SHA256()
      output = hashlib.sha256(temp_key.encode())
      # print( output.hexdigest()[0])

      # Determining if hash value starts at 0
      if( output.hexdigest()[0] == "0"):
         result = output

         # Printing the equivalent hexadecimal value.
         print("The hexadecimal equivalent of SHA256 is : ")
         print(result.hexdigest())
         break
      temp_key += "1"
   