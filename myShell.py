import os
import sys



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



def help():
    with open("help.txt") as file_in:
        lines = []
        for line in file_in:
            lines.append(line)
    
    for line in lines:
        print(f"\033[34m{line}\033[37m")



def invoke(program):
    cmd = "/bin/python3"

    pid = os.fork()
    if pid == 0:
        print(f"CHILD: child with pid = {os.getpid()}\n")
        os.execv(cmd, (cmd, program))
        sys.exit()
    elif pid > 0:
        print(f"PARENT: parent with pid = {os.getpid()}\n")
        print("--- EVERYTHING BELOW IS FROM INSIDE THE INVOKED PROGRAM ---\n")
        wval = os.wait()
        print("\n--- BACK INSIDE THE SHELL ---\n")
        print(f"PARENT: child has finished with exit code {wval}\n")
    else:
        print("forking error\n")

def execute(userInput):
    userInput = userInput.split(" ")
    command = userInput[0]
    parameter = ""

    for i in range(1, len(userInput)):
        if i == 1:
            parameter += userInput[i]
        else:
            parameter += f" {userInput[i]}"

    if command == "cd":
        cd(parameter)
    elif command == "clr":
        os.system('clear')
    elif command == "dir":
        dir(parameter)
    elif command == "environ":
        print(f"{os.environ}\n")
    elif command == "echo":
        print(f"{parameter}\n")
    elif command == "help":
        help()
    elif command == "pause":
        input("Press Enter key to continue...\n")
    elif command == "quit":
        print("\033[32mExiting shell...\n>>\033[37m")
        sys.exit()
    else:
        try:
            invoke(command)
        except Exception:
            print(f"{command} is not a recognized program name in the current directory\n")



########################################################-- LOOP STARTS HERE --################################################################

if len(sys.argv) > 1:
    try:
        with open(sys.argv[1]) as file_in:
            lines = []
            for line in file_in:
                lines.append(line)
        
        for line in lines:
            line = line.strip()
            execute(line)
    except Exception:
        print(f"{sys.argv[1]} is not a recognized batch file in the current directory...\nContinuing normal execution\n")
        
while True:
    userInput = input(f"\033[32m{os.getcwd()}\nmyshell>>\033[37m ")
    execute(userInput)
    
    


