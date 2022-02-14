import os

from pytest import param



#convert to absolute path and change directory
def cd(path):
    try:
        if(path == ""):
            print(f"The current working directory is {os.getcwd()}\n")
        else:
            os.chdir(os.path.abspath(path))
    except Exception:
        print("cd: no such file or directory: {}".format(path))

def dir(path):
    contents = []
    i = 1

    try:
        if(path == ""):
            contents = os.listdir(os.getcwd())
            print(f"The contents of the current working directory are: \n")
            for item in contents:
                print(f"{i} - {item}\n")
                i = i+1
        else:
            contents = os.listdir(path)
            print(f"The contents of the specified directory are: \n")
            for item in contents:
                print(f"{i} - {item}\n")
                i = i+1
    except Exception:
        print("dir: no such file or directory: {}".format(path))


########################################################-- LOOP STARTS HERE --################################################################
os.system('cls')
while True:
    userInput = input(f"{os.getcwd()}\n>> ")
    
    userInput = userInput.split(" ")
    command = userInput[0]
    parameter = ""

    for i in range(1, len(userInput)):
        if i == 1:
            parameter += userInput[i]
        else:
            parameter += f" {userInput[i]}"

    #print(f"command: {command}, parameter: {parameter}")

    if command == "cd":
        cd(parameter)
    elif command == "clr":
        os.system('cls')
    elif command == "dir":
        dir(parameter)
    else:
        print(f"{command} is not a recognized command\n")


