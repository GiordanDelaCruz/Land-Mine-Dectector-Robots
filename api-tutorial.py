# ----------------------------------------------------------------------------------------
# Note: The purpose of this program is to learn and documente how to use API's 
# in Python. 
# 
# Website Tutorial Link: https://www.dataquest.io/blog/python-api-tutorial/
# ----------------------------------------------------------------------------------------

# Import Libraries 
import requests
import json

# Get data from API endpoint
response = requests.get("https://coe892.reev.dev/lab1/rover/1")

# Return API endpoint status code
print("Status Code:", response.status_code, "\n")

# Print JSON object from API endpoint
print("JSON Object:\n{}" .format(response.json()) )

#  Create a formatted String of the Python JSON object
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Print out the whole String version of the Python JSON Object
print("\nString Version of JSON Object:")
jprint(response.json())

# Query only specific parameters from the JSON String
moveSeq = response.json()['data']['moves']
print("\nRover's Move Data:")
print(moveSeq)
