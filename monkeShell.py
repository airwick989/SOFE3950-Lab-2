import os

from joblib import parallel_backend



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
    try:
        if(path == ""):
            print(f"The current working directory is {os.getcwd()}\n")
        else:
            os.chdir(os.path.abspath(path))
    except Exception:
        print("cd: no such file or directory: {}".format(path))


########################################################-- LOOP STARTS HERE --################################################################
os.system('cls')
while True:
    userInput = input(f"{os.getcwd()}\n>> ")
    
    command = userInput[:3]
    command = command.strip()
    parameter = userInput[3:]
    parameter = parameter.strip()

    #print(f"command: {command}, parameter: {parameter}")

    if command == "cd":
        cd(parameter)
    elif command == "clr":
        os.system('cls')
    elif command == "dir":
        dir(parameter)
    else:
        print(f"{command} is not a recognized command\n")


