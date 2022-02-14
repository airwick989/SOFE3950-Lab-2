import os

userInput = input("Type here: ")
userInput = userInput.split(" ")
command = userInput[0]
parameter = ""

for i in range(1, len(userInput)):
    parameter += f" {userInput[i]}"

print(f"command: {command}, parameter: {parameter}")